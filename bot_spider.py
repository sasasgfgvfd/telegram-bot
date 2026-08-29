import os
import json
import time
import logging
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Any

import httpx
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    InlineQueryResultArticle, InputTextMessageContent
)
from telegram.constants import ChatType
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    InlineQueryHandler, ContextTypes, filters
)

# ============================================================
# SETTINGS
# ============================================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_BOT_TOKEN_HERE")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8379531283"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "MUM_AFROT_OACCOUNT_BOT")
CONTACT_USERNAME = os.getenv("CONTACT_USERNAME", "J_D_D_M")

REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "@AF_R_O_TO")
REQUIRED_CHANNEL_ID = os.getenv("REQUIRED_CHANNEL_ID", "-1001179303301")

# Put the API key in the hosting environment as SMS_API_KEY.
# Do NOT paste a real API key into this file.
SMS_API_KEY = os.getenv("SMS_API_KEY", "")
SMS_API_URL = "https://api.spider-service.com"

# Number of seconds between getCode requests.
CODE_POLL_SECONDS = int(os.getenv("CODE_POLL_SECONDS", "5"))
CODE_POLL_ATTEMPTS = int(os.getenv("CODE_POLL_ATTEMPTS", "18"))

DATA = Path(os.getenv("DATA_DIR", "."))
USERS_DIR = DATA / "id"
STATS_DIR = DATA / "stats"
USERS_DIR.mkdir(parents=True, exist_ok=True)
STATS_DIR.mkdir(parents=True, exist_ok=True)

SALES_FILE = DATA / "sales.json"
TELEGRAM_SALES_FILE = DATA / "telegram.json"
STATS_USERS_FILE = STATS_DIR / "users.txt"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("bot")


# ============================================================
# STORAGE
# ============================================================
def load_json(path: Path, default: Any) -> Any:
    try:
        if not path.exists():
            save_json(path, default)
            return default
        return json.loads(path.read_text(encoding="utf-8") or "null")
    except Exception:
        return default


def save_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


sales = load_json(SALES_FILE, {"sales": {}})
telegram_sales = load_json(TELEGRAM_SALES_FILE, {"sales": {}})


def user_dir(user_id: int) -> Path:
    p = USERS_DIR / str(user_id)
    p.mkdir(parents=True, exist_ok=True)
    return p


def read_user(user_id: int, name: str, default: str = "") -> str:
    try:
        return (user_dir(user_id) / name).read_text(encoding="utf-8").strip()
    except Exception:
        return default


def write_user(user_id: int, name: str, value: Any) -> None:
    (user_dir(user_id) / name).write_text(str(value), encoding="utf-8")


def get_points(user_id: int) -> int:
    try:
        return max(0, int(read_user(user_id, "collect.txt", "0") or 0))
    except ValueError:
        return 0


def set_points(user_id: int, value: int) -> None:
    write_user(user_id, "collect.txt", max(0, int(value)))


def members() -> list[int]:
    if not STATS_USERS_FILE.exists():
        return []
    result = []
    for line in STATS_USERS_FILE.read_text(encoding="utf-8").splitlines():
        try:
            if line.strip():
                result.append(int(line.strip()))
        except ValueError:
            pass
    return list(dict.fromkeys(result))


def register_user(user_id: int) -> None:
    if user_id not in members():
        with STATS_USERS_FILE.open("a", encoding="utf-8") as f:
            f.write(f"{user_id}\n")


# ============================================================
# SPIDER API
# ============================================================
async def spider_request(action: str, **params) -> Any:
    if not SMS_API_KEY:
        raise RuntimeError("SMS_API_KEY غير مضبوط في الاستضافة.")

    query = {"apiKay": SMS_API_KEY, "action": action}
    query.update({k: v for k, v in params.items() if v is not None})

    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        r = await client.get(SMS_API_URL, params=query)
        r.raise_for_status()
        text = r.text.strip()
        try:
            return r.json()
        except Exception:
            return text


def flatten_strings(obj: Any) -> list[str]:
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.append(str(k))
            out.extend(flatten_strings(v))
    elif isinstance(obj, list):
        for x in obj:
            out.extend(flatten_strings(x))
    elif obj is not None:
        out.append(str(obj))
    return out


def find_value(obj: Any, names: set[str]) -> Any:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).lower() in names and v not in (None, ""):
                return v
        for v in obj.values():
            found = find_value(v, names)
            if found not in (None, ""):
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = find_value(v, names)
            if found not in (None, ""):
                return found
    return None


def api_error(obj: Any) -> str | None:
    if isinstance(obj, dict):
        for key in ("error", "errors", "message", "msg"):
            value = obj.get(key)
            if isinstance(value, str) and value.strip():
                low = value.lower()
                if any(x in low for x in ("error", "fail", "invalid", "insufficient", "not found", "no number")):
                    return value
        status = obj.get("status")
        if isinstance(status, str) and status.lower() in {"error", "failed", "fail"}:
            return str(obj.get("message") or obj.get("msg") or "فشل الطلب")
    return None


def extract_number_and_hash(obj: Any) -> tuple[str | None, str | None]:
    number = find_value(obj, {"number", "phone", "phone_number", "mobile"})
    hash_code = find_value(obj, {"hash_code", "hash", "order_id", "id"})

    if isinstance(number, (dict, list)):
        number = None
    if isinstance(hash_code, (dict, list)):
        hash_code = None

    # Some providers return a plain string containing both values.
    if (not number or not hash_code) and isinstance(obj, str):
        import re
        m = re.search(r"(?:number|phone)\s*[:=]\s*([+\d][\d\-\s]+)", obj, re.I)
        if m:
            number = number or m.group(1).strip()
        m = re.search(r"(?:hash_code|hash)\s*[:=]\s*([A-Za-z0-9_-]+)", obj, re.I)
        if m:
            hash_code = hash_code or m.group(1)

    return (
        str(number) if number is not None else None,
        str(hash_code) if hash_code is not None else None,
    )


def extract_code(obj: Any) -> str | None:
    value = find_value(obj, {"code", "sms", "otp", "activation_code", "verification_code"})
    if isinstance(value, (dict, list)):
        return None
    if value is not None:
        s = str(value).strip()
        if s and s.lower() not in {"null", "none", "waiting", "pending"}:
            return s
    if isinstance(obj, str):
        import re
        m = re.search(r"\b(\d{4,8})\b", obj)
        if m:
            return m.group(1)
    return None


def extract_countries(obj: Any) -> list[tuple[str, str]]:
    """
    Best-effort parser for the provider's getCountrys response.
    Returns (country_code, display_name).
    """
    found: list[tuple[str, str]] = []

    def walk(x: Any):
        if isinstance(x, dict):
            # Common object shape: {"PS":"Palestine"} or {"code":"PS","name":"Palestine"}
            code = None
            name = None
            for k, v in x.items():
                lk = str(k).lower()
                if lk in {"code", "country", "country_code", "iso", "iso_code"}:
                    code = str(v) if not isinstance(v, (dict, list)) else None
                if lk in {"name", "country_name", "title", "countryname"}:
                    name = str(v) if not isinstance(v, (dict, list)) else None
            if code and len(code) <= 5:
                found.append((code.upper(), name or code.upper()))

            for k, v in x.items():
                if len(x) <= 50 and isinstance(v, (str, int, float)):
                    sk = str(k)
                    if 2 <= len(sk) <= 5 and sk.isalpha():
                        found.append((sk.upper(), str(v)))
                walk(v)

        elif isinstance(x, list):
            for item in x:
                walk(item)

    walk(obj)

    clean = []
    seen = set()
    for code, name in found:
        key = code.upper()
        if key not in seen and 2 <= len(key) <= 5:
            seen.add(key)
            clean.append((key, name))
    return clean[:100]


# ============================================================
# KEYBOARDS
# ============================================================
def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("شراء رقم 💶", callback_data="saless")],
        [InlineKeyboardButton("جمع النقاط 💲", callback_data="col")],
        [InlineKeyboardButton("شراء نقاط", callback_data="buy")],
        [InlineKeyboardButton("شرح البوت ⁉️", callback_data="about")],
        [InlineKeyboardButton("شراء بوت خاص بك 💬", callback_data="buybot")],
    ])


def admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("إضافة دولة واتساب", callback_data="add"),
            InlineKeyboardButton("حذف دولة واتساب", callback_data="del"),
        ],
        [
            InlineKeyboardButton("إضافة دولة تليجرام", callback_data="addtel"),
            InlineKeyboardButton("حذف تليجرام", callback_data="deltel"),
        ],
        [InlineKeyboardButton("نسخة إحتياطية", callback_data="pointsfile")],
        [InlineKeyboardButton("تبديل الأكواد", callback_data="setcode")],
        [InlineKeyboardButton("رصيد المزود 💰", callback_data="provider_balance")],
        [InlineKeyboardButton("تحديث الدول 🌍", callback_data="provider_countries")],
    ])


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("القائمة الرئيسية 🔙", callback_data="back")]
    ])


def provider_countries_keyboard(kind: str, countries: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    rows = []
    for code, name in countries:
        # Price is controlled by your sales.json / telegram.json.
        rows.append([
            InlineKeyboardButton(
                f"{name} — {code}",
                callback_data=f"provider-{kind}-{code}",
            )
        ])
    rows.append([InlineKeyboardButton("القائمة الرئيسية 🔙", callback_data="back")])
    return InlineKeyboardMarkup(rows)


# ============================================================
# USER FLOW
# ============================================================
async def channel_required(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(REQUIRED_CHANNEL_ID, user_id)
        return member.status not in ("left", "kicked")
    except Exception:
        # If the bot cannot verify membership, don't lock the user out.
        return True


def welcome(user_id: int) -> str:
    return (
        f"أهلا بك يا عزيزي...🍃\n"
        f"في بوت @{BOT_USERNAME} 🔘\n"
        f"نقاطك الآن: ( {get_points(user_id)} )"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.effective_chat or not update.message:
        return

    uid = update.effective_user.id
    register_user(uid)

    if update.effective_chat.type != ChatType.PRIVATE:
        return

    # Referral: /start USER_ID
    if context.args:
        try:
            ref = int(context.args[0])
            if ref != uid:
                ref_file = user_dir(ref) / "mymembers.txt"
                existing = (
                    ref_file.read_text(encoding="utf-8").splitlines()
                    if ref_file.exists() else []
                )
                if str(uid) not in existing:
                    set_points(ref, get_points(ref) + 1)
                    with ref_file.open("a", encoding="utf-8") as f:
                        f.write(f"{uid}\n")
        except Exception:
            pass

    if not await channel_required(context, uid):
        await update.message.reply_text(
            f"عذرا عزيزي... يجب الإشتراك في القناة حتى تتمكن من إستخدام البوت.\n"
            f"إشترك هنا👇\n{REQUIRED_CHANNEL}\n\nثم إضغط /start 👉"
        )
        return

    write_user(uid, "num.txt", "No")
    await update.message.reply_text(welcome(uid), reply_markup=main_keyboard())


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user and update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(
            "أهلا مطوري...\nشبيك لبيك البوت بين يديك",
            reply_markup=admin_keyboard(),
        )


async def send_number_to_user(
    q,
    context: ContextTypes.DEFAULT_TYPE,
    uid: int,
    kind: str,
    country: str,
) -> None:
    # Prevent two simultaneous purchases per user.
    if read_user(uid, "active_hash.txt", ""):
        await q.answer("لديك طلب رقم قيد الانتظار بالفعل.", show_alert=True)
        return

    target = telegram_sales if kind == "telegram" else sales
    item = target.get("sales", {}).get(country, {})
    try:
        price = int(item.get("price", 0))
    except Exception:
        price = 0

    if price <= 0:
        await q.answer("هذه الدولة غير مضافة بسعر في المخزون.", show_alert=True)
        return

    if get_points(uid) < price:
        await q.answer(f"نقاطك غير كافية. السعر: {price} نقطة.", show_alert=True)
        return

    await q.edit_message_text("⏳ جاري طلب الرقم من المزود...")

    try:
        result = await spider_request("getNumber", country=country)
        err = api_error(result)
        if err:
            raise RuntimeError(err)

        number, hash_code = extract_number_and_hash(result)
        if not number or not hash_code:
            raise RuntimeError(
                "المزود ردّ بصيغة غير معروفة. لم يتم خصم النقاط.\n"
                f"الرد: {str(result)[:700]}"
            )

        # Deduct only after successful number acquisition.
        set_points(uid, get_points(uid) - price)
        write_user(uid, "active_hash.txt", hash_code)
        write_user(uid, "active_number.txt", number)
        write_user(uid, "active_price.txt", price)
        write_user(uid, "active_kind.txt", kind)

        await q.edit_message_text(
            f"✅ تم الحصول على الرقم بنجاح\n\n"
            f"📱 الرقم: `{number}`\n"
            f"💰 السعر: {price} نقطة\n"
            f"🔑 رقم الطلب: `{hash_code}`\n\n"
            f"⏳ جاري انتظار كود التفعيل...",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 فحص الكود الآن", callback_data="check_code")],
                [InlineKeyboardButton("🏠 الرئيسية", callback_data="back")],
            ]),
        )

        # Automatic polling.
        asyncio.create_task(poll_code(context, uid, hash_code, number))

    except Exception as e:
        log.exception("getNumber failed")
        await q.edit_message_text(
            f"❌ لم يتم الحصول على الرقم.\n\n{str(e)[:1000]}",
            reply_markup=back_keyboard(),
        )


async def poll_code(context: ContextTypes.DEFAULT_TYPE, uid: int, hash_code: str, number: str):
    for _ in range(CODE_POLL_ATTEMPTS):
        await asyncio.sleep(CODE_POLL_SECONDS)
        if read_user(uid, "active_hash", "") != hash_code:
            return
        try:
            result = await spider_request("getCode", hash_code=hash_code)
            err = api_error(result)
            if err:
                continue
            code = extract_code(result)
            if code:
                await context.bot.send_message(
                    uid,
                    f"📩 وصل كود التفعيل!\n\n"
                    f"📱 الرقم: `{number}`\n"
                    f"🔐 الكود: `{code}`",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🏠 الرئيسية", callback_data="back")]
                    ]),
                )
                clear_active(uid)
                return
        except Exception:
            continue

    await context.bot.send_message(
        uid,
        "⌛ انتهى وقت الانتظار التلقائي للكود.\n"
        "يمكنك الضغط على «فحص الكود الآن» إذا كان الطلب ما زال فعالًا.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 فحص الكود الآن", callback_data="check_code")],
            [InlineKeyboardButton("🏠 الرئيسية", callback_data="back")],
        ]),
    )


def clear_active(uid: int) -> None:
    for name in ("active_hash.txt", "active_number.txt", "active_price.txt", "active_kind.txt"):
        try:
            (user_dir(uid) / name).unlink()
        except FileNotFoundError:
            pass


async def check_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    uid = update.effective_user.id
    hash_code = read_user(uid, "active_hash", "")
    number = read_user(uid, "active_number", "")

    if not hash_code:
        await q.answer("لا يوجد طلب نشط.", show_alert=True)
        return

    await q.answer("جاري الفحص...")
    try:
        result = await spider_request("getCode", hash_code=hash_code)
        err = api_error(result)
        if err:
            await q.answer(err[:180], show_alert=True)
            return

        code = extract_code(result)
        if code:
            await q.edit_message_text(
                f"📩 وصل كود التفعيل!\n\n"
                f"📱 الرقم: `{number}`\n"
                f"🔐 الكود: `{code}`",
                parse_mode="Markdown",
                reply_markup=back_keyboard(),
            )
            clear_active(uid)
        else:
            await q.answer("لم يصل الكود بعد، جرّب بعد قليل.", show_alert=True)
    except Exception as e:
        await q.answer(str(e)[:180], show_alert=True)


# ============================================================
# CALLBACKS
# ============================================================
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    if not q:
        return
    await q.answer()

    uid = update.effective_user.id
    data = q.data or ""

    if data == "back":
        clear_active(uid)
        await q.edit_message_text(welcome(uid), reply_markup=main_keyboard())
        return

    if data == "saless":
        if read_user(uid, "active_hash", ""):
            await q.answer("لديك طلب رقم قيد الانتظار.", show_alert=True)
            return
        await q.edit_message_text(
            "❇️ اختر التطبيق الذي تريد استخدامه:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("واتساب - Whatsapp", callback_data="sales"),
                    InlineKeyboardButton("تيليجرام - Telegram", callback_data="telegram"),
                ],
                [InlineKeyboardButton("القائمة الرئيسية 🔙", callback_data="back")],
            ]),
        )
        return

    if data in ("sales", "telegram"):
        kind = "telegram" if data == "telegram" else "whatsapp"
        try:
            result = await spider_request("getCountrys")
            err = api_error(result)
            if err:
                raise RuntimeError(err)
            countries = extract_countries(result)
            if not countries:
                raise RuntimeError(f"لم أستطع قراءة الدول من رد المزود: {str(result)[:700]}")
            await q.edit_message_text(
                "🌍 اختر الدولة:\n\n"
                f"نقاطك: {get_points(uid)}",
                reply_markup=provider_countries_keyboard(kind, countries),
            )
        except Exception as e:
            await q.edit_message_text(
                f"❌ تعذر جلب الدول من المزود.\n\n{str(e)[:900]}",
                reply_markup=back_keyboard(),
            )
        return

    if data.startswith("provider-"):
        parts = data.split("-", 2)
        if len(parts) == 3:
            await send_number_to_user(q, context, uid, parts[1], parts[2])
        return

    if data == "check_code":
        await check_code(update, context)
        return

    if data == "col":
        await q.edit_message_text(
            f"- https://t.me/{BOT_USERNAME}?start={uid}\n\n"
            "👆 هذا هو رابطك الخاص 👆\n"
            "كل شخص يدخل من خلاله تحصل على نقطة واحدة.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌐 مشاركة الرابط", switch_inline_query="")],
                [InlineKeyboardButton("- العودة", callback_data="back")],
            ]),
        )
        return

    if data == "buy":
        await q.edit_message_text(
            "لشراء النقاط تواصل مع المشرف.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("حساب المطور 🌀", url=f"https://t.me/{CONTACT_USERNAME}")],
                [InlineKeyboardButton("القائمة الرئيسية 🔙", callback_data="back")],
            ]),
        )
        return

    if data == "about":
        await q.edit_message_text(
            "إليك شرح البوت:\n\n"
            "اجمع النقاط من رابط الإحالة، ثم اختر شراء رقم، "
            "واختر الدولة. إذا كان لديك رصيد كافٍ سيطلب البوت الرقم من المزود "
            "ثم ينتظر كود التفعيل.",
            reply_markup=back_keyboard(),
        )
        return

    if data == "buybot":
        await q.edit_message_text(
            f"✅ لشراء بوت خاص بك تواصل مع المطور: @{CONTACT_USERNAME}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("حساب المطور 🌀", url=f"https://t.me/{CONTACT_USERNAME}")],
                [InlineKeyboardButton("القائمة الرئيسية 🔙", callback_data="back")],
            ]),
        )
        return

    # ---------------- ADMIN ----------------
    if uid != ADMIN_ID:
        return

    if data == "provider_balance":
        try:
            result = await spider_request("getBalance")
            await q.edit_message_text(
                f"💰 رد المزود:\n\n`{str(result)[:2500]}`",
                parse_mode="Markdown",
                reply_markup=back_keyboard(),
            )
        except Exception as e:
            await q.edit_message_text(f"❌ {e}", reply_markup=back_keyboard())
        return

    if data == "provider_countries":
        try:
            result = await spider_request("getCountrys")
            countries = extract_countries(result)
            text = "🌍 الدول المتاحة:\n\n" + "\n".join(
                f"• {code} — {name}" for code, name in countries
            )
            await q.edit_message_text(text[:4000], reply_markup=back_keyboard())
        except Exception as e:
            await q.edit_message_text(f"❌ {e}", reply_markup=back_keyboard())
        return

    if data == "pointsfile":
        save_json(DATA / "backup_sales.json", sales)
        save_json(DATA / "backup_telegram.json", telegram_sales)
        await q.edit_message_text("▪ تم عمل نسخة احتياطية بنجاح", reply_markup=admin_keyboard())
        return

    if data == "add":
        context.user_data["admin_state"] = "add_wa_name"
        await q.edit_message_text("أرسل اسم الدولة، مثال: مصر 🇪🇬")
        return

    if data == "addtel":
        context.user_data["admin_state"] = "add_tg_name"
        await q.edit_message_text("أرسل اسم الدولة، مثال: مصر 🇪🇬")
        return

    if data == "del":
        context.user_data["admin_state"] = "del_wa"
        await q.edit_message_text("أرسل كود الدولة لحذفها من قائمة واتساب")
        return

    if data == "deltel":
        context.user_data["admin_state"] = "del_tg"
        await q.edit_message_text("أرسل كود الدولة لحذفها من قائمة تيليجرام")
        return

    if data == "setcode":
        await q.edit_message_text(
            "زر تبديل الأكواد القديم لا يحتاجه مزود Spider؛ "
            "الأكواد تأتي من getCode تلقائيًا.",
            reply_markup=admin_keyboard(),
        )
        return

    if data == "users":
        await q.answer(f"المشتركين: {len(members())}", show_alert=True)
        return

    if data == "set":
        context.user_data["admin_state"] = "broadcast"
        await q.edit_message_text("أرسل الرسالة التي تريد بثها.")
        return

    if data == "stats":
        await q.edit_message_text(
            f"معلومات البوت:\n\n"
            f"@{BOT_USERNAME}\n"
            f"عدد المشتركين: {len(members())}\n"
            f"الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="admin_home")]
            ]),
        )
        return

    if data == "admin_home":
        await q.edit_message_text("لوحة الأدمن", reply_markup=admin_keyboard())
        return


# ============================================================
# ADMIN TEXT INPUT
# ============================================================
async def admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or update.effective_user.id != ADMIN_ID:
        return

    state = context.user_data.get("admin_state")
    text = (update.message.text or "").strip()

    if state == "broadcast":
        count = 0
        for uid in members():
            try:
                await context.bot.send_message(uid, text)
                count += 1
            except Exception:
                pass
        context.user_data.clear()
        await update.message.reply_text(f"تم إرسال الرسالة إلى {count} مستخدم.")
        return

    if state in ("add_wa_name", "add_tg_name"):
        context.user_data["item_name"] = text
        context.user_data["admin_state"] = (
            "add_price_wa" if state == "add_wa_name" else "add_price_tg"
        )
        await update.message.reply_text("أرسل السعر بالنقاط، مثال: 25")
        return

    if state in ("add_price_wa", "add_price_tg"):
        try:
            price = int(text)
            if price <= 0:
                raise ValueError
        except ValueError:
            await update.message.reply_text("السعر يجب أن يكون رقمًا أكبر من صفر.")
            return
        context.user_data["price"] = price
        context.user_data["admin_state"] = (
            "add_code_wa" if state == "add_price_wa" else "add_code_tg"
        )
        await update.message.reply_text("أرسل كود الدولة كما يأتي من المزود، مثال: PS")
        return

    if state in ("add_code_wa", "add_code_tg"):
        code = text.upper()
        target = sales if state == "add_code_wa" else telegram_sales
        path = SALES_FILE if state == "add_code_wa" else TELEGRAM_SALES_FILE
        target.setdefault("sales", {})[code] = {
            "name": context.user_data["item_name"],
            "price": context.user_data["price"],
        }
        save_json(path, target)
        context.user_data.clear()
        await update.message.reply_text(
            f"تمت الإضافة ✅\n"
            f"الدولة: {text}\n"
            f"السعر: {target['sales'][code]['price']} نقطة"
        )
        return

    if state in ("del_wa", "del_tg"):
        target = sales if state == "del_wa" else telegram_sales
        path = SALES_FILE if state == "del_wa" else TELEGRAM_SALES_FILE
        if text.upper() in target.get("sales", {}):
            target["sales"].pop(text.upper())
            save_json(path, target)
            await update.message.reply_text("تم الحذف بنجاح ✅")
        else:
            await update.message.reply_text("هذا الكود غير موجود.")
        context.user_data.clear()
        return


# ============================================================
# INLINE
# ============================================================
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = update.inline_query.from_user.id
    result = InlineQueryResultArticle(
        id=str(time.time_ns()),
        title="◾ شارك رابطك الخاص لتحصل على النقاط",
        description="اضغط هنا لمشاركة رابطك",
        input_message_content=InputTextMessageContent(
            f"احصل على رقمك من البوت 😻\n"
            f"https://t.me/{BOT_USERNAME}?start={uid}"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "دخول للبوت 😻💯",
                url=f"https://t.me/{BOT_USERNAME}?start={uid}"
            )]
        ]),
    )
    await update.inline_query.answer([result], cache_time=1)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.error("Unhandled exception: %s", context.error)


# ============================================================
# START
# ============================================================
def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN == "PUT_YOUR_BOT_TOKEN_HERE":
        raise RuntimeError("ضع BOT_TOKEN في متغير البيئة.")
    if not SMS_API_KEY:
        raise RuntimeError("ضع SMS_API_KEY في متغير البيئة.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_text))
    app.add_error_handler(error_handler)

    log.info("Bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

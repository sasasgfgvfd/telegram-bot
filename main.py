#!/usr/bin/env python
# -*- coding: utf-8 -*-

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @FFJFF5
#====================#

import os
try:
    from telethon.sessions import StringSession
    import asyncio, re, json, shutil
    from kvsqlite.sync import Client as uu
    from telethon.tl.types import KeyboardButtonUrl
    from telethon.tl.types import KeyboardButton, ReplyInlineMarkup
    from telethon import TelegramClient, events, functions, types, Button
    from telethon.tl.types import DocumentAttributeFilename
    import time, datetime, random 
    from datetime import timedelta
    from telethon import TelegramClient, events, Button
    from binance.client import Client
    from datetime import datetime
    import datetime
    import json
    import os
    from telethon.errors import (
        ApiIdInvalidError,
        PhoneNumberInvalidError,
        PhoneCodeInvalidError,
        PhoneCodeExpiredError,
        SessionPasswordNeededError,
        PasswordHashInvalidError
    )
    from plugins.messages import *
    from plugins.get_code import *
    from plugins.SessionConverter import *
    from telethon.errors.rpcerrorlist import UserDeactivatedBanError
    from telethon.sessions import StringSession
    from telethon.tl.types import InputPeerUser, InputPeerChannel
    from telethon.tl.functions.account import GetAuthorizationsRequest
    from telethon.tl.functions.messages import GetHistoryRequest
except:
    os.system("python3 set_module.py")
    try:
        from telethon.sessions import StringSession
        import asyncio, re, json, shutil
        from kvsqlite.sync import Client as uu
        from telethon.tl.types import KeyboardButtonUrl
        from telethon.tl.types import KeyboardButton
        from telethon import TelegramClient, events, functions, types, Button
        from telethon.tl.types import DocumentAttributeFilename
        import time, datetime, random 
        from datetime import timedelta
        from telethon.errors import (
            ApiIdInvalidError,
            PhoneNumberInvalidError,
            PhoneCodeInvalidError,
            PhoneCodeExpiredError,
            SessionPasswordNeededError,
            PasswordHashInvalidError
        )
        from plugins.messages import *
        from plugins.get_code import *
        from plugins.SessionConverter import *
        from telethon.errors.rpcerrorlist import UserDeactivatedBanError
        from telethon.sessions import StringSession
        from telethon.tl.types import InputPeerUser, InputPeerChannel
        from telethon.tl.functions.account import GetAuthorizationsRequest
        from telethon.tl.functions.messages import GetHistoryRequest
    except Exception as errors:
        print('An Erorr with: ' + str(errors))
        exit(0)

bot_enabled = True

def is_bot_enabled():
    global bot_enabled
    return bot_enabled

import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    coind REAL DEFAULT 0.0
)
''')

conn.commit()
conn.close()

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @FFJFF5
#====================#

def get_user_balance(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT coind FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0.0

def update_user_balance(user_id, amount):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT coind FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        new_balance = result[0] + amount
        cursor.execute('UPDATE users SET coind = ? WHERE user_id = ?', (new_balance, user_id))
    else:
        cursor.execute('INSERT INTO users (user_id, coind) VALUES (?, ?)', (user_id, amount))
    
    conn.commit()
    conn.close()

def check_vip(user):
    user_id = int(user)
    users = db.get(f"vip_{user_id}")
    noww = time.time()
    if db.exists(f"vip_{user_id}"):
        last_time = users['vip']
        timeee = int(db.get(f"vip_{user_id}_time"))
        WAIT_TIMEE = int(timeee) * 24 * 60 * 60
        elapsed_time = noww - last_time
        if elapsed_time < WAIT_TIMEE:
            remaining_time = WAIT_TIMEE - elapsed_time
            return int(remaining_time)
        else:
            return None
    else:
        return None
        
from binance.client import Client

from binance.client import Client
from binance.exceptions import BinanceAPIException
        
def get_exchange_rate(currency):
    rates = {
        'BTC': 50000, 
        'USDT': 1,    
        'LTC': 200    
    }
    return rates.get(currency, 1)
        
if not os.path.isdir('database'):
    os.mkdir('database')

API_ID = "24188127"
API_HASH = "e0e2a70a885d1497c8feb47815bb3e36"

admin = 8379531283

token = "8610293571:AAHB_bidYvFFGc26OGZ9iu-KxkUuknFTT9w" #توكن بوتك

binance_api_key = '000000' #ايبي حسابك بينانس
binance_api_secret = '000000' #سيكرت حسابك بينانس

new_password = "@J_D_D_M"

client = TelegramClient('FFJFF5', api_id=API_ID, api_hash=API_HASH).start(bot_token=token)
bot = client

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @FFJFF5
#====================#

MIN_AMOUNT = 0.00001
MAX_AMOUNT = 1000.0

while True: 
    try:
        binance_client = Client(binance_api_key, binance_api_secret)
        print("✅ الاتصال بـ Binance ناجح!")
        break 
    except BinanceAPIException as e:
        if "Service unavailable from a restricted location" in str(e):
            print("⚠️ تم حظر الوصول من موقعك! يستمر البرنامج في العمل...")
            break 
        else:
            print(f"❌ خطأ غير متوقع: {e}")

pending_deposits = {}
countdown_time = 360

wallet_addresses = {
    'BTC': {
        'address': 'bc1q9728ht5ttcctz76f62emq89n5kxg0l04ehrm84',
        'network': 'Bitcoin'
    },
    'USDT': {
        'address': 'TEYNBhRiEuYVWsc33KiTvG6qZuWRGLHRNe',
        'network': 'TRC20'
    },
    'LTC': {
        'address': '0xd9B24A99726178817B79c15c1fFA288A2dBBE9e3',
        'network': 'BNB smart chain (BEP20)'
    }
}

USERS_FILE = 'users.json'

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def generate_random_key():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(16))

import random
import string
from telethon import Button, events

def generate_random_password(length=5):
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choice(characters) for _ in range(length))

def generate_referral_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

users = load_data(USERS_FILE)

db = uu('database/FFJFF5.ss', 'bot')

if not db.exists("accounts"):
    db.set("accounts", [])

if not db.exists("countries"):
    db.set("countries", [])

if not db.exists("bad_guys"):
    db.set("bad_guys", [])

if not db.exists("force"):
   db.set("force", [])

if not db.exists("admins"):
   db.set("admins", [admin])

if not db.exists("auto_charge_enabled"):
    db.set("auto_charge_enabled", True)

if not db.exists("manual_charge_enabled"):
    db.set("manual_charge_enabled", True) 

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @FFJFF5
#====================#

@client.on(events.NewMessage(pattern="/sell_price", func = lambda x: x.is_private))
async def start(event):
    user_id = event.chat_id
    bans = db.get('bad_guys') if db.exists('bad_guys') else []
    async with bot.conversation(event.chat_id) as x:
        countries = db.get("countries")
        text = ""
        for i in countries:
            text += f'{i["name"]} ({i["calling_code"]}): {i["sell_price"]}$'
        await x.send_message(text)
        
from telethon import events, Button
import random
import string
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def generate_verification_image(code):
    width, height = 300, 150
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    for i in range(width):
        r = random.randint(100, 200)
        g = random.randint(100, 200)
        b = random.randint(100, 200)
        draw.line((i, 0, i, height), fill=(r, g, b), width=1)
    
    try:
        font = ImageFont.truetype("arial.ttf", 150)
    except:
        font = ImageFont.load_default()
    
    for _ in range(90):  
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=2)
    
    for _ in range(200): 
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    bbox = draw.textbbox((0, 0), code, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    
    draw.text((x, y), code, font=font, fill=(0, 0, 0))
    
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    img.save("verification_code.png")

def generate_verification_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def cleanup_temp_files():
    if os.path.exists("verification_code.png"):
        os.remove("verification_code.png")

async def show_captcha_buttons(event):
    correct_code = generate_verification_code()
    
    wrong_codes = [generate_verification_code() for _ in range(4)]
    
    all_codes = wrong_codes + [correct_code]
    random.shuffle(all_codes)  
    
    buttons = [
        [Button.inline(code, data=f"captcha_{code}") for code in all_codes[:2]],
        [Button.inline(code, data=f"captcha_{code}") for code in all_codes[2:4]],
        [Button.inline(code, data=f"captcha_{code}") for code in all_codes[4:]],
    ]
    
    generate_verification_image(correct_code)
    
    await event.respond("**🔐 | تحقق أنك لست روبوت:**\n\nالرجاء الضغط على الزر الذي يحتوي على الكود الصحيح.", file="verification_code.png", buttons=buttons)
    
    db.set(f"captcha_{event.chat_id}", correct_code)
    
    cleanup_temp_files()

buttonsr = [
        [Button.inline("📲| حسابات تليجرام جاهزه", data="buy")],
        [Button.inline("تسليم حسابات تليجرام جاهزه", data="seller")],
        [Button.url("فريق الدعم", url="t.me/FFJFF5"), Button.inline("الوكلاء", data="wkala")],
        [Button.inline("شحن رصيد", data="shahn")],
        [Button.url("الشراء الناجح", url="t.me/taf3ilatbot"), Button.inline("الاعدادات", data="SUPEGY")],
        [Button.inline("الاحاله الخاص بك", data="referral")]
    ]
        
@client.on(events.NewMessage(pattern="/start", func=lambda x: x.is_private))
async def start(event):
    user_id = event.chat_id
    bans = db.get('bad_guys') if db.exists('bad_guys') else []
    admins = db.get("admins") if db.exists("admins") else []
    
    if user_id != admin and user_id not in admins:
        if not is_bot_enabled():
            await event.reply("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمة")
            return
    
    referral_id = None
    if len(event.raw_text.split()) > 1: 
        referral_id = event.raw_text.split()[1] 

    keyboard = [
        [Button.inline("- نسخه احتياطيه  ", data="zip_all")],
        [Button.inline("- اعدادات الارقام  ", data="ajxjao")],
        [Button.inline("- الاشتراك الاجباري ", data="ajxkho"), Button.inline("- الادمن ", data="aksgl")],
        [Button.inline("- قناة اثباتات التسليم", data="set_trust_channel")],
        [Button.inline("- الشراء والبيع  ", data="ajkofgl")],
        [Button.inline("- قسم الرصيد ", data="ajkcoingl"), Button.inline("- قسم الحظر ", data="bbvjls")],
        [Button.inline("- تعطيل استقبال دولة ", data="stopcountry")],
        [Button.inline("- الدول المغلق استقبالها ", data="ttrt")],
        [Button.inline("- اذاعة ", data="start_broadcast")],
        [Button.inline("- تغيير سعر الاحالة ", data="amubnf")],
        [Button.inline('تعطيل التلقائي', b'disableauto'), Button.inline('تفعيل التلقائي', b'enableauto')],
        [Button.inline('تعطيل المانيوال', b'disablemanual'), Button.inline('تفعيل المانيوال', b'enablemanual')],
        [Button.inline("- تعيين عنوان المانيوال ", data="setwalletaddress")],
        [Button.inline('تعطيل البوت', b'disablebot'), Button.inline('تفعيل البوت', b'enablebot')],
        [Button.inline("- حالة البوت ", data="sts")],
    ]
      
    new_user_buttons = [
        [Button.inline("✅- تسجيل الدخول.", data="login"), Button.inline("📌- انشاء حساب.", data="create_account")],
        [Button.inline("📃- شرح البوت.", data="sharh")],
        [Button.url("⚠️- الدعم الفني.", url="t.me/FFJFF5")]
    ]
    
    buttons = [
        [Button.inline("📲| حسابات تليجرام جاهزه", data="buy")],
        [Button.inline("تسليم حسابات تليجرام جاهزه", data="seller")],
        [Button.url("فريق الدعم", url="t.me/FFJFF5"), Button.inline("الوكلاء", data="wkala")],
        [Button.inline("شحن رصيد", data="shahn")],
        [Button.url("الشراء الناجح", url="t.me/taf3ilatbot"), Button.inline("الاعدادات", data="SUPEGY")],
        [Button.inline("الاحاله الخاص بك", data="referral")]
    ]
    
    if user_id in bans: 
        return
    
    if not db.exists(f"user_{user_id}"):
        members = 0
        
        if referral_id:
            if db.exists(f"user_{referral_id}"):
                referrer_data = db.get(f"user_{referral_id}")
                referral_amount = referrer_data.get("referral_amount", 0.02)
                referrer_data["coins"] += referral_amount
                db.set(f"user_{referral_id}", referrer_data)

                await client.send_message(
                    referrer_data["id"],
                    f"💎 • تم شحن حسابك بسبب دخول شخص بواسطة رابط الدعوة الذي أرسلته. رصيدك الحالي هو : {referrer_data['coins']}$"
                )
        
        if user_id == admin:
            await event.reply(msgs['ADMIN_MESSAGE'], buttons=keyboard)
            await event.reply(msgs['START_MESSAGE'].format(event.chat_id, 0), buttons=new_user_buttons)
        else:
            await event.reply(msgs['NEW_MESSAGE'].format(event.chat_id, 0), buttons=new_user_buttons)
        
        user_info = await client.get_entity(user_id)
        users = db.keys('user_%')
        for _ in users:
            members += 1
        
        username = "@" + str(user_info.username) if user_info.username else "None"
        await bot.send_message(admin, f'• شخص جديد انضم للبوت 👾\n\n- معلومات الشخص.\n\n- المستخدم : <a href="tg://user?id={user_id}">{user_info.first_name}</a>\n- يوزره : {username}\n- ايديه : {user_id}\n\n• اجمالي المستخدمين : {members}', parse_mode="html")
    else:
        coins = db.get(f"user_{user_id}")["coins"]
        if user_id == admin or user_id in db.get("admins"):
            await event.reply(msgs['ADMIN_MESSAGE'], buttons=keyboard)
            await event.reply(msgs['START_MESSAGE'].format(event.chat_id, coins), buttons=buttons)
        else:
            await event.reply(msgs['START_MESSAGE'].format(event.chat_id, coins), buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b'sts'))
async def toggle_bot(event):
    global bot_enabled
    bot_enabled = not bot_enabled
    status = "مُفعّل ✅" if bot_enabled else "مُعطّل ❌"
    await event.answer(f"- حالة البوت : {status}")

@client.on(events.CallbackQuery(data=b'disablebot'))
async def disable_bot(event):
    global bot_enabled
    if event.sender_id == admin:
        bot_enabled = False
        await event.answer("تم تعطيل البوت ❌")

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @FFJFF5
#====================#

@client.on(events.CallbackQuery(data=b'enablebot'))
async def enable_bot(event):
    global bot_enabled
    if event.sender_id == admin:
        bot_enabled = True
        await event.answer("تم تفعيل البوت ✅")

@bot.on(events.CallbackQuery(pattern=b'disableauto'))
async def disable_auto(event):
    db.set("auto_charge_enabled", False)
    await event.edit("✅ تم تعطيل الشحن التلقائي.")

@bot.on(events.CallbackQuery(pattern=b'enableauto'))
async def enable_auto(event):
    db.set("auto_charge_enabled", True)
    await event.edit("✅ تم تفعيل الشحن التلقائي.")

@bot.on(events.CallbackQuery(pattern=b'disablemanual'))
async def disable_manual(event):
    db.set("manual_charge_enabled", False)
    await event.edit("✅ تم تعطيل الشحن المانيوال.")

@bot.on(events.CallbackQuery(pattern=b'enablemanual'))
async def enable_manual(event):
    db.set("manual_charge_enabled", True)
    await event.edit("✅ تم تفعيل الشحن المانيوال.")

@client.on(events.CallbackQuery(pattern="chargecrypto"))
async def handle_charge_crypto(event):
    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    if not db.get("manual_charge_enabled"):
        await event.respond("⚠️ الشحن المانيوال معطل حاليًا.")
        return

    currency = "USDT"
    
    user_id = event.sender_id
    user_data = db.get(f"user_{user_id}") if db.exists(f"user_{user_id}") else {}
    wallet_address = user_data.get("wallet_address", "TFJymg2niTFaXSvufeatV2C5btgFb3Adsw") 
    
    network = "TRC20"

    await event.edit(
        f"💎 • لإجراء عملية شحن حسابك قم بإرسال المبلغ إلى العنوان التالي ثم اضغط دفعت المبلغ\n\n"
        f"**العملة** : `{currency}`\n"
        f"**العنوان** : `{wallet_address}`\n" 
        f"**الشبكة** : `{network}`\n\n"
        f"⚠️ تأكد من استخدام الشبكة الصحيحة لتجنب فقدان الأموال.",
        buttons=[
            [Button.inline("دفعت المبلغ", data="paidsamount")],
        ]
    )

@client.on(events.CallbackQuery(pattern="setwalletaddress"))
async def set_wallet_address(event):
    user_id = event.sender_id
    await event.edit("- ارسل عنوان المحفظة بعملة USDT شبكة TRC20")

    @client.on(events.NewMessage(from_users=user_id))
    async def handle_wallet_address_message(new_message_event):
        wallet_address = new_message_event.text.strip()

        user_data = db.get(f"user_{user_id}") if db.exists(f"user_{user_id}") else {}
        
        user_data["wallet_address"] = wallet_address
        
        db.set(f"user_{user_id}", user_data)

        await new_message_event.reply(f"✅ • تم تحديث عنوان المحفظة بنجاح \n\n**العنوان الجديد** : {wallet_address}")

        client.remove_event_handler(handle_wallet_address_message)
        
@client.on(events.CallbackQuery(pattern="paidsamount"))
async def handle_paid_amount(event):
    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("• الرجاء إدخال المبلغ الذي أرسلته بـ $")
        amount = await x.get_response()

        await x.send_message("• الرجاء إدخال هاش العملية (hashid)")
        transaction_hash = await x.get_response()

        admin_message = (
            f"⚡ • طلب شحن جديد\n\n"
            f"**المستخدم**: {event.sender_id}\n"
            f"**المبلغ**: {amount.text}$\n"
            f"**هاش العملية**: `{transaction_hash.text}`\n\n"
            f"• قم بالتحقق من العملية ثم اضغط **قبول** أو **رفض**."
        )

        buttons = [
            [Button.inline("قبول", data=f"accepters:{event.sender_id}:{amount.text}")],
            [Button.inline("رفض", data=f"rejecters:{event.sender_id}")]
        ]

        await client.send_message(admin, admin_message, buttons=buttons)

        await x.send_message("⏳ جاري مراجعة العملية .. يستغرق الامر من 5 دقائق الى 12 ساعه")

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @FFJFF5
#====================#

@client.on(events.CallbackQuery(pattern="accepters:"))
async def handle_accept(event):
    data = event.data.decode("utf-8")
    _, user_id, amount = data.split(":")

    user_key = f"user_{user_id}"
    user = db.get(user_key) if db.exists(user_key) else {"id": user_id, "coins": 0.0}

    user["coins"] += float(amount)
    db.set(user_key, user)

    await event.edit("💎 • تمت الموافقة على العملية وإضافة الرصيد إلى حساب المستخدم.")

    await client.send_message(
        int(user_id),
        f"✅ تم التأكد من عملية الشحن\n\n"
        f"**المبلغ **: {amount}$\n"
        f"**رصيدك الحالي **: {user['coins']}$"
    )

@client.on(events.CallbackQuery(pattern="rejecters:"))
async def handle_reject(event):
    data = event.data.decode("utf-8")
    _, user_id = data.split(":")

    await event.edit("💔 تم رفض طلب الشحن")

    await client.send_message(
        int(user_id),
        "❎• تم رفض طلب الشحن الخاص بك. يرجى التحقق من المعلومات والمحاولة مرة أخرى"
    )
        
@client.on(events.CallbackQuery(data="start_broadcast"))
async def ask_for_message(event):
    if event.sender_id == admin:
        async with client.conversation(admin) as conv:
            await conv.send_message("📃- أرسل الرسالة التي تريد اذاعتها لجميع المستخدمين")
            response = await conv.get_response()
            message = response.text

            await conv.send_message(
                f"⚠️ | هل تريد اذاعة هذه الرسالة لجميع المستخدمين؟\n\n"
                f"**الرسالة:**\n{message}",
                buttons=[
                    [Button.inline("✅ نعم، اذاعة", data=f"confirms_broadcast|{message}")],
                    [Button.inline("❌ إلغاء", data="cancel_broadcast")]
                ]
            )

from telethon import events

@client.on(events.CallbackQuery(pattern="amubnf"))
async def amubnf(event):
    user_id = event.sender_id

    await event.edit("💎 • ارسل المبلغ الجديد لكل احالة")

    @client.on(events.NewMessage(from_users=user_id))
    async def handle_message(new_message_event):
        response = new_message_event

        try:
            new_amount = float(response.text)
            if MIN_AMOUNT <= new_amount <= MAX_AMOUNT:
                user_data = db.get(f"user_{user_id}")
                user_data["referral_amount"] = new_amount
                db.set(f"user_{user_id}", user_data)

                await event.reply(f"✅ • تم تحديث المبلغ لكل إحالة إلى : {new_amount}$")
            else:
                await event.reply(f"❌ • المبلغ يجب أن يكون بين {MIN_AMOUNT} و {MAX_AMOUNT}.")
        except ValueError:
            await event.reply("❌ • الرجاء إدخال رقم صحيح أو عشري.")
        
        client.remove_event_handler(handle_message)

@bot.on(events.CallbackQuery(pattern=b'withdraw'))
async def withdraw_start(event):
    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    buttons = [
        [Button.inline("USDT", data="network_USDT")],
        [Button.inline("TRX", data="network_TRX")]
    ]
    await event.edit("**اختر العملة المراد السحب بها**", buttons=buttons)

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @FFJFF5
#====================#

@bot.on(events.CallbackQuery(pattern=b'network_'))
async def choose_network(event):
    data = event.data.decode('utf-8')
    network_type = data.split('_')[1] 
    user_id = event.chat_id

    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    user_data = db.get(f"user_{user_id}")
    if user_data["coins"] < 5:
        await event.answer(" - الحد الادني للسحب 5$.")
        return

    async with bot.conversation(user_id) as conv:
        await conv.send_message(f"- أرسل عنوان  {network_type} الخاص بك بينانس")
        address = await conv.get_response()

        if network_type == "USDT":
            buttons = [
                [Button.inline("USDT-TRC20", data="network_USDT-TRC20")],
                [Button.inline("USDT-ERC20", data="network_USDT-ERC20")]
            ]
            await conv.send_message("**اختر نوع شبكة USDT**", buttons=buttons)
            network_event = await conv.wait_event(events.CallbackQuery)
            network = network_event.data.decode('utf-8').split('_')[1]
        elif network_type == "TRX":
            buttons = [
                [Button.inline("TRC20", data="network_TRC20")],
                [Button.inline("BEP20", data="network_BEP20")]
            ]
            await conv.send_message("**اختر نوع شبكة TRX**", buttons=buttons)
            network_event = await conv.wait_event(events.CallbackQuery)
            network = network_event.data.decode('utf-8').split('_')[1]
        else:
            network = network_type 

        await conv.send_message("- ارسل المبلغ الذي تريد سحبه")
        amount_info = await conv.get_response()

        try:
            amount = float(amount_info.text)
            if amount > user_data["coins"]:
                await conv.send_message("- لا يمكنك سحب مبلغ أكبر من رصيدك.")
                return

            user_data["coins"] -= amount
            db.set(f"user_{user_id}", user_data)

            withdraw_message = await bot.send_message(
                admin, 
                f"• طلب سحب جديد من البوت\n\n"
                f"- ايديه : {user_id}\n"
                f"- يوزره : @{event.sender.username}\n\n"
                f"- الشبكة : {network}\n"
                f"- عنوان المحفظه : {address.text}\n\n"
                f"- المبلغ : {amount}$",
                buttons=[
                    [Button.inline("تأكيد السحب", data=f"confirm_withdraw_{user_id}_{amount}")]
                ]
            )

            await conv.send_message(f"- جاري معالجة طلب السحب الخاص بك بمبلغ ${amount}\n\n- يستغرق الامر من 6 دقائق الى 8 ساعات")
        except ValueError:
            await conv.send_message("- المبلغ يكون ارقام فقط")


@bot.on(events.CallbackQuery(pattern=b'confirm_withdraw_'))
async def confirm_withdraw(event):
    data = event.data.decode('utf-8')
    parts = data.split('_')
    user_id = int(parts[2]) 
    amount = float(parts[3]) 

    await bot.send_message(user_id, f"- تم تأكيد طلب السحب الخاص بك ✅\n\n- المبلغ : {amount}$ \n\n- تحقق من المبلغ في محفظتك")

    await event.edit("تم تأكيد الدفع واشعار المستخدم")

@bot.on(events.CallbackQuery(pattern=b'cancel'))
async def cancel_button(event):
    user_id = event.sender_id  
    coins = db.get(f"user_{user_id}")["coins"]
    buttons = [
        [
            Button.inline("📲| حسابات تليجرام جاهزه", data="buy"),
        ],
        [
            Button.inline("تسليم حسابات تليجرام جاهزه", data="seller"),
        ],
        [
            Button.url("فريق الدعم", url="t.me/FFJFF5"),
            Button.inline("الوكلاء", data="wkala"),
        ],
        [
            Button.inline("شحن رصيد", data="shahn"),
        ],
        [
            Button.url("الشراء الناجح", url="t.me/taf3ilatbot"),
            Button.inline("الاعدادات", data="SUPEGY"),
        ],
        [
            Button.inline("الاحاله الخاص بك", data="referral"),
        ]
    ]
    await event.edit(msgs['START_MESSAGE'].format(user_id, coins), parse_mode='markdown', buttons=buttons)
    return
        
@bot.on(events.CallbackQuery(pattern=b'ajxjao'))
async def numgpv_button(event):
    await event.answer(' - مرحبا بك في قسم التحكم في الحسابات ☎️ .')
    await event.edit('** - مرحبًا يا عزيزي في قسم الأرقام ** \n- يمكنك التحكم في أرقامك بسهولة. \n - يتم تحديث الأرقام تلقائيًا',
                    buttons=[
                        [
                            Button.inline("- عدد ارقام البوت ", data="all_of_number")
                        ],
                        [
                            Button.inline("- اضافة دولة ", data="add_country"),
                            Button.inline("- حذف دولة", data="del_country")
                        ],
                        [
                            Button.inline("- اضافة رقم", data="add"),
                            Button.inline("- حذف رقم", data="delaccount")
                        ],
                        [
                            Button.inline(" رجوع ⬅️ ", data="admin_panel")
                        ]
                    ])

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @FFJFF5
#====================#

@bot.on(events.CallbackQuery(pattern=b'seller'))
async def numgpv_button(event):
    user_id = event.sender_id
    user_info = db.get(f"user_{user_id}") if db.exists(f"user_{user_id}") else {"coind": 0}
    
    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    if "coind" not in user_info:
        user_info["coind"] = 0
    
    await event.edit(
        f'**- ✅ هنا اللوحة المتطورة الخاصة في استلام حسابات تلجرام الجاهزة •\n\n'
        f'🪐 يمكنك بيع حسابات تلجرام لجميع الدول وسحب اموالك عبر عدة طرق دفع متوفرة •\n'
        f'🪐 يمكنك تحويل اموال محفضتك الى رصيد في البوت وشراء حسابات تلجرام جاهزة ايضا •\n'
        f'🪐 يمكنك التواصل مع الدعم في حال كان لديك استفسار حول موضوع ما •\n\n'
        f'🚀 رصيد حسابك : {user_info["coind"]}$**',
        buttons=[
            [
                Button.inline("بيع حساب", data="sell"),
                Button.inline("اسعار الدول", data="buysr")
            ],
            [
                Button.inline("سحب رصيدك ", data="withdraw"),
                Button.inline("تحويل رصيد", data="transfer")
            ],
            [
                Button.url("قناة التحديثات", url="https://t.me/AF_R_O_TO")
            ],
            [
                Button.inline(" رجوع ⬅️ ", data="main")
            ]
        ]
    )
                             
@bot.on(events.CallbackQuery(pattern=b'ajxkho'))
async def nuupv_button(event):
    await event.answer(' - مرحبا بك في قسم الاشتراك الاجباري')
    await event.edit('** يمكنك اضافة وحذف قناة من الاشتراك الاجباري من هذا القسم**',
                    buttons=[
                        [
                            Button.inline("- اضافة قناة ", data="add_force"),
                            Button.inline("- حذف قناة ", data="del_force")
                        ],
                        [
                            Button.inline("رجوع ↪️", data="admin_panel")
                        ]
                    ])
@bot.on(events.CallbackQuery(pattern=b'aksgl'))
async def nuupv_button(event):
    await event.answer(' - مرحبا بك في قسم الادمن‍')
    await event.edit('** يمكنك رفع ادمن وتنزيل ادمن في البوت من هذا القسم **',
                    buttons=[
                        [
                            Button.inline("- رفع ادمن ", data="add_admin"),
                            Button.inline("- تنزيل ادمن ", data="del_admin")
                        ],
                        [
                            Button.inline("رجوع ↪️", data="admin_panel")
                        ]
                    ])
@bot.on(events.CallbackQuery(pattern=b'ajkofgl'))
async def nuupv_button(event):
    await event.answer(' - مرحبا بك في قسم البيع والشراء .')
    await event.edit('**- يمكنك التحكم في اسعار البيع والشراء من هذا القسم**',
                    buttons=[
                        [
                            Button.inline("- سعر الشراء", data="change_price"),
                            Button.inline("- سعر البيع", data="change_sell_price")
                        ],
                        [
                            Button.inline("رجوع ↪️", data="admin_panel")
                        ]
                    ])              
@bot.on(events.CallbackQuery(pattern=b'ajkcoingl'))
async def nuupv_button(event):
    await event.answer(' -  مرحبا بك في قسم الرصيد.')
    await event.edit('**- يمكنك اضافة وخصم رصيد من المستخدمين من هذا القسم  **',
                    buttons=[
                        [
                            Button.inline("- اضافة نقاط ", data="add_coins"),
                            Button.inline("- خصم نقاط", data="del_coins")
                        ],
                        [
                            Button.inline("رجوع ↪️", data="admin_panel")
                        ]
                    ])            

@bot.on(events.CallbackQuery(pattern=b'bbvjls'))
async def nuupv_button(event):
    await event.answer(' - مرحبا بك في قسم الحظر.')
    await event.edit('**يمكنك حظر والغاء حظر مستخدمين من البوت من هذا القسم**',
                    buttons=[
                        [
                            Button.inline("- حظر مستخدم", data="ban"),
                            Button.inline("- الغاء حظر مستخدم", data="unban")
                        ],
                        [
                            Button.inline("رجوع ↪️", data="admin_panel")
                        ]
                    ])       

@bot.on(events.CallbackQuery(pattern=b'shahn'))
async def deposit_menu(event):
    print("Deposit menu called")
    
    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    buttons = [
        [Button.inline('شحن تلقائي', b'chargauto')],
        [Button.inline('شحن مانيوال', b'chargecrypto')],
    ]
    await event.respond('اختر الطريقة المراد شحن حسابك بها \n\n- **شحن تلقائي** : يتم  اضافة الرصيد تلقائي فور ارسال العملات \n- **شحن مانيوال** : يتم اضافة الرصيد بموافقة الادمن', buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b'chargauto'))
async def deposit_menu(event):
    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    if not db.get("auto_charge_enabled"):
        await event.respond("⚠️ الشحن التلقائي معطل حاليًا.")
        return

    buttons = [
        [Button.inline('BTC', b'deposit_BTC')],
        [Button.inline('USDT', b'deposit_USDT')],
        [Button.inline('LTC', b'deposit_LTC')]
    ]
    await event.edit('اختر العملة المراد الإيداع عن طريقها 🪙', buttons=buttons)

@client.on(events.CallbackQuery(data=b'deposit_LTC'))
async def handle_currency_selection(event):
    print("Currency selection handler called")
    currency = event.data.decode().split('_')[1]
    print(f"Selected currency: {currency}")

    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    if currency not in wallet_addresses:
        await event.respond('Currency not supported.')
        return

    try:
        address_info = wallet_addresses[currency]
        address = address_info['address']
        network = address_info['network']

        buttons = [[Button.inline('ارسلت المبلغ ✅', f'enter_txid_{currency}')]]
        message = await event.respond(
            f'ارسل المبلغ الذي تريد ايداعه في حسابك الى العنوان التالي ثم اضغط على زر ارسلت المبلغ 💵\n\n'
            f'🖇 العنوان :\n `{address}`\n\n🪩 الشبكة : `{network}`\n\n'
            f'⏳ وقت العملية : 60:00',
            buttons=buttons
        )

        pending_deposits[event.sender_id] = {
            'currency': currency,
            'address': address,
            'network': network,
            'message_id': message.id
        }

        await start_countdown(event.sender_id, message.id, currency, countdown_time)

    except Exception as e:
        print(f'Error fetching deposit address: {str(e)}')

@client.on(events.CallbackQuery(data=b'deposit_USDT'))
async def handle_currency_selection(event):
    print("Currency selection handler called")
    currency = event.data.decode().split('_')[1]
    print(f"Selected currency: {currency}")

    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    if currency not in wallet_addresses:
        await event.respond('Currency not supported.')
        return

    try:
        address_info = wallet_addresses[currency]
        address = address_info['address']
        network = address_info['network']

        buttons = [[Button.inline('ارسلت المبلغ ✅', f'enter_txid_{currency}')]]
        message = await event.respond(
            f'ارسل المبلغ الذي تريد ايداعه في حسابك الى العنوان التالي ثم اضغط على زر ارسلت المبلغ 💵\n\n'
            f'🖇 العنوان :\n `{address}`\n\n🪩 الشبكة : `{network}`\n\n'
            f'⏳ وقت العملية : 60:00',
            buttons=buttons
        )

        pending_deposits[event.sender_id] = {
            'currency': currency,
            'address': address,
            'network': network,
            'message_id': message.id
        }

        await start_countdown(event.sender_id, message.id, currency, countdown_time)

    except Exception as e:
        print(f'Error fetching deposit address: {str(e)}')
        
@client.on(events.CallbackQuery(data=b'deposit_BTC'))
async def handle_currency_selection(event):
    print("Currency selection handler called")
    currency = event.data.decode().split('_')[1]
    print(f"Selected currency: {currency}")

    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    if currency not in wallet_addresses:
        await event.respond('Currency not supported.')
        return

    try:
        address_info = wallet_addresses[currency]
        address = address_info['address']
        network = address_info['network']

        buttons = [[Button.inline('ارسلت المبلغ ✅', f'enter_txid_{currency}')]]
        message = await event.respond(
            f'ارسل المبلغ الذي تريد ايداعه في حسابك الى العنوان التالي ثم اضغط على زر ارسلت المبلغ 💵\n\n'
            f'🖇 العنوان :\n `{address}`\n\n🪩 الشبكة : `{network}`\n\n'
            f'⏳ وقت العملية : 60:00',
            buttons=buttons
        )

        pending_deposits[event.sender_id] = {
            'currency': currency,
            'address': address,
            'network': network,
            'message_id': message.id
        }

        await start_countdown(event.sender_id, message.id, currency, countdown_time)

    except Exception as e:
        print(f'Error fetching deposit address: {str(e)}')

@bot.on(events.CallbackQuery(pattern=b'enter_txid_'))
async def handle_payment_made(event):
    currency = event.data.decode().split('_')[2] 
    
    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    await event.respond(f'ارسل (TxID) العملية الخاصه بـ {currency}.')
    pending_deposits[event.sender_id]['awaiting_txid'] = True

@bot.on(events.NewMessage())
async def handle_txid_input(event):
    user_id = event.sender_id

    if not is_bot_enabled():
        await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
        return
    
    if user_id in pending_deposits and pending_deposits[user_id].get('awaiting_txid'):
        txid = event.text.strip() 
        currency = pending_deposits[user_id]['currency']

        try:
            transactions_history = binance_client.get_deposit_history(asset=currency)
            found_transaction = False

            for transaction in transactions_history:
                txid_from_api = transaction['txId']
                if txid == txid_from_api:
                    found_transaction = True
                    amount = float(transaction['amount'])
                    status = transaction['status']

                    if status == 1: 
                        await event.respond(
                            f'تم قبول العملية ✅\n\n'
                            f'💸 المبلغ : {amount} {currency}\n'
                            f'⚡ تم اضافة المبلغ الى حسابك ✅'
                        )
                        del pending_deposits[user_id] 
                        return

            if not found_transaction:
                await event.respond('المعاملة غير موجودة أو لم تكتمل بعد. يرجى التحقق من txid أو المحاولة مرة أخرى بعد 15 دقيقة.')
                del pending_deposits[user_id]
                return

        except Exception as e:
            print(f'Error verifying the transaction: {str(e)}')

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @FFJFF5
#====================#

@client.on(events.callbackquery.CallbackQuery())
async def start_lis(event):
    data = event.data.decode('utf-8')
    user_id = event.chat_id
    bans = db.get('bad_guys') if db.exists('bad_guys') else []
    global new_password
    if data == "change_sell_price":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['sell_price']
            if len(row) < 2:
                row.append(Button.inline(text=f"{name} : {price} $", data=f"chs_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f"{name} : {price} $", data=f"chs_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline(text="رجوع ↪️", data="admin_panel")])
        await event.edit("- اختر البلد الذي تريد تغيير سعره \n سعر البيع هو السعر المجاور لاسم الدولة", parse_mode='markdown', buttons=buttons)
        return 
    
    if data.startswith("confirms_broadcast|"):
        message = data.split("|", 1)[1]

        await broadcast_message(event, message)

    if data == "cancel_broadcast":
        await event.respond("❌ | تم إلغاء الإرسال.")
    
    if data.startswith("chs_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"- أرسل الآن سعر البيع الجديد الذي تريد تعيينه لدولة {name}")
            ch = await x.get_response()
            try:
                price = float(ch.text)
            except:
                await x.send_message(f"- الرجاء ارسال السعر ارقام فقط")
                return
            countries = db.get("countries")
            for i in countries:
                if calling_code == i['calling_code']:
                    i['sell_price'] = price
                    db.set("countries", countries)
                    await x.send_message(f"- تم تغيير سعر دولة {name} الى {price}$")
                    return
            await x.send_message(f"- حدث خطأ أثناء تغيير سعر الدولة ❌")
    
    if data.startswith("captcha_"):
        selected_code = data.split("_")[1]
        
        correct_code = db.get(f"captcha_{user_id}")
        
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        if selected_code == correct_code:
            await create_account(event)
        else:
            await event.respond("❌ | الكود غير صحيح! الرجاء المحاولة مرة أخرى.")
            await show_captcha_buttons(event) 
        return
    
    if data == "login":
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        if db.exists(f"user_{user_id}"):
            await event.respond("🔑 | الرجاء إدخال كلمة سر حسابك")
            response = await event.get_response()
            password = response.text
            user_data = db.get(f"user_{user_id}")
            if "password" in user_data and user_data["password"] == password:
                await event.respond("✅ | تم تسجيل الدخول بنجاح")
            else:
                await event.respond("❌ | كلمة السر غير صحيحة")
        else:
            await event.respond("❌ | ليس لديك حساب، الرجاء إنشاء حساب أولاً.")
    
    if data == "create_account":
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
            
        await show_captcha_buttons(event)
    
    if data == "change_code":
        verification_code = generate_verification_code()
        generate_verification_image(verification_code)
        await event.respond("📷 | تم تغيير كود التحقق، الرجاء إدخال الكود الجديد:", file="verification_code.png")
        response = await event.get_response()
        if response.text == verification_code:
            db.set(f"user_{user_id}", {"coins": 0, "id": user_id, "password": "default_password"})
            await event.respond(msgs['START_MESSAGE'].format(user_id, 0), buttons=buttons)
            await event.respond("✅ | تم إنشاء حسابك بنجاح\n\n شكرًا لاستخدامك بوت فوكس.")
        else:
            await event.respond("❌ | كود التحقق غير صحيح!")
    
    if data == "change_price":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['price']
            if len(row) < 2:
                row.append(Button.inline(text=f"{name} : {price} $", data=f"chg_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f"{name} : {price} $", data=f"chg_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline(text="رجوع ↪️", data="admin_panel")])
        await event.edit("- اختر الدولة الذي تريد تغيير سعرها", parse_mode='markdown', buttons=buttons)
        return 
    
    if data.startswith("chg_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"- أرسل الآن السعر الجديد الذي تريد تعيينه لدولة {name}")
            ch = await x.get_response()
            try:
                price = float(ch.text)
            except:
                await x.send_message(f"- ارسل السعر ارقام فقط")
                return
            countries = db.get("countries")
            for i in countries:
                if calling_code == i['calling_code']:
                    i['price'] = price
                    db.set("countries", countries)
                    await x.send_message(f"- تم تغيير سعر دولة {name} الى {price}")
                    return
            await x.send_message(f"- حدث خطأ أثناء تغيير سعر الدولة ❌")
            
    if data == "ttrt":
        countries = db.get("countries") or []

        blockeds = [
            (code['calling_code'], code['name'])
            for code in countries
            if db.get(f"stops_{code['calling_code']}")
        ]

        if not blockeds:
            await event.answer("🚫 لا توجد دول محظورة حاليًا.", alert=True)
            return

        buttons = [
            Button.inline(f"{name}", data=f"selectyu_{calling_code}")
            for calling_code, name in blockeds
        ]

        buttons = [buttons[i:i+2] for i in range(0, len(buttons), 2)]

        buttons.append([Button.inline("🔙 رجوع", data="admin_panel")])

        await event.edit(
            "📋 **قائمة الدول المحظور استقبال أرقام منها**\n\n"
            "- اضغط على زر الدولة للتحكم بها",
            buttons=buttons
        )

    if data.startswith("selectyu_"):
        calling_code = data.replace("selectyu_", "")
        country_name = next(
            (code['name'] for code in db.get("countries") if code['calling_code'] == calling_code),
            None
        )

        if country_name:
            buttons = [
                [Button.inline("تفعيل استقبال الأرقام", data=f"activatery_{calling_code}")],
                [Button.inline("🔙 رجوع", data="ttrt")]
            ]
            await event.edit(
                f"**اختر ما تريد تنفيذه على الدولة المحظورة**\n\n- اسم الدولة : {country_name}\n\n",
                buttons=buttons
            )
        else:
            await event.answer("❌ الدولة غير موجودة في القائمة.", alert=True)

    if data.startswith("activatery_"):
        calling_code = data.replace("activatery_", "")
        country_name = next(
            (code['name'] for code in db.get("countries") if code['calling_code'] == calling_code),
            None
        )

        if country_name:
            db.set(f"stops_{calling_code}", False)
            await event.edit(
                f"✅ **تم تفعيل استقبال الأرقام من دولة {country_name} بنجاح **",
                buttons=[
                    [Button.inline("🔙 رجوع", data="ttrt")]
                ]
            )
        else:
            await event.answer("❌ الدولة غير موجودة في القائمة.", alert=True)
            
    if data == "add_force":
        async with bot.conversation(event.chat_id) as x:
            force = db.get("force")
            await x.send_message(f"- ارسل يوزر او رابط القناة.")
            ch = await x.get_response()
            channel = ch.text.replace('https://t.me/', '').replace('@', '').replace(" ", "")
            if channel in force:
                await x.send_message(f"- هذه القناة مضافة بالفعل.")
                return
            force.append(channel)
            db.set("force", force)
            await x.send_message(f"- تم اضافة القناة للاشتراك الاجباري بنجاح ✅")
            return
            
    if data == "del_force":
        async with bot.conversation(event.chat_id) as x:
            force = db.get("force")
            await x.send_message(f"- ارسل يوزر او رابط القناة المراد حذفها من الاشتراك الاجباري")
            ch = await x.get_response()
            channel = ch.text.replace('https://t.me/', '').replace('@', '').replace(" ", "")
            if channel not in force:
                await x.send_message(f"- هذه القناة غير مضافة بالفعل")
                return
            force.remove(channel)
            db.set("force", force)
            await x.send_message(f"- تم حذف القناة بنجاح 🗑")
            return

    if data == "sell":
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        await event.edit(f"-")
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"• ارسل الان رقم الهاتف الذي تريد بيعه\n• مثال: \n+201211000000")
            ch = await x.get_response()
            phone_number = ch.text.replace("+", "").replace(" ", "")
            if "+" not in ch.text:
                message = "- ارسل رقم الهاتف بشكل صحيح مع +"
                await x.send_message(message)
            else:
                countries = db.get("countries")
                for code in countries:
                    if ch.text.startswith(code['calling_code']):
                        calling_code = code['calling_code']
                        name = code["name"]
                        sell_price = code["sell_price"]
                        
                        if db.exists(f"stops_{calling_code}"): 
                            message = f"- عذراً، غير مسموح ببيع أرقام من دولة {name} ❌"
                            await x.send_message(message)
                            return
                        else:
                            data = f"next_sell:+{phone_number}"
                            await x.send_message(f"تم العثور على الدولة 💎\n\n• الدولة : {name}\n• السعر : {sell_price}")
                            break
                else:
                    message = "- عذراً، غير مسموح ببيع ارقام لهذه الدولة .. راسل المالك لاضافتها ⚠️"
                    await x.send_message(message)
                    return
    
    if isinstance(data, str) and data.startswith("next_sell:"):
        async with bot.conversation(event.chat_id) as x:
            phone_number = data.split(':')[1]
            countries = db.get("countries")
            for code in countries:
                if phone_number.startswith(code['calling_code']):
                    calling_code = code['calling_code']
                    name = code["name"]
                    sell_price = code["sell_price"]
                    
                    if db.exists(f"stops_{calling_code}"): 
                        message = f"- عذراً، غير مسموح ببيع أرقام من دولة {name} ❌"
                        await x.send_message(message)
                        return
                    
                    app = TelegramClient(StringSession(), api_id=API_ID, api_hash=API_HASH)
                    await app.connect()
                    password = None
                    try:
                        code = await app.send_code_request(phone_number)
                    except (ApiIdInvalidError):
                        await x.send_message("ʏᴏᴜʀ **ᴀᴩɪ_ɪᴅ** ᴀɴᴅ **ᴀᴩɪ_ʜᴀsʜ** ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ᴅᴏᴇsɴ'ᴛ ᴍᴀᴛᴄʜ ᴡɪᴛʜ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴩᴩs sʏsᴛᴇᴍ.")
                        return
                    except (PhoneNumberInvalidError):
                        await x.send_message("ᴛʜᴇ **ᴩʜᴏɴᴇ_ɴᴜᴍʙᴇʀ** ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ᴅᴏᴇsɴ'ᴛ ʙᴇʟᴏɴɢ ᴛᴏ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ.")
                        return
                    await x.send_message("- تم ارسال كود التحقق الخاص بك على حسابك على تليجرام.\n\n- ارسل الكود بالتنسيق التالي: 1 2 3 4 5")
                    txt = await x.get_response()
                    code = txt.text.replace(" ", "")
                    try:
                        await app.sign_in(phone_number, code, password=None)
                        string_session = app.session.save()
                        
                        data = {"phone_number": phone_number, "two-step": "لا يوجد", "session": string_session, "password": new_password}
                        accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
                        accounts.append(data)
                        db.set(f"accounts_{calling_code}", accounts)
                        buttons = [
                            [
                                Button.inline("تحقق ✅", data=f"check:{phone_number}:{calling_code}"),
                            ]
                        ]
                        try:
                            session = MangSession.TELETHON_TO_PYROGRAM(string_session)
                            await enable_password(session, new_password)
                        except Exception as a:
                            print(a)
                            pass
                        await event.reply(f"**• تم التحقق من صحة الكود **\n\n- الآن الخطوة التالية هي تسجيل الخروج من جميع جلسات الحساب ماعدا جلسة البوت الأساسية، ثم اضغط زر **تحقق** ", buttons=buttons)
                    
                    except (PhoneCodeInvalidError):
                        await x.send_message("ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs **ᴡʀᴏɴɢ.**")
                        return
                    except (PhoneCodeExpiredError):
                        await x.send_message("ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs **ᴇxᴩɪʀᴇᴅ.**")
                        return
                    except (SessionPasswordNeededError):
                        await x.send_message("- ارسل رمز التحقق بخطوتين الخاص بالحساب")
                        txt = await x.get_response()
                        password = txt.text
                        try:
                            await app.sign_in(password=password)
                        except (PasswordHashInvalidError):
                            await x.send_message("ᴛʜᴇ ᴩᴀssᴡᴏʀᴅ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs �ᴡʀᴏɴɢ.")
                            return
                        string_session = app.session.save()
                        
                        data = {"phone_number": phone_number, "two-step": password, "session": string_session, "password": new_password}
                        accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
                        accounts.append(data)
                        db.set(f"accounts_{calling_code}", accounts)
                        try:
                            session = MangSession.TELETHON_TO_PYROGRAM(string_session)
                            await change_password(session, password, new_password)
                        except:
                            pass
                        buttons = [
                            [
                                Button.inline("تحقق ✅", data=f"check:{phone_number}:{calling_code}"),
                            ]
                        ]
                        await event.reply(f"**• تم التحقق من صحة الكود**\n\n- الآن الخطوة التالية هي تسجيل الخروج من جميع جلسات الحساب ماعدا جلسة البوت الأساسية، ثم اضغط زر **تحقق** ", buttons=buttons)
                    
    if isinstance(data, str) and data.startswith("check:"):
        await event.edit(f"-")
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        async with bot.conversation(event.chat_id) as x:
            phone_number = data.split(':')[1]
            calling_code = data.split(':')[2]
            countries = db.get("countries")
            
            for code in countries:
                if phone_number.startswith(code['calling_code']):
                    calling_code = code['calling_code']
                    name = code["name"]
                    sell_price = code["sell_price"]
                    accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
                    
                    for i in accounts:
                        if phone_number == i["phone_number"]:
                            ses = i["session"]
                            xx = await count_ses(ses)
                            mkk = isinstance(xx, list)
                            
                            if mkk is False:
                                await x.send_message(f"• حدث خطأ ما، رجاء إعادة تسجيل الرقم مرة أخرى\n\n{xx}")
                                return
                            
                            xv = len(xx)
                            
                            if xv == 1:
                                user_accounts_key = f"user_accounts_{event.chat_id}"
                                user_accounts = db.get(user_accounts_key) if db.exists(user_accounts_key) else []
                                user_accounts.append(phone_number)
                                db.set(user_accounts_key, user_accounts)
                                num_accounts = len(user_accounts)
                                
                                message = f"**• تم استلام الرقم بنجاح ✅**\n\nإجمالي حساباتك: {num_accounts}"
                                buttons = [Button.inline("بيع حساب آخر", data="sell")]
                                await event.respond(message, buttons=buttons)
                                
                                update_user_balance(event.chat_id, float(sell_price))
                                
                                await x.send_message(message)
                                
                                admin_message = f"**- قام مستخدم بتسليم حساب إلى البوت.**\n• أي دي المستخدم: {event.chat_id}\n\n- الرقم: {phone_number}\n- الدولة: {name}\n- إجمالي حساباته: {num_accounts}"
                                await client.send_message(admin, admin_message)
                            
                            else:
                                bm = ""
                                for i in xx:
                                    bm += f"• {i}\n"
                                
                                xxx = f"""**• فشل في إكمال عملية التحقق ❌**
        
        - مازالت هناك بعض الجلسات يجب تسجيل الخروج منها.
        
        {bm}
        
        ⚠️- تذكر: قم بحذف جميع الجلسات ماعدا جلسة البوت ثم اضغط **تحقق**"""
                                
                                buttons = [
                                    [
                                        Button.inline("تحقق ✅", data=f"check:{phone_number}:{calling_code}"),
                                    ]
                                ]
                                await x.send_message(xxx, buttons=buttons)
                                
    if data == "set_trust_channel":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"- ارسل معرف او رابط قناة اثباتات التسليم.")
            ch = await x.get_response()
            channel = ch.text.replace('https://t.me/', '').replace('@', '').replace(" ", "")
            try:
                message = "- تم تفعيل قناة اثباتات التسليم بنجاح ✅"
                await client.send_message(channel, message)
            except:
                message = "- حدث خطأ ❌، تأكد من رفع البوت ادمن في قناتك مع صلاحية ارسال الرسائل"
                await x.send_message(message)
                return
            message = "- تم تفعيل قناة اثباتات التسليم بنجاح ✅"
            await x.send_message(message)
            db.set("trust_channel", channel)
                    
    if data == "sharh":
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
            
        await event.edit(
            f"**• مرحبا بك عزيزي في قسم التعليمات والشروط.**\n\n"
            f"• شروط البوت : ↘️\n\n"
            f"- هذا البوت يقوم بجلب حسابات تيليجرام جاهزة.\n"
            f"- البوت لا يتحمل مسؤولية الأرقام في حالة أنها انحظرت او انسرقت، بمعنى البوت لا يتحمل مسؤولية الرقم بعد شرائه.\n"
            f"- فضلاً يرجى عدم استعمال الأرقام في أشياء قد تغضب الله عز وجل أو الانحراف الإسلامي كالإختراقات وغيره.\n\n"
            f"• تعليمات عن كيفية استعمال البوت : ↘️\n\n"
            f"⚠️ - ملاحظة مهمة: هذا البوت مخصص لشراء حسابات تيليجرام جاهزة، بمجرد الضغط على ( ✅ شراء ✅ )، سيتم إعطاؤك رقم، ويتم خصم قيمة الرقم تلقائياً، ولا يمكنك الإلغاء بعد أن يتم الشراء ⚠️.\n\n"
            f"- البوت يوفر حسابات تيليجرام جاهزة\n"
            f"• للاستفسار تواصل معنا:  @FFJFF5 ",
            buttons=[
                [Button.inline("الرجوع", data="bhoht")]
            ]
        )
    
    if data == "bhoht":
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        await event.edit(
            f"**• 👨‍✈️ ⁞ مرحبا بك عزيزي المستخدم**\n"
            f"✅ - في - بوت ارقام صلاح\n"
            f"📮 - لخدمات الحسابات التيلجرام الجاهزة .\n\n"
            f"1⃣ - أكثر من 200 دولة في المخزون مع إضافات جديدة .\n"
            f"2⃣ - سرعة العمل، أرخص بوت لبيع الأرقام الجاهزة \n"
            f"3⃣ - سعر الرقم يبدأ من 0.25 سنت ويحتوي على أكثر دول العالم\n"
            f"4⃣ - يحتوي على الأرقام النادرة .\n\n"
            f"- يرجى بدء الاستخدام بإنشاء حساب، إذا لديك حساب من قبل، قم بالضغط على زر تسجيل الدخول ✅.\n\n"
            f"الإدارة والدعم الفني: @FFJFF5 ",
            buttons=[
                [Button.inline("📌- انشاء حساب.", data="create_account"), Button.inline("✅- تسجيل الدخول.", data="login")],
                [Button.inline("📃- شرح البوت.", data="sharh")],  
                [Button.url("⚠️- فريق الدعم", url="t.me/FFJFF5")],
            ]
        )
    
    if data == "passwd":
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        if db.exists(f"user_{user_id}"):
            user_data = db.get(f"user_{user_id}")
            old_password = user_data.get("password", "غير معروف")
    
            new_ppassword = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    
            user_data["password"] = new_ppassword
            db.set(f"user_{user_id}", user_data)
    
            await event.respond(
                f"✅ | تم تغيير كلمة السر بنجاح!\n\n"
                f"- كلمة السر القديمة: {old_password}\n"
                f"- كلمة السر الجديدة: `{new_ppassword}`"
            )
        else:
            await event.respond("❌ | ليس لديك حساب، الرجاء إنشاء حساب أولاً.")
    
    if data == "SUPEGY":
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        await event.edit(
            "**⚙️| اختر الإعدادات من الأسفل.**",
            buttons=[
                [Button.inline("🔐 تعديل كلمة سر الحساب.", data="passwd")],
                [Button.inline("📊- احصائيات البوت..", data="successful_accounts")],
                [Button.inline("الرجوع", data="main")]
            ]
        )
    
    if data == "successful_accounts":
        successful_accounts_count = db.get("successful_accounts_count") if db.exists("successful_accounts_count") else 0
        await event.edit(
            f"**📈- عدد الأرقام المكتملة: **{successful_accounts_count}",
            buttons=[[Button.inline("رجوع", data="SUPEGY")]]
        )
    
    if data == "transfer":
        user_info = db.get(f"user_{user_id}") if db.exists(f"user_{user_id}") else {"coins": 0, "coind": 0}
        
        await event.edit(
            f"**⚜️ | هنا قائمة تحويل من محفظة السحب الى حسابك في البوت لإستخدام الأموال في الشراء داخل البوت .**\n\n"
            f"➖ الرصيد| {user_info.get('coind', 0)}$",
            buttons=[
                [Button.inline("تحويل الكل", data="transferdr")],
                [Button.inline("الرجوع", data="main")]
            ]
        )
                                                        
    if data == "transferdr":
        user_info = db.get(f"user_{user_id}") if db.exists(f"user_{user_id}") else {"coins": 0, "coind": 0}
        
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        await event.edit(
            f"**❕ هل انت متأكد من تحويل جميع المحفظة للسحب الى حسابك في البوت ؟ حيث انه لا يمكن عكس العملية...**\n\n"
            f"➖ الرصيد| {user_info.get('coind', 0)}$",
            buttons=[
                [Button.inline("✅تأكيد✅", data="trcoind")],
                [Button.inline("الرجوع", data="transfer")]
            ]
        )

    if data == "trcoind":
        coind_balance = get_user_coind(user_id)
        
        user_info = db.get(f"user_{user_id}") if db.exists(f"user_{user_id}") else {"coins": 0, "coind": 0}
        
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        if coind_balance <= 0:
            await event.answer("- رصيدك غير كافي ❗", alert=True)
            return
        
        user_info['coins'] += coind_balance
        db.set(f"user_{user_id}", user_info)
        
        update_user_coind(user_id, 0)
        
        await event.edit(
            f"**- تم تحويل {coind_balance}$ من محفظة السحب إلى حسابك في البوت بنجاح ✅**\n\n"
            f"• رصيدك الآن : {user_info['coins']}$",
            buttons=[
                [Button.inline("الرجوع", data="main")]
            ]
        )
    if data == "add_coins":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"- ارسل ايدي المستخدم الذي تريد اضافة الرصيد له")
            id = await x.get_response()
            if not db.exists(f"user_{id.text}"):
                await x.send_message(f"- لم ينضم للبوت بعد")
                return
            info = db.get(f"user_{id.text}")
            await x.send_message(f"- المستخدم : {id.text}\n- رصيده : {info['coins']} $\n\n- ارسل المبلغ الذي تريد اضافته للمستخدم")
            count = await x.get_response()
            try:
                info['coins'] += float(count.text)
            except:
                await x.send_message(f"- ارسل المبلغ ارقام فقط")
                return
            db.set(f"user_{id.text}", info)
            await x.send_message(f"- تم اضافة الرصيد للمستخدم بنجاح.\n\n- المبلغ : {info['coins']} $")
            message = f"- تم اضافة {count.text}$ الى رصيدك ✅\n\n- رصيدك الان : {info['coins']}$"
            await client.send_message(int(id.text), message)
            return 
    if data == "del_coins":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"- ارسل ايدي المستخدم المراد خصم رصيد منه")
            id = await x.get_response()
            if not db.exists(f"user_{id.text}"):
                await x.send_message(f"- المستخدم لم ينضم للبوت بعد")
                return
            info = db.get(f"user_{id.text}")
            await x.send_message(f"- المستخدم : {id.text}\n- رصيده : {info['coins']} $\n\n- ارسل المبلغ المراد خصمه من رصيد المستخدم")
            count = await x.get_response()
            try:
                info['coins'] -= float(count.text)
            except:
                await x.send_message(f"- ارسل المبلغ ارقام فقط")
                return
            db.set(f"user_{id.text}", info)
            await x.send_message(f"- تم خصم الرصيد بنجاح.\n- الرصيد الان : {info['coins']} $")
            return
        
    if data == "ban":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"- ارسل ايدي المستخدم المراد حظره")
            id = await x.get_response()
            try:
                i = int(id.text)
            except:
                await x.send_message(f"- ارسل ايدي بشكل صحيح")
                return
            bans = db.get('bad_guys') if db.exists('bad_guys') else []
            if id.text in bans:
                await x.send_message(f"- هذا المستخدم محظور بالفعل")
                return
            bans.append(id.text)
            db.set("bad_guys", bans)
            await x.send_message(f"- تم حظر المستخدم من البوت بنجاح.")
            return 
    
    if data == "unban":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"- ارسل ايدي المستخدم المراد الغاء حظره من البوت")
            id = await x.get_response()
            try:
                i = int(id.text)
            except:
                await x.send_message(f"- ارسل ايدي المستخدم بشكل صحيح.")
                return
            bans = db.get('bad_guys') if db.exists('bad_guys') else []
            if id.text not in bans:
                await x.send_message(f"- هذا المستخدم ليس محظور بالفعل")
                return
            bans.remove(id.text)
            db.set("bad_guys", bans)
            await x.send_message(f"- تم الغاء حظر المستخدم بنجاح")
            return 
    
    if data == "wkala":
        user_info = db.get(f"user_{user_id}") if db.exists(f"user_{user_id}") else {"coins": 0, "coind": 0}
    
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        await event.edit(
            f"**- مرحباً بك في قسم الوكلاء، هنا قائمة بوكلاء البوت الذين تم اعتمادهم من الإدارة شخصياً.**\n\n"
            f"✅ يمكنك شحن البوت عبرهم بكل ثقة وأمان، وبضمان من الإدارة رسميًا.\n"
            f"⚠️ في حال لاحظت من أحدهم أي تصرف غير لائق، يرجى إبلاغنا فورًا.",
            buttons=[
                [Button.inline("Abu Fahd", data="#"), Button.url("الدخول للمحادثة", url="t.me/FFJFF5")],
                [Button.inline("رجوع", data="main")],
            ]
        )
    
    if data == "all_of_number":
        countries = db.get("countries")
        count = 0
        keys = db.keys("accounts_%")
        for i in keys:
            count += len(db.get(i[0]))
                          
        return await event.answer(f"- اجمالي الحسابات : {count}.", alert=True)
        
    if data == "main":
        coins = db.get(f"user_{user_id}")["coins"]
        buttons = [
            [
                Button.inline("📲| حسابات تليجرام جاهزه", data="buy"),
            ],
            [
                Button.inline("تسليم حسابات تليجرام جاهزه", data="seller"),
            ],
            [
                Button.url("فريق الدعم", url="t.me/FFJFF5"),
                Button.inline("الوكلاء", data="wkala"),
            ],
            [
                Button.inline("شحن رصيد", data="shahn"),
            ],
            [
                Button.url("الشراء الناجح", url="t.me/A_F_R_OTO_TRA_ST"),
                Button.inline("الاعدادات", data="SUPEGY"),
            ],
            [
                Button.inline("الاحاله الخاص بك", data="referral"),
            ]
        ]
        await event.edit(msgs['START_MESSAGE'].format(event.chat_id, coins), parse_mode='markdown', buttons=buttons)
        return
        
    if data == "admin_panel":
        keyboard = [
            [
                Button.inline("- نسخة احتياطيه  ", data="zip_all"),
            ],
            [
                Button.inline("- اعدادات الارقام ", data="ajxjao"),
            ],
            [
                Button.inline("- قناة الشراء الناجح", data="set_trust_channel"),
            ],
            [
                Button.inline("- الاشتراك الاجباري ", data="ajxkho"), 
                Button.inline("- الادمن ", data="aksgl"), 
            ],
            [
                Button.inline("- البيع والشراء ", data="ajkofgl"),
            ],
            [
                Button.inline("- الرصيد ", data="ajkcoingl"), 
                Button.inline("- الحظر ", data="bbvjls"), 
            ],
            [
                Button.inline("- ايقاف استقبال من دولة", data="stopcountry")
            ],
            [
                Button.inline("- الدول المعطل استلامها ", data="ttrt"),
            ],
            [
                Button.inline("- اذاعة", data="start_broadcast"),
            ],
            [
                Button.inline("- تغيير سعر الاحالة ", data="amubnf"),
            ],
            [
                Button.inline('تعطيل التلقائي', b'disableauto'), 
                Button.inline('تفعيل التلقائي', b'enableauto')
            ],
            [
                Button.inline('تعطيل المانيوال', b'disablemanual'), 
                Button.inline('تفعيل المانيوال', b'enablemanual')
            ],
            [
                Button.inline("- تعيين عنوان المانيوال ", data="setwalletaddress")
            ],
            [
                Button.inline('تعطيل البوت', b'disablebot'), 
                Button.inline('تفعيل البوت', b'enablebot')
            ],
            [
                Button.inline("- حالة البوت ", data="sts")
            ],
        ]
        await event.edit(msgs['ADMIN_MESSAGE'], buttons=keyboard)
        return 
        
    if data == "buy" or data == "back" or data.startswith("page_") or data == "search_country":
        countries = db.get("countries")
    
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        if data == "search_country":
            async with bot.conversation(event.chat_id) as x:
                await x.send_message("🔎 | حسنًا ، يمكنك الآن إرسال أي شيء يشير إلى البلد ... على سبيل المثال رمز الدولة +20.")
                search_code = await x.get_response()
                search_code = search_code.text.strip() 
                
                found_country = None
                for country in countries:
                    if country['calling_code'] == search_code:
                        found_country = country
                        break
            
                if found_country:
                    message_text = (
                        f"- الدولة : {found_country['name']}\n"
                        f"- رمز الدولة : {found_country['calling_code']}\n"
                        f"- سعر الحساب : {found_country['price']} $\n"
                        "------------------------------------------------------"
                    )
                
                    buttons = [
                        [Button.inline("شراء حساب", f"buy_{found_country['calling_code']}_{found_country['name']}_{found_country['price']}")]
                    ]
                
                    await event.edit(message_text, buttons=buttons)
                    return
                else:
                    await event.answer("- هذه الدولة غير موجوده.", alert=True)
                    return
    
        buttons_per_page = 20 
        total_pages = (len(countries) + buttons_per_page - 1) // buttons_per_page
    
        current_page = int(data.split('_')[1]) if data.startswith("page_") else 0
    
        if current_page < 0:
            current_page = 0
        elif current_page >= total_pages:
            current_page = total_pages - 1
    
        start_index = current_page * buttons_per_page
        end_index = start_index + buttons_per_page
        page_countries = countries[start_index:end_index]
    
        buttons = []
        row = []
        for code in page_countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['price']
            if len(row) < 2:
                row.append(Button.inline(text=f"{name} : {price} $", data=f"countries_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f"{name} : {price} $", data=f"countries_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
    
        navigation_buttons = []
    
        if current_page > 0:
            navigation_buttons.append(Button.inline(text="⏪", data=f"page_{current_page - 1}"))
    
        if current_page < total_pages - 1:
            navigation_buttons.append(Button.inline(text="⏩", data=f"page_{current_page + 1}"))
    
        if navigation_buttons:
            buttons.append(navigation_buttons)
    
        buttons.append([Button.inline(text="AUTO 🔍", data="search_country")])
        buttons.append([Button.inline(text="رجوع ↪️", data="main")])
    
        await event.edit(msgs['COUNTRY_LIST'], parse_mode='markdown', buttons=buttons)
        return
        
    if data.startswith("countries_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        coins = db.get(f"user_{user_id}")['coins']
        if float(coins) < float(price):
            return await event.answer("- رصيدك لا يكفي لشراء اي ارقام من هذه الدولة.", alert=True)
        accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
        if accounts == []:
            return await event.answer("- لا توجد أي حسابات في هذه الدولة.", alert=True)
        keyboard = [
            [
                Button.inline("الغاء ❌", data="back"),
                Button.inline("تأكيد ✅", data=f"buy_{calling_code}_{name}_{price}")
            ],
        ]
        await event.edit(msgs['BUY_MESSAGE'].format(name, price), parse_mode='markdown', buttons=keyboard)
        return
        
    if data == "buysr":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['sell_price']
            if len(row) < 2:
                row.append(Button.inline(text=f"{name} : {price} $", data=f"#"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f"{name} : {price} $", data=f"#")]
        if row:
            buttons.append(row)
    
        buttons.append([Button.inline(text="رجوع ↪️", data="seller")])
        await event.edit(msgs['COUNTRY_LIST'], parse_mode='markdown', buttons=buttons)
        return
        
    if data == "delaccount" or data.startswith("paget_"):
        countries = db.get("countries")
    
        buttons_per_page = 10
        total_pages = (len(countries) + buttons_per_page - 1) // buttons_per_page
    
        if data.startswith("paget_"):
            try:
                current_page = int(data.split('_')[3]) 
            except (IndexError, ValueError):
                current_page = 0
        else:
            current_page = 0
    
        if current_page < 0:
            current_page = 0
        elif current_page >= total_pages:
            current_page = total_pages - 1
    
        start_index = current_page * buttons_per_page
        end_index = start_index + buttons_per_page
        page_countries = countries[start_index:end_index]
    
        buttons = []
        row = []
        for code in page_countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['price']
            if len(row) < 2:
                row.append(Button.inline(text=f"{name} : {price} $", data=f"show_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f"{name} : {price} $", data=f"show_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
    
        navigation_buttons = []
    
        if current_page > 0:
            navigation_buttons.append(Button.inline(text="⏪", data=f"paget_{current_page - 1}"))
    
        if current_page < total_pages - 1:
            navigation_buttons.append(Button.inline(text="⏩", data=f"paget_{current_page + 1}"))
    
        if navigation_buttons:
            buttons.append(navigation_buttons)
    
        buttons.append([Button.inline(text="رجوع ↪️", data="admin_panel")])
    
        await event.edit(
            f"- اختر الدولة الذي تريد حذف رقم منها",
            parse_mode='markdown',
            buttons=buttons
        )
        return
    
    if data.startswith("show_") or data.startswith("pagevv_"):
        if data.startswith("show_"):
            calling_code = data.split('_')[1]
            name = data.split('_')[2]
            price = data.split('_')[3]
            current_page = 0
        else:
            calling_code = data.split('_')[2]
            name = data.split('_')[3]
            price = data.split('_')[4]
            current_page = int(data.split('_')[1]) 

        accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
    
        if accounts == []:
            return await event.answer("- There are no accounts in this country.", alert=True)
    
        accounts_per_page = 10  
        total_pages = (len(accounts) + accounts_per_page - 1) // accounts_per_page
    
        if current_page < 0:
            current_page = 0
        elif current_page >= total_pages:
            current_page = total_pages - 1
    
        start_index = current_page * accounts_per_page
        end_index = start_index + accounts_per_page
        page_accounts = accounts[start_index:end_index]
    
        buttons = [
            [Button.inline(f"{count + start_index}: {i['phone_number']}", data=f"v:{i['phone_number']}:{calling_code}:{name}:{price}")]
            for count, i in enumerate(page_accounts, 1)
        ]
    
        navigation_buttons = []
    
        if current_page > 0:
            navigation_buttons.append(Button.inline(text="⏪", data=f"pagevv_{current_page - 1}_{calling_code}_{name}_{price}"))
    
        if current_page < total_pages - 1:
            navigation_buttons.append(Button.inline(text="⏩", data=f"pagevv_{current_page + 1}_{calling_code}_{name}_{price}"))
    
        if navigation_buttons:
            buttons.append(navigation_buttons)
    
        buttons.append([Button.inline("حذف كل الحسابات", data=f"deleteall:{calling_code}:{name}")])
    
        buttons.append([Button.inline("رجوع ↪️", data=f"delaccount")])
    
        await event.edit(
            f"- اليك قائمة بالحسابات المضافة لدولة {name}",
            parse_mode='markdown',
            buttons=buttons
        )
        return
    
    if data.startswith("deleteall"):
        calling_code = data.split(':')[1]
        name = data.split(':')[2]
    
        db.delete(f"accounts_{calling_code}")
    
        await event.answer(f"- هل تريد حذف جميع الحسابات من دولة {name} من البوت ؟.", alert=True)
        await event.edit("- تم حذف جميع الأرقام بنجاح .", buttons=[[Button.inline("رجوع ↪️", data=f"delaccount")]])
        return
        
    if data.startswith("v:"):
        phone_number = data.split(':')[1]
        calling_code = data.split(':')[2]
        name = data.split(':')[3]
        price = data.split(':')[4]
        info = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
        for i in info:
            if i['phone_number'] == phone_number:
                text = f"- الرقم : `{i['phone_number']}`\n- التحقق بخطوتين : `{i['two-step']}`\n\n**• اختر ما تريد فعله في الحساب**"
        keyboard = [
            [
                Button.inline("جلب الكود 💬", data=f"get:{phone_number}:{calling_code}:{name}:{price}"),
            ],
            [
            Button.inline(f"حذف الحساب 🗑", data=f"del:{phone_number}:{calling_code}:{name}"), 
            ],
            [
            Button.inline("رجوع ↪️", data=f"show_{calling_code}_{name}_{price}")
            ]
        ]
        await event.edit(text, parse_mode='markdown', buttons=keyboard)
        return
        
    if data.startswith("del:"):
        phone_number = data.split(':')[1]
        calling_code = data.split(':')[2]
        name = data.split(':')[3]
        text = f"- الرقم : `{phone_number}`\n\n**- هل تريد حذفه من البوت ؟**"
        keyboard = [
            [
            Button.inline("رجوع ↪️", data=f"v:{phone_number}:{calling_code}:{name}"),
            Button.inline("حذف ❌", data=f"del_done:{phone_number}:{calling_code}:{name}")
            ]
        ]
        await event.edit(text, parse_mode='markdown', buttons=keyboard)
        return
        
    if data.startswith("del_done:"):
        phone_number = data.split(':')[1]
        calling_code = data.split(':')[2]
        name = data.split(':')[3]
        keyboard = [
            [
            Button.inline("رجوع ↪️", data="admin_panel")
            ]
        ]
        
        info = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
        for i in info:
            if i['phone_number'] == phone_number:
                info.remove(i)
                db.set(f"accounts_{calling_code}", info)
                await event.edit(f"- تم حذف الرقم بنجاح 🗑", parse_mode='markdown', buttons=keyboard)
                return
        await event.edit(f"- حدث خطأ اثناء حذف الرقم ❌", parse_mode='markdown', buttons=keyboard)
        return 
        
    if data == "add":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['price']
            if len(row) < 2:
                row.append(Button.inline(text=f"{name} : {price} $", data=f"rig_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f"{name} : {price} $", data=f"rig_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline(text="رجوع ↪️", data="main")])
        await event.edit("- اختر دولة الرقم الذي تريد اضافته", parse_mode='markdown', buttons=buttons)
        return 
        
    if data.startswith("rig_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"- أرسل رقم الحساب مع الرمز الدولي +")
            txt = await x.get_response()
            phone_number = txt.text.replace("+", "").replace(" ", "")
            app = TelegramClient(StringSession(), api_id=API_ID, api_hash=API_HASH)
            await app.connect()
            password=None
            try:
                code = await app.send_code_request(phone_number)
            except (ApiIdInvalidError):
                await x.send_message("ʏᴏᴜʀ **ᴀᴩɪ_ɪᴅ** ᴀɴᴅ **ᴀᴩɪ_ʜᴀsʜ** ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ᴅᴏᴇsɴ'ᴛ ᴍᴀᴛᴄʜ ᴡɪᴛʜ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴩᴩs sʏsᴛᴇᴍ.")
                return
            except (PhoneNumberInvalidError):
                await x.send_message("ᴛʜᴇ **ᴩʜᴏɴᴇ_ɴᴜᴍʙᴇʀ** ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ᴅᴏᴇsɴ'ᴛ ʙᴇʟᴏɴɢ ᴛᴏ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ.")
                return
            await x.send_message("- تم ارسال كود تحقق الى الحساب .. ارسله لي\n\n- ارسله هكذا : 1 2 3 4 5")
            txt = await x.get_response()
            code = txt.text.replace(" ", "")
            try:
                await app.sign_in(phone_number, code, password=None)
                string_session = app.session.save()
                data = {"phone_number": phone_number, "two-step": "WevyPython", "session": string_session}
                accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
                accounts.append(data)
                db.set(f"accounts_{calling_code}", accounts)
                await x.send_message(f"- تم اضافة الحساب الى دولة {name}\n- اجمالي حسابات هذه الدولة : {len(accounts)}")
            except (PhoneCodeInvalidError):
                await x.send_message("ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs **ᴡʀᴏɴɢ.**")
                return
            except (PhoneCodeExpiredError):
                await x.send_message("ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs **ᴇxᴩɪʀᴇᴅ.**")
                return
            except (SessionPasswordNeededError):
                await x.send_message("- ارسل التحقق بخطوتين الخاص بالحساب")
                txt = await x.get_response()
                password = txt.text
                try:
                    await app.sign_in(password=password)
                except (PasswordHashInvalidError):
                    await x.send_message("ᴛʜᴇ ᴩᴀssᴡᴏʀᴅ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs ᴡʀᴏɴɢ.")
                    return
                string_session = app.session.save()
                data = {"phone_number": phone_number, "two-step": password, "session": string_session}
                accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
                accounts.append(data)
                db.set(f"accounts_{calling_code}", accounts)
                await x.send_message(f"- تم اضافة الحساب الى دولة {name}\n- اجمالي هحسابات هذه الدولة : {len(accounts)}")
        return 
        
    if data == 'zip_all':
        folder_path = f"./database"
        zip_file_name = f"database.zip"
        zip_file_nam = f"database"
        try:
            shutil.make_archive(zip_file_nam, 'zip', folder_path)
            with open(zip_file_name, 'rb') as zip_file:
                await client.send_file(user_id, zip_file, attributes=[DocumentAttributeFilename(file_name="database.zip")])
            os.remove(zip_file_name)
        except Exception as a:
            print(a)

    if data.startswith("get:"):
        phone_number = data.split(':')[1]
        calling_code = data.split(':')[2]
        name = data.split(':')[3]
        price = data.split(':')[4]
        info = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
        keyboard = [
            [
            Button.inline("رجــوع ↪️", data="main")
            ]
        ]
        for i in info:
            if i['phone_number'] == phone_number:
                code = await get_code(i['session'])
                try:
                    cd = int(code)
                    text = f"**تم جلب كود التحقق ✅**\nالرقم : `{i['phone_number']}`\nتحقق بخطوتين : `@FFJFF5`\n💬 الكود : `{code}`"
                    now = datetime.datetime.now()
                    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    bots = await client.get_me()
                    user_info = await client.get_entity(bots.id)
                    keyboards = [
                        [
                            KeyboardButtonUrl("شراء رقم", url=f"https://t.me/{user_info.username}"),
                        ]
                    ]
                    if db.exists("trust_channel"):
                        await client.send_message(
                            db.get("trust_channel"),
                            msgs['TRUST_MESSAGE'].format(
                                name,
                                f"{phone_number}"[:8],
                                price,
                                f"{user_id}"[:8],
                                code,
                                current_time
                            ),
                            buttons=keyboards,
                            parse_mode="markdown"
                        )

                    app = TelegramClient(StringSession(i['session']), api_id=API_ID, api_hash=API_HASH)
                    await app.connect()
                    await app.log_out()
                    await app.disconnect()

                    info.remove(i)
                    db.set(f"accounts_{calling_code}", info)
                except Exception as a:
                    print(a)
                    text = f"الرقم : `{i['phone_number']}`\nتحقق بخطوتين : `@FFJFF5`\n\nلم يتم العثور على الكود. ❌"
                async with bot.conversation(event.chat_id) as x:
                    await x.send_message(text, buttons=keyboard)
        return
    if data == "add_country":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("- ارسل اسم الدولة بالعلم الخاص بها\n مثال :- مصر 🇪🇬")
            name = await x.get_response()
            await x.send_message(f"- ارسل الرمز الدولي مع + \nمثال\n- +20")
            calling_code = await x.get_response()
            await x.send_message(f"- ارسل سعر شراء المستخدمين من البوت")
            price = await x.get_response()
            try:
                am = float(price.text)
            except:
                await x.send_message(f"- ارسل ارقام فقط")
                return 
            await x.send_message(f"- ارسل سعر شراء البوت من المستخدمين")
            sell_price = await x.get_response()
            
            countries = db.get("countries") or [] 
            countries.append({
                "name": name.text,
                "calling_code": calling_code.text,
                "price": price.text,
                "sell_price": sell_price.text,
            })
            db.set("countries", countries)
        
            await x.send_message(f"- تم اضافة الدولة بنجاح ✅")
        
            bot_info = await bot.get_me()
            bot_username = bot_info.username 
        
            channel_username = "https://t.me/AF_R_O_TO"  
            message_text = (
                f"- {name.text} : {calling_code.text} - ${price.text} < @{bot_username}\n"
                f"------------------------------------------------------\n"
                f"الدولة - {name.text.split(' ')[0]}"
            )
        
            buttons = [[Button.url("شراء رقم", f"https://t.me/{bot_username}")]]
        
            await bot.send_message(
                entity=channel_username,
                message=message_text,
                buttons=buttons
            )
            return
    
    if data == "del_country":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['price']
            if len(row) < 2:
                row.append(Button.inline(text=f"{name} : {price} $", data=f"delete_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f"{name} : {price} $", data=f"delete_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline(text="رجوع ↪️", data="ajxjao")])
        await event.edit("- اختر الدولة الذي تريد حذفها من البوت", parse_mode='markdown', buttons=buttons)
    
    if data.startswith("delete_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        countries = db.get("countries")
        buttons = [
            [
            Button.inline("رجوع ↪️", data="del_country")
            ]
        ]
        for data in countries:
            if data["calling_code"] == calling_code:
                countries.remove(data)
                await event.edit("- تم حذف الدولة من البوت بنجاح ✅", parse_mode='markdown', buttons=buttons)
                db.set("countries", countries)
                return
        await event.edit("- حدث خطأ اثناء حذف الدولة ❌", parse_mode='markdown', buttons=buttons)
        
    if data == "stopcountry":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['price']
            if len(row) < 2:
                row.append(Button.inline(text=f"{name}", data=f"shower_options_{calling_code}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f"{name}", data=f"shower_options_{calling_code}")]
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline(text="رجوع ↪️", data="admin_panel")])
        await event.edit("- اختر الدولة الذي تريد ايقاف استقبال ارقام منها", parse_mode='markdown', buttons=buttons)
    
    if isinstance(data, str) and data.startswith("shower_options_"):
        calling_code = data.split('_')[2] 
        country_name = next((code['name'] for code in db.get("countries") if code['calling_code'] == calling_code), None)
        
        if country_name:
            buttons = [
                [Button.inline(f"إيقاف استلام حسابات", data=f"stops_{calling_code}")],
                [Button.inline("رجوع ↪️", data="del_country")]
            ]
            await event.edit(f"اختر الإجراء الذي تريد تنفيذه على دولة {country_name}:", buttons=buttons)
    
    if isinstance(data, str) and data.startswith("stops_"):
        calling_code = data.split('_')[1] 
        country_name = next((code['name'] for code in db.get("countries") if code['calling_code'] == calling_code), None)
        
        if country_name:
    
            db.set(f"stops_{calling_code}", True)
            await event.edit(f"تم إيقاف استقبال الأرقام من دولة {country_name} ✅")
        
    if data.startswith("buy_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        
        acc = db.get(f"user_{user_id}")
        if float(acc['coins']) < float(price):
            return await event.answer("- رصيدك لا يكفي لشراء حساب من هذه الدولة.", alert=True)
        
        accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
        if not accounts:
            return await event.answer("- لا يوجد حسابات في هذه الدولة", alert=True)
        
        acc['coins'] -= float(price)
        db.set(f"user_{user_id}", acc)
        
        i = random.choice(accounts)
        text = f"- الرقم : `{i['phone_number']}`\n\n**• حاول تسجيل الدخول بالرقم في تطبيق تليجرام ثم اضغط على زر جلب الكود**"
        keyboard = [
            [
                Button.inline("جلب الكود", data=f"get:{i['phone_number']}:{calling_code}:{name}:{price}"),
            ]
        ]
        await event.edit(text, buttons=keyboard)
    if data == "add_admin":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("-ارسل ايدي المستخدم الذي تريد رفعه ادمن في البوت")
            name = await x.get_response()
            try:
                id = int(name.text)
            except:
                return await x.send_message("- ارسل الايدي ارقام فقط")
            admins = db.get("admins")
            if id in admins:
                return await x.send_message("- هذا المستخدم ادمن بالفعل ❗")
            admins.append(id)
            db.set("admins", admins)
            await x.send_message("- تم رفع المستخدم ادمن في البوت ✅")
            
    if data == "del_admin":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("- ارسل ايدي المستخدم المراد تنزيله من الادمنيه")
            name = await x.get_response()
            try:
                id = int(name.text)
            except:
                return await x.send_message("- ارسل الايدي ارقام فقط")
            admins = db.get("admins")
            if id not in admins:
                return await x.send_message("- المستخدم ليس ادمن بالفعل ❗")
            admins.remove(id)
            db.set("admins", admins)
            await x.send_message("- تم تنزيل المستخدم من الادمن بنجاح ✅")

    if data == "referral":
        user_info = db.get(f"user_{user_id}") if db.exists(f"user_{user_id}") else {"coins": 0, "coind": 0}
        
        if not is_bot_enabled():
            await event.edit("⚠️ البوت حاليا تحت الصيانة سيتم اعادة تشغيله في الساعات القادمه")
            return
        
        bot_info = await client.get_me()
        bot_username = bot_info.username
        
        referral_amount = user_info.get("referral_amount", 0.02) 
        
        referral_link = f"https://t.me/{bot_username}?start={user_id}"
        
        await event.edit(
            f"**🤑 ⌯ إربح دولارات الآن مجاناً عبر مشاركة رابط البوت إلى أصدقائك 👥 واحصل على {referral_amount} دولار مقابل كل شخص يقوم بالدخول إلى البوت عبر الرابط الخاص بك ✅.\n\n"
            f"☑️ - رابط الدعوة الخاص بك: \n\n\n"
            f"`{referral_link}`",
            buttons=[
                [Button.inline("رجوع", data="main")]
            ]
        )

async def start_countdown(chat_id, message_id, currency, remaining_time):
    while remaining_time > 0:
        minutes = remaining_time // 60
        seconds = remaining_time % 60

        address = pending_deposits[chat_id]['address']
        network = pending_deposits[chat_id]['network']

        buttons = [[Button.inline('ارسلت المبلغ ✅', f'enter_txid_{currency}')]]
        try:
            await client.edit_message(
                chat_id,
                message_id,
                f'ارسل المبلغ الذي تريد ايداعه في حسابك الى العنوان التالي ثم اضغط على زر ارسلت المبلغ 💵\n\n'
                f'🖇 العنوان :\n `{address}`\n\n🪩 الشبكة : `{network}`\n\n'
                f'⏳ وقت العملية : 60:00',
                buttons=buttons
            )
        except Exception as e:
            print(f"Error updating message: {e}")

        await asyncio.sleep(1)
        remaining_time -= 1

    await client.edit_message(chat_id, message_id, "Time is up. The deposit window has closed.")
    del pending_deposits[chat_id]

async def cancel_start(event):
    user_id = event.chat_id
    coins = db.get(f"user_{user_id}")["coins"]
    buttons = [
        [
            Button.inline("📲| حسابات تليجرام جاهزه", data="buy"),
        ],
        [
            Button.inline("تسليم حسابات تليجرام جاهزه", data="seller"),
        ],
        [
            Button.url("فريق الدعم", url="t.me/FFJFF5 "),
            Button.inline("الوكلاء", data="wkala"),
        ],
        [
            Button.inline("شحن رصيد", data="shahn"),
        ],
        [
            Button.url("الشراء الناجح", url="t.me/taf3ilatbot"),
            Button.inline("الاعدادات", data="SUPEGY"),
        ],
        [
            Button.inline("الاحاله الخاص بك", data="referral"),
        ]
    ]
    await event.reply(msgs['START_MESSAGE'].format(user_id, coins), parse_mode='markdown', buttons=buttons)
    return

async def create_account(event):
    user_id = event.chat_id
    if not db.exists(f"user_{user_id}"):
        db.set(f"user_{user_id}", {"coins": 0, "id": user_id, "password": "default_password"})
        
        await event.respond(msgs['START_MESSAGE'].format(user_id, 0), buttons=buttonsr)
        await event.respond("✅ | تم إنشاء حسابك بنجاح \n\n شكرًا لاستخدامك بوت فوكس.")
    else:
        await event.respond(msgs['START_MESSAGE'].format(user_id, 0), buttons=buttonsr)
        await event.respond("✅ | تم إنشاء حسابك بنجاح \n\n شكرًا لاستخدامك بوت فوكس.")

async def broadcast_message(event, message):
    users = db.keys('user_%') 
    users = [key[0] if isinstance(key, tuple) else key for key in users]

    total_users = len(users)
    success, failed = 0, 0

    progress_message = await event.respond(
        f"📢 **جارٍ اذاعة الرسالة**\n\n"
        f"✅ **تم الإرسال :** {success}\n"
        f"❌ **فشل الإرسال :** {failed}\n\n"
        f"👥 **إجمالي المستخدمين :** {total_users}"
    )

    for index, user_key in enumerate(users):
        user_id = user_key.replace("user_", "") 
        try:
            await client.send_message(int(user_id), message)
            success += 1
        except Exception as e:
            print(f"⚠️ فشل إرسال الرسالة إلى {user_id}: {e}")
            failed += 1

        if index % 10 == 0 or index == total_users - 1:
            await progress_message.edit(
                f"📢 **جارٍ اذاعة الرسالة**\n\n"
                f"✅ **تم الإرسال :** {success}\n"
                f"❌ **فشل الإرسال :** {failed}\n\n"
                f"👥 **إجمالي المستخدمين :** {total_users}"
            )
        await asyncio.sleep(0.1)

    await progress_message.edit(
        f"🎉 **اكتملت عملية الاذاعة**\n\n"
        f"✅ **تم الإرسال :** {success}\n"
        f"❌ **فشل الإرسال :** {failed}\n\n"
        f"👥 **إجمالي المستخدمين :** {total_users}"
    )
    
#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @FFJFF5
#====================#
    
async def count_ses(session):
    api_hash='d00b2a9f2c9b17ee7b25cbac6ef9f1bf'
    api_id=27140514
    try:
        app = TelegramClient(StringSession(session), api_id=API_ID, api_hash=API_HASH)
        await app.connect()
        try:
            resulkt = await app(functele.auth.ResetAuthorizationsRequest())
        except:
            pass
        unauthorized_attempts = await app(GetAuthorizationsRequest())
        listt = []
        for i in unauthorized_attempts.authorizations:
        	mod = listt.append(i.device_model)
        return listt
    except Exception as a:
        print(str(a))
        return str(a)
        
client.run_until_disconnected()

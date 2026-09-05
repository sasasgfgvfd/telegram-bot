import asyncio
import os
import requests
import json
import time
import random
from datetime import datetime
from telethon import TelegramClient, events, Button, functions, types
from telethon.sessions import StringSession
import re 

API_ID = 24188127
API_HASH = 'e0e2a70a885d1497c8feb47815bb3e36'
BOT_TOKEN = '8906845470:AAGjVGgMfuEfmVoqVhdQvVmJcVfNdrGL_F4'


CHANNEL_USERNAME = '@AF_R_O_TO'

user_sessions = {}
user_settings = {}
publishing_status = {}
waiting_for = {}
user_groups = {}
admin_users = {8379531283: True}
banned_users = {}
vip_users = {}
paid_users = {}
auto_replies = {}
clock_users = {}
ai_chat_sessions = {}
broadcast_sessions = {}
welcome_photo = 'https://iili.io/fdqe0g4.md.jpg'

group_creation_settings = {}
custom_buttons = {}
session_files = {}
channel_members = set()

bot = TelegramClient('auto_publisher_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def B1(text):
    return Button.inline(f'{text}', f'btn_{text}'.encode())

def main_keyboard(user_id):
    buttons = []
    
    if user_id in user_sessions:
        buttons.append([B1('تعيين كليشة'), B1('تعيين سليب')])
        buttons.append([B1('بدء النشر'), B1('ايقاف النشر')])
        buttons.append([B1('السوبرات'), B1('اعدادات الرد التلقائي')])
        buttons.append([B1('اوامر الحساب'), B1('اعدادات انشاء الكروبات')])
        buttons.append([B1('معلومات البوت'), B1('قناة السورس')])
        buttons.append([B1('تسجيل خروج')])
        
        if user_id in custom_buttons:
            for btn_text in custom_buttons[user_id].keys():
                buttons.append([B1(btn_text)])
        
        if user_id in admin_users:
            buttons.append([B1('لوحة الادمن')])
    else:
        buttons.append([B1('تسجيل دخول')])
        
    return buttons

def groups_keyboard():
    return [
        [B1('اضف سوبر'), B1('حذف سوبر')],
        [B1('عرض السوبرات')],
        [B1('رجوع')]
    ]

def account_commands_keyboard():
    return [
        [B1('اذاعة بالخاص'), B1('تحدث مع الذكاء الاصطناعي')],
        [B1('مغادرة كل القنوات'), B1('مغادرة كل المجموعات')],
        [B1('نقل اعضاء'), B1('تحميل من قنوات مقيدة')],
        [B1('تفعيل الساعة'), B1('ايقاف الساعة')],
        [B1('رجوع')]
    ]

def auto_reply_keyboard():
    return [
        [B1('اضف كليشة رد'), B1('حذف كليشة رد')],
        [B1('الكلايش'), B1('وقت النشر للكلايش')],
        [B1('تفعيل الرد التلقائي'), B1('ايقاف الرد التلقائي')],
        [B1('رجوع')]
    ]

def group_creation_keyboard():
    return [
        [B1('انشاء يدوي'), B1('انشاء تلقائي')],
        [B1('تعيين عدد رسائل'), B1('اضف رسالة')],
        [B1('حذف رسالة'), B1('المدة بين كل انشاء مجموعة')],
        [B1('المجموعات المنشأة'), B1('رجوع')]
    ]

def admin_keyboard():
    return [
        [B1('قسم VIP'), B1('الاحصائيات')],
        [B1('تفعيل VIP'), B1('حذف VIP')],
        [B1('رفع ادمن'), B1('تنزيل ادمن')],
        [B1('حظر عضو'), B1('فك حظر عضو')],
        [B1('الوضع المدفوع'), B1('الوضع المجاني')],
        [B1('اذاعة للجميع'), B1('تعيين صورة الواجهة')],
        [B1('قسم الازرار'), B1('رسالة الترحيب start')],
        [B1('المشتركين VIP'), B1('الجلسات')],
        [B1('تحقق من الاشتراك'), B1('رجوع')]
    ]

def vip_management_keyboard():
    return [
        [B1('تفعيل VIP'), B1('حذف VIP')],
        [B1('المشتركين VIP'), B1('رجوع')]
    ]

def buttons_management_keyboard():
    return [
        [B1('اضف زر'), B1('تعديل اسم زر')],
        [B1('حذف زر'), B1('عرض الازرار')],
        [B1('رجوع')]
    ]

def sessions_management_keyboard():
    return [
        [B1('جلب ملف الجلسات'), B1('الجلسات النشطة')],
        [B1('فحص الجلسات'), B1('حذف جلسة من البوت')],
        [B1('الجلسات القديمة'), B1('رجوع')]
    ]

async def check_subscription(user_id):
    try:
        user = await bot.get_entity(user_id)
        
        try:
            channel = await bot.get_entity(CHANNEL_USERNAME)
            participants = await bot.get_participants(channel)
            
            member_ids = [participant.id for participant in participants]
            if user_id in member_ids:
                return True
            else:
                return False
        except:
            return False
            
    except Exception as e:
        print(f"خطأ في التحقق من الاشتراك: {e}")
        return False

async def upload_image_to_freeimage(image_path):
    try:
        url = "https://freeimage.host/api/1/upload"
        payload = {
            'key': '6d207e02198a847aa98d0a2a901485a5',
            'action': 'upload',
            'format': 'json'
        }
        
        with open(image_path, 'rb') as f:
            files = {'source': f}
            response = requests.post(url, data=payload, files=files)
        
        if response.status_code == 200:
            result = response.json()
            return result['image']['url']
        else:
            return None
    except Exception as e:
        print(f"خطأ في رفع الصورة: {e}")
        return None

async def W1(event):
    welcome_text = '''
مرحبًا بك في بوت النشر التلقائي من خلال هذا البوت يمكنك تفعيل النشر في جميع الكروبات تلقائيًا .

Developer : @WW_GGW
'''
    
    user_id = event.sender_id
    if user_id not in admin_users and user_id not in vip_users:
        is_subscribed = await check_subscription(user_id)
        if not is_subscribed:
            channel_link = f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
            await event.reply(f'''
يجب عليك الاشتراك في القناة اولاً:
{CHANNEL_USERNAME}
ارسل /start بعد الاشتراك
            ''', buttons=[[B1('تحقق من الاشتراك')]])
            return
    
    try:
        await event.reply(
            file=welcome_photo,
            message=welcome_text,
            buttons=main_keyboard(event.sender_id)
        )
    except:
        await event.reply(
            welcome_text,
            buttons=main_keyboard(event.sender_id)
        )

async def bot_info(event):
    info_text = f'''
معلومات البوت

الاحصائيات:
المستخدمين المسجلين: {len(user_sessions)}
الادمن: {len(admin_users)}
VIP: {len(vip_users)}
المحظورين: {len(banned_users)}

المطور: @WW_GGW
قناة السورس: @x2hdo

البوت متعدد الوظائف:
- النشر التلقائي في المجموعات
- الذكاء الاصطناعي
- ادارة الحسابات
- نظام VIP والادمن
- انشاء المجموعات التلقائي
'''
    await event.reply(info_text, buttons=main_keyboard(event.sender_id))

async def verify_session(session_string, user_id, event):
    try:
        client = TelegramClient(
            StringSession(session_string), 
            API_ID, 
            API_HASH,
            connection_retries=3,
            timeout=30,
            request_retries=2
        )
        
        await asyncio.wait_for(client.start(), timeout=30)
        
        me = await client.get_me()
        user_sessions[user_id] = session_string
        user_settings[user_id] = {
            'message': "مرحباً بالجميع! هذه رسالة نشر تلقائي من البوت",
            'sleep_time': 30
        }
        if user_id not in user_groups:
            user_groups[user_id] = []
        
        await event.reply(f'''
تم تسجيل الدخول بنجاح
باسم: {me.first_name or 'غير معروف'}
username: @{me.username or 'لا يوجد'}

Developer : @WW_GGW
''', buttons=main_keyboard(user_id))
        
        await client.disconnect()
        return True
        
    except asyncio.TimeoutError:
        await event.reply("انتهت مهلة الاتصال راجع نتك")
        return False
        
    except Exception as e:
        error_msg = str(e)
        print(f"خطأ في الجلسة: {error_msg}")
        
        if "AUTH_KEY" in error_msg:
            error_display = "كود الجلسة غير صالح او منتهي"
        elif "Timeout" in error_msg:
            error_display = "خطأ بالسيرفر"
        elif "SESSION_PASSWORD_NEEDED" in error_msg:
            error_display = "حساب بي كلمة مرور"
        else:
            error_display = "جلسة منتهية جددها"
        
        await event.reply(f'''
ماكدرت اسجل دخول: {error_display}
راجع الجلسة .
او استخرج منا @nbv_czbot .
''')
        return False

async def download_restricted_content(user_id, message_link):
    try:
        session_string = user_sessions[user_id]
        client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        await client.start()
        
        if 't.me/' in message_link:
            parts = message_link.split('/')
            channel_username = parts[-2]
            message_id = int(parts[-1])
            
            entity = await client.get_entity(channel_username)
            message = await client.get_messages(entity, ids=message_id)
            
            if message:
                await bot.send_message(user_id, "تم تحميل المحتوى بنجاح:")
                await client.forward_messages(user_id, message)
                await client.disconnect()
                return True
            else:
                await client.disconnect()
                return False
                
    except Exception as e:
        print(f"خطأ في تحميل المحتوى: {e}")
        return False

async def create_group_automatically(user_id):
    try:
        session_string = user_sessions[user_id]
        client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        await client.start()
        
        if user_id not in group_creation_settings:
            group_creation_settings[user_id] = {
                'auto_create': False,
                'messages': [],
                'delay': 60,
                'created_groups': []
            }
        
        settings = group_creation_settings[user_id]
        
        group_title = f"Group {random.randint(1000, 9999)}"
        created_group = await client(functions.channels.CreateChannelRequest(
            title=group_title,
            about="Group created automatically by bot",
            megagroup=True
        ))
        
        group_id = created_group.chats[0].id
        settings['created_groups'].append({
            'title': group_title,
            'id': group_id,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        if settings['messages']:
            for msg in settings['messages']:
                try:
                    await client.send_message(group_id, msg)
                    await asyncio.sleep(2)
                except:
                    continue
        else:
            random_messages = [
                "مرحباً بالجميع",
                "هذه مجموعة جديدة",
                "نتمنى لكم وقتاً ممتعاً",
                "شاركونا بأفكاركم",
                "مجتمع رائع",
                "تفاعلوا مع بعضكم البعض",
                "نرحب بجميع الاعضاء الجدد",
                "مجموعة مفيدة للجميع",
                "لا تترددوا في المشاركة",
                "شكراً للانضمام"
            ]
            for i in range(10):
                try:
                    await client.send_message(group_id, random.choice(random_messages))
                    await asyncio.sleep(2)
                except:
                    continue
        
        await bot.send_message(user_id, f'تم انشاء المجموعة: {group_title}')
        await client.disconnect()
        return True
        
    except Exception as e:
        print(f"خطأ في انشاء المجموعة: {e}")
        return False

async def auto_group_creation_loop(user_id):
    while (user_id in group_creation_settings and 
           group_creation_settings[user_id].get('auto_create', False)):
        
        await create_group_automatically(user_id)
        delay = group_creation_settings[user_id].get('delay', 60)
        await asyncio.sleep(delay)

async def chat_with_ai(message):
    try:
        payload = {"device_id": "32430D60C2DF1529",
                  "order_id": "",
                  "product_id": "",
                  "purchase_token": "",
                  "subscription_id": ""}

        headers = {
            'User-Agent': "Chat Smith Android, Version 4.0.5(1032)",
            'Accept': "application/json",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'x-vulcan-application-id': "com.smartwidgetlabs.chatgpt",
            'x-vulcan-request-id': "9149487891757681852694",
            'content-type': "application/json; charset=utf-8"}
        
        re = requests.post("https://api.vulcanlabs.co/smith-auth/api/v1/token", data=json.dumps(payload), headers=headers).json()
        tok = re["AccessToken"]

        payload = {
            "model": "gpt-4o-mini",
            "user": "32430D60C2DF1529",
            "messages": [{"role": "user", "content": message}],
            "max_tokens": 1000,
            "nsfw_check": True
        }

        headers.update({
            'x-auth-token': "challenge_token",
            'authorization': f"Bearer {tok}",
            'x-vulcan-request-id': "9149487891757681854021",
        })

        res = requests.post("https://api.vulcanlabs.co/smith-v2/api/v7/chat_android", data=json.dumps(payload), headers=headers).json()
        return res["choices"][0]["Message"]["content"]
        
    except Exception as e:
        return f"عذراً، حدث خطأ في الذكاء الاصطناعي: {str(e)}"

async def update_clock(user_id):
    if user_id not in user_sessions:
        return
    
    session_string = user_sessions[user_id]
    client = None
    
    try:
        client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        await client.start()
        
        while clock_users.get(user_id, False):
            current_time = datetime.now().strftime("%H:%M:%S")
            try:
                await client(functions.account.UpdateProfileRequest(
                    first_name=f"{current_time}"
                ))
                await asyncio.sleep(10)
            except Exception as e:
                print(f"خطأ في تحديث الساعة: {e}")
                await asyncio.sleep(30)
                
    except Exception as e:
        print(f"خطأ في الساعة: {e}")
    finally:
        if client:
            await client.disconnect()

async def leave_channels(user_id):
    if user_id not in user_sessions:
        return
    
    session_string = user_sessions[user_id]
    client = None
    
    try:
        client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        await client.start()
        
        dialogs = await client.get_dialogs()
        channels_left = 0
        
        for dialog in dialogs:
            if dialog.is_channel and not dialog.is_group:
                try:
                    await client.delete_dialog(dialog.entity)
                    channels_left += 1
                    await asyncio.sleep(2)
                except Exception as e:
                    continue
        
        await bot.send_message(user_id, f'تم مغادرة {channels_left} قناة')
        
    except Exception as e:
        await bot.send_message(user_id, f'خطأ في مغادرة القنوات: {str(e)}')
    finally:
        if client:
            await client.disconnect()

async def leave_groups(user_id):
    if user_id not in user_sessions:
        return
    
    session_string = user_sessions[user_id]
    client = None
    
    try:
        client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        await client.start()
        
        dialogs = await client.get_dialogs()
        groups_left = 0
        
        for dialog in dialogs:
            if dialog.is_group:
                try:
                    await client.delete_dialog(dialog.entity)
                    groups_left += 1
                    await asyncio.sleep(2)
                except Exception as e:
                    continue
        
        await bot.send_message(user_id, f'تم مغادرة {groups_left} مجموعة')
        
    except Exception as e:
        await bot.send_message(user_id, f'خطأ في مغادرة المجموعات: {str(e)}')
    finally:
        if client:
            await client.disconnect()

async def transfer_members(user_id, source_group, target_group):
    if user_id not in user_sessions:
        return
    
    session_string = user_sessions[user_id]
    client = None
    
    try:
        client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        await client.start()
        
        source_entity = await client.get_entity(source_group)
        target_entity = await client.get_entity(target_group)
        
        all_participants = await client.get_participants(source_entity)
        transferred = 0
        
        for participant in all_participants:
            try:
                await client(functions.channels.InviteToChannelRequest(
                    channel=target_entity,
                    users=[participant]
                ))
                transferred += 1
                await asyncio.sleep(3)
            except Exception as e:
                continue
        
        await bot.send_message(user_id, f'تم نقل {transferred} عضو بنجاح')
        
    except Exception as e:
        await bot.send_message(user_id, f'خطأ في نقل الاعضاء: {str(e)}')
    finally:
        if client:
            await client.disconnect()

async def P1(user_id):
    if user_id not in user_sessions:
        return
    
    session_string = user_sessions[user_id]
    client = None
    
    try:
        client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        await client.start()
        
        await bot.send_message(user_id, "بدء النشر في المجموعات...")
        
        while publishing_status.get(user_id, False):
            if user_id in user_groups and user_groups[user_id]:
                for group in user_groups[user_id]:
                    if not publishing_status.get(user_id, False):
                        break
                    
                    try:
                        await client.send_message(group['id'], user_settings[user_id]['message'])
                        await asyncio.sleep(user_settings[user_id]['sleep_time'])
                    except Exception as e:
                        continue
            
            try:
                dialogs = await client.get_dialogs()
                
                for dialog in dialogs:
                    if not publishing_status.get(user_id, False):
                        break
                    
                    if not (dialog.is_group or dialog.is_channel):
                        continue
                    
                    if user_id in user_groups and any(g['id'] == dialog.entity.id for g in user_groups[user_id]):
                        continue
                    
                    try:
                        if hasattr(dialog.entity, 'title'):
                            await client.send_message(dialog.entity.id, user_settings[user_id]['message'])
                            await asyncio.sleep(user_settings[user_id]['sleep_time'])
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"خطأ في جلب المحادثات: {e}")
                
            if publishing_status.get(user_id, False):
                await asyncio.sleep(60)
                
    except Exception as e:
        await bot.send_message(user_id, f'خطأ في النشر: {str(e)}')
    finally:
        if client:
            await client.disconnect()

@bot.on(events.NewMessage(pattern='/start'))
async def S1(event):
    user_id = event.sender_id
    waiting_for[user_id] = False
    
    # التحقق من الاشتراك
    if user_id not in admin_users and user_id not in vip_users:
        is_subscribed = await check_subscription(user_id)
        if not is_subscribed:
            channel_link = f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
            await event.reply(f'''
يجب عليك الاشتراك في القناة اولاً:
{CHANNEL_USERNAME}

بعد الاشتراك اضغط على زر التحقق:
            ''', buttons=[[B1('تحقق من الاشتراك')]])
            return
    
    await W1(event)

@bot.on(events.NewMessage(pattern='/admin'))
async def admin_command(event):
    user_id = event.sender_id
    if user_id in admin_users:
        admin_info = f'''
لوحة الادمن
اي دي الادمن: {user_id}
يمكنك ادارة البوت من هنا
'''
        await event.reply(admin_info, buttons=admin_keyboard())
    else:
        await event.reply('ليس لديك صلاحية الوصول الى لوحة الادمن')

@bot.on(events.CallbackQuery)
async def C1(event):
    user_id = event.sender_id
    data = event.data.decode('utf-8')
    
    if data == 'btn_تحقق من الاشتراك':
        is_subscribed = await check_subscription(user_id)
        if is_subscribed:
            await event.edit('تم التحقق من اشتراكك بنجاح', buttons=main_keyboard(user_id))
            await W1(event)
        else:
            channel_link = f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
            await event.edit(f'''
لم تشترك بعد في القناة:
{CHANNEL_USERNAME}

يرجى الاشتراك ثم اضغط على زر التحقق:
            ''', buttons=[[B1('تحقق من الاشتراك')]])
    
    elif data == 'btn_تسجيل دخول':
        waiting_for[user_id] = 'session'
        await event.edit('ارسل كود الجلسة:')
        
    elif data == 'btn_تسجيل خروج':
        if user_id in user_sessions:
            publishing_status[user_id] = False
            clock_users.pop(user_id, None)
            ai_chat_sessions.pop(user_id, None)
            broadcast_sessions.pop(user_id, None)
            
            if user_id in group_creation_settings:
                group_creation_settings[user_id]['auto_create'] = False
            
            del user_sessions[user_id]
            if user_id in user_settings:
                del user_settings[user_id]
            if user_id in publishing_status:
                del publishing_status[user_id]
            if user_id in waiting_for:
                del waiting_for[user_id]
            if user_id in user_groups:
                del user_groups[user_id]
                
        await event.edit('تم تسجيل الخروج', buttons=main_keyboard(user_id))
        
    elif data == 'btn_تعيين كليشة':
        if user_id in user_sessions:
            await event.edit('ارسل الكليشة الان:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'message'
            
    elif data == 'btn_تعيين سليب':
        if user_id in user_sessions:
            await event.edit('ارسل وقت السليب (بالثواني):', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'sleep'
            
    elif data == 'btn_بدء النشر':
        if user_id in user_sessions:
            publishing_status[user_id] = True
            await event.edit('تم بدء النشر', buttons=main_keyboard(user_id))
            asyncio.create_task(P1(user_id))
            
    elif data == 'btn_ايقاف النشر':
        if user_id in user_sessions:
            publishing_status[user_id] = False
            await event.edit('تم ايقاف النشر', buttons=main_keyboard(user_id))
            
    elif data == 'btn_السوبرات':
        if user_id in user_sessions:
            await event.edit('ادارة المجموعات:', buttons=groups_keyboard())
            
    elif data == 'btn_اضف سوبر':
        if user_id in user_sessions:
            await event.edit('ارسل رابط المجموعة او المعرف:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'add_group'
            
    elif data == 'btn_حذف سوبر':
        if user_id in user_sessions:
            if user_id not in user_groups or not user_groups[user_id]:
                await event.edit('لا توجد مجموعات مسجلة', buttons=groups_keyboard())
            else:
                groups_list = "\n".join([f"{i+1}. {g['title']}" for i, g in enumerate(user_groups[user_id])])
                await event.edit(f'المجموعات:\n{groups_list}\n\nارسل رقم المجموعة للحذف:', buttons=[[B1('رجوع')]])
                waiting_for[user_id] = 'remove_group'
                
    elif data == 'btn_عرض السوبرات':
        if user_id in user_sessions:
            if user_id not in user_groups or not user_groups[user_id]:
                await event.edit('لا توجد مجموعات مسجلة', buttons=groups_keyboard())
            else:
                groups_list = "\n".join([f"{i+1}. {g['title']} ({g['type']})" for i, g in enumerate(user_groups[user_id])])
                await event.edit(f'المجموعات المسجلة:\n{groups_list}', buttons=groups_keyboard())
                
    elif data == 'btn_رجوع':
        await event.edit('القائمة الرئيسية:', buttons=main_keyboard(user_id))
    
    elif data == 'btn_معلومات البوت':
        await event.edit('جاري جلب المعلومات...')
        await bot_info(event)
        
    elif data == 'btn_قناة السورس':
        await event.edit('قناة السورس: @x2hdo\n\nالمطور: @WW_GGW', buttons=main_keyboard(user_id))
    
    elif data == 'btn_اوامر الحساب':
        if user_id in user_sessions:
            await event.edit('اوامر الحساب:', buttons=account_commands_keyboard())
            
    elif data == 'btn_اذاعة بالخاص':
        if user_id in user_sessions:
            broadcast_sessions[user_id] = True
            await event.edit('ارسل الرسالة للاذاعة بالخاص (ارسل /cancel للالغاء):', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'broadcast'
            
    elif data == 'btn_تحدث مع الذكاء الاصطناعي':
        if user_id in user_sessions:
            ai_chat_sessions[user_id] = True
            await event.edit('مرحباً! يمكنك التحدث مع الذكاء الاصطناعي. ارسل /cancel للالغاء', buttons=[[B1('رجوع')]])
            
    elif data == 'btn_مغادرة كل القنوات':
        if user_id in user_sessions:
            await event.edit('جاري مغادرة جميع القنوات...')
            asyncio.create_task(leave_channels(user_id))
            
    elif data == 'btn_مغادرة كل المجموعات':
        if user_id in user_sessions:
            await event.edit('جاري مغادرة جميع المجموعات...')
            asyncio.create_task(leave_groups(user_id))
            
    elif data == 'btn_نقل اعضاء':
        if user_id in user_sessions:
            await event.edit('ارسل رابط المجموعة المصدر:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'transfer_source'
            
    elif data == 'btn_تحميل من قنوات مقيدة':
        if user_id in user_sessions:
            await event.edit('ارسل رابط الرسالة من القناة المقيدة:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'download_restricted'
            
    elif data == 'btn_تفعيل الساعة':
        if user_id in user_sessions:
            clock_users[user_id] = True
            await event.edit('تم تفعيل الساعة', buttons=account_commands_keyboard())
            asyncio.create_task(update_clock(user_id))
            
    elif data == 'btn_ايقاف الساعة':
        if user_id in user_sessions:
            clock_users[user_id] = False
            await event.edit('تم ايقاف الساعة', buttons=account_commands_keyboard())
    
    elif data == 'btn_اعدادات الرد التلقائي':
        if user_id in user_sessions:
            await event.edit('اعدادات الرد التلقائي:', buttons=auto_reply_keyboard())
            
    elif data == 'btn_اضف كليشة رد':
        if user_id in user_sessions:
            await event.edit('ارسل كليشة الرد التلقائي:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'add_auto_reply'
            
    elif data == 'btn_حذف كليشة رد':
        if user_id in user_sessions:
            if user_id not in auto_replies or not auto_replies[user_id].get('messages', []):
                await event.edit('لا توجد كلايش رد تلقائي', buttons=auto_reply_keyboard())
            else:
                messages_list = "\n".join([f"{i+1}. {msg[:50]}..." for i, msg in enumerate(auto_replies[user_id]['messages'])])
                await event.edit(f'كلايش الرد التلقائي:\n{messages_list}\n\nارسل رقم الكليشة للحذف:', buttons=[[B1('رجوع')]])
                waiting_for[user_id] = 'remove_auto_reply'
                
    elif data == 'btn_الكلايش':
        if user_id in user_sessions:
            if user_id not in auto_replies or not auto_replies[user_id].get('messages', []):
                await event.edit('لا توجد كلايش رد تلقائي', buttons=auto_reply_keyboard())
            else:
                messages_list = "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(auto_replies[user_id]['messages'])])
                await event.edit(f'كلايش الرد التلقائي:\n{messages_list}', buttons=auto_reply_keyboard())
                
    elif data == 'btn_وقت النشر للكلايش':
        if user_id in user_sessions:
            await event.edit('ارسل وقت النشر للكلايش (بالثواني):', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'auto_reply_sleep'
            
    elif data == 'btn_تفعيل الرد التلقائي':
        if user_id in user_sessions:
            if user_id not in auto_replies:
                auto_replies[user_id] = {'active': True, 'messages': [], 'sleep_time': 30}
            else:
                auto_replies[user_id]['active'] = True
            await event.edit('تم تفعيل الرد التلقائي', buttons=auto_reply_keyboard())
            
    elif data == 'btn_ايقاف الرد التلقائي':
        if user_id in user_sessions:
            if user_id in auto_replies:
                auto_replies[user_id]['active'] = False
            await event.edit('تم ايقاف الرد التلقائي', buttons=auto_reply_keyboard())
    
    elif data == 'btn_اعدادات انشاء الكروبات':
        if user_id in user_sessions:
            await event.edit('اعدادات انشاء الكروبات:', buttons=group_creation_keyboard())
            
    elif data == 'btn_انشاء يدوي':
        if user_id in user_sessions:
            await event.edit('جاري انشاء مجموعة يدوياً...')
            await create_group_automatically(user_id)
            
    elif data == 'btn_انشاء تلقائي':
        if user_id in user_sessions:
            if user_id not in group_creation_settings:
                group_creation_settings[user_id] = {
                    'auto_create': True,
                    'messages': [],
                    'delay': 60,
                    'created_groups': []
                }
            else:
                group_creation_settings[user_id]['auto_create'] = True
            
            await event.edit('تم تفعيل الانشاء التلقائي للمجموعات', buttons=group_creation_keyboard())
            asyncio.create_task(auto_group_creation_loop(user_id))
            
    elif data == 'btn_اضف رسالة':
        if user_id in user_sessions:
            await event.edit('ارسل الرسالة التي تريد اضافتها للمجموعات:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'add_group_message'
            
    elif data == 'btn_حذف رسالة':
        if user_id in user_sessions:
            if user_id not in group_creation_settings or not group_creation_settings[user_id].get('messages', []):
                await event.edit('لا توجد رسائل', buttons=group_creation_keyboard())
            else:
                messages_list = "\n".join([f"{i+1}. {msg[:50]}..." for i, msg in enumerate(group_creation_settings[user_id]['messages'])])
                await event.edit(f'الرسائل:\n{messages_list}\n\nارسل رقم الرسالة للحذف:', buttons=[[B1('رجوع')]])
                waiting_for[user_id] = 'remove_group_message'
                
    elif data == 'btn_تعيين عدد رسائل':
        if user_id in user_sessions:
            await event.edit('ارسل عدد الرسائل التي تريد ارسالها في كل مجموعة:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'set_messages_count'
            
    elif data == 'btn_المدة بين كل انشاء مجموعة':
        if user_id in user_sessions:
            await event.edit('ارسل المدة بين كل انشاء مجموعة (بالثواني):', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'set_creation_delay'
            
    elif data == 'btn_المجموعات المنشأة':
        if user_id in user_sessions:
            if user_id not in group_creation_settings or not group_creation_settings[user_id].get('created_groups', []):
                await event.edit('لا توجد مجموعات منشأة', buttons=group_creation_keyboard())
            else:
                groups_list = "\n".join([f"{i+1}. {g['title']} - {g['date']}" for i, g in enumerate(group_creation_settings[user_id]['created_groups'])])
                await event.edit(f'المجموعات المنشأة:\n{groups_list}', buttons=group_creation_keyboard())
    
    elif data == 'btn_لوحة الادمن':
        if user_id in admin_users:
            admin_info = f'لوحة الادمن\nاي دي الادمن: {user_id}'
            await event.edit(admin_info, buttons=admin_keyboard())
            
    elif data == 'btn_قسم VIP':
        if user_id in admin_users:
            await event.edit('قسم VIP:', buttons=vip_management_keyboard())
            
    elif data == 'btn_تفعيل VIP':
        if user_id in admin_users:
            await event.edit('ارسل اي دي المستخدم لتفعيل VIP:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'activate_vip'
            
    elif data == 'btn_حذف VIP':
        if user_id in admin_users:
            await event.edit('ارسل اي دي المستخدم لحذف VIP:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'remove_vip'
            
    elif data == 'btn_المشتركين VIP':
        if user_id in admin_users:
            vip_list = "\n".join([f"{uid}" for uid in vip_users]) if vip_users else "لا يوجد اعضاء VIP"
            await event.edit(f'اعضاء VIP:\n{vip_list}', buttons=vip_management_keyboard())
            
    elif data == 'btn_رفع ادمن':
        if user_id in admin_users:
            await event.edit('ارسل اي دي المستخدم لرفعه ادمن:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'promote_admin'
            
    elif data == 'btn_تنزيل ادمن':
        if user_id in admin_users:
            await event.edit('ارسل اي دي المستخدم لتنزيله من الادمن:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'demote_admin'
            
    elif data == 'btn_حظر عضو':
        if user_id in admin_users:
            await event.edit('ارسل اي دي المستخدم لحظره:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'ban_user'
            
    elif data == 'btn_فك حظر عضو':
        if user_id in admin_users:
            await event.edit('ارسل اي دي المستخدم لفك حظره:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'unban_user'
            
    elif data == 'btn_الاحصائيات':
        if user_id in admin_users:
            stats = f'''
الاحصائيات:
المستخدمين المسجلين: {len(user_sessions)}
الادمن: {len(admin_users)}
VIP: {len(vip_users)}
المحظورين: {len(banned_users)}
المدفوعين: {len(paid_users)}
'''
            await event.edit(stats)
            
    elif data == 'btn_الوضع المدفوع':
        if user_id in admin_users:
            await event.edit('ارسل اي دي المستخدم لتفعيل الوضع المدفوع:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'activate_paid'
            
    elif data == 'btn_الوضع المجاني':
        if user_id in admin_users:
            await event.edit('ارسل اي دي المستخدم الغاء الوضع المدفوع:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'deactivate_paid'
            
    elif data == 'btn_اذاعة للجميع':
        if user_id in admin_users:
            await event.edit('ارسل الرسالة للاذاعة لجميع المستخدمين:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'broadcast_all'
            
    elif data == 'btn_تعيين صورة الواجهة':
        if user_id in admin_users:
            await event.edit('ارسل الصورة الجديدة للواجهة:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'set_welcome_photo'
            
    elif data == 'btn_رسالة الترحيب start':
        if user_id in admin_users:
            await event.edit('ارسل رسالة الترحيب الجديدة:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'set_welcome_message'
            
    elif data == 'btn_قسم الازرار':
        if user_id in admin_users:
            await event.edit('ادارة الازرار:', buttons=buttons_management_keyboard())
            
    elif data == 'btn_اضف زر':
        if user_id in admin_users:
            await event.edit('ارسل نص الزر الجديد:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'add_button'
            
    elif data == 'btn_تعديل اسم زر':
        if user_id in admin_users:
            if not custom_buttons.get(user_id, {}):
                await event.edit('لا توجد ازرار مخصصة', buttons=buttons_management_keyboard())
            else:
                buttons_list = "\n".join([f"{i+1}. {btn}" for i, btn in enumerate(custom_buttons[user_id].keys())])
                await event.edit(f'الازرار الحالية:\n{buttons_list}\n\nارسل رقم الزر لتعديله:', buttons=[[B1('رجوع')]])
                waiting_for[user_id] = 'edit_button_select'
                
    elif data == 'btn_حذف زر':
        if user_id in admin_users:
            if not custom_buttons.get(user_id, {}):
                await event.edit('لا توجد ازرار مخصصة', buttons=buttons_management_keyboard())
            else:
                buttons_list = "\n".join([f"{i+1}. {btn}" for i, btn in enumerate(custom_buttons[user_id].keys())])
                await event.edit(f'الازرار الحالية:\n{buttons_list}\n\nارسل رقم الزر لحذفه:', buttons=[[B1('رجوع')]])
                waiting_for[user_id] = 'delete_button'
                
    elif data == 'btn_عرض الازرار':
        if user_id in admin_users:
            if not custom_buttons.get(user_id, {}):
                await event.edit('لا توجد ازرار مخصصة', buttons=buttons_management_keyboard())
            else:
                buttons_list = "\n".join([f"{btn}" for btn in custom_buttons[user_id].keys()])
                await event.edit(f'الازرار المخصصة:\n{buttons_list}', buttons=buttons_management_keyboard())
            
    elif data == 'btn_الجلسات':
        if user_id in admin_users:
            await event.edit('ادارة الجلسات:', buttons=sessions_management_keyboard())
            
    elif data == 'btn_جلب ملف الجلسات':
        if user_id in admin_users:
            sessions_text = "الجلسات النشطة:\n\n"
            for uid, session in user_sessions.items():
                sessions_text += f"المستخدم: {uid}\n"
                sessions_text += f"الجلسة: {session[:50]}...\n\n"
            
            with open('sessions.txt', 'w', encoding='utf-8') as f:
                f.write(sessions_text)
            
            await event.reply(file='sessions.txt')
            await event.edit('تم ارسال ملف الجلسات', buttons=sessions_management_keyboard())
            
    elif data == 'btn_الجلسات النشطة':
        if user_id in admin_users:
            active_sessions = "\n".join([f"{uid}" for uid in user_sessions.keys()])
            await event.edit(f'الجلسات النشطة:\n{active_sessions}', buttons=sessions_management_keyboard())
            
    elif data == 'btn_فحص الجلسات':
        if user_id in admin_users:
            await event.edit('جاري فحص الجلسات...')
            valid_sessions = 0
            for uid, session in user_sessions.items():
                try:
                    client = TelegramClient(StringSession(session), API_ID, API_HASH)
                    await client.start()
                    await client.get_me()
                    await client.disconnect()
                    valid_sessions += 1
                except:
                    continue
            
            await event.edit(f'الجلسات الصالحة: {valid_sessions}/{len(user_sessions)}', buttons=sessions_management_keyboard())
            
    elif data == 'btn_حذف جلسة من البوت':
        if user_id in admin_users:
            await event.edit('ارسل اي دي المستخدم لحذف جلسته:', buttons=[[B1('رجوع')]])
            waiting_for[user_id] = 'delete_session'
            
    elif data == 'btn_الجلسات القديمة':
        if user_id in admin_users:
            await event.edit('هذه الميزة قيد التطوير', buttons=sessions_management_keyboard())

@bot.on(events.NewMessage)
async def M1(event):
    user_id = event.sender_id
    text = event.text
    
    if text.startswith('/start'):
        return
    
    if text.startswith('/cancel'):
        waiting_for[user_id] = False
        ai_chat_sessions.pop(user_id, None)
        broadcast_sessions.pop(user_id, None)
        await event.reply('تم الالغاء', buttons=main_keyboard(user_id))
        return
    
    if text.startswith('/admin'):
        return
    
    if user_id in banned_users:
        await event.reply('تم حظرك من استخدام البوت')
        return
    
    if ai_chat_sessions.get(user_id):
        await event.reply('جاري التفكير...')
        response = await chat_with_ai(text)
        await event.reply(response)
        return
    
    if waiting_for.get(user_id) == 'broadcast' and broadcast_sessions.get(user_id):
        session_string = user_sessions[user_id]
        client = None
        
        try:
            client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            await client.start()
            
            dialogs = await client.get_dialogs()
            sent = 0
            
            for dialog in dialogs:
                if dialog.is_user and not dialog.entity.bot:
                    try:
                        await client.send_message(dialog.entity.id, text)
                        sent += 1
                        await asyncio.sleep(2)
                    except:
                        continue
            
            await event.reply(f'تم ارسال الرسالة الى {sent} مستخدم')
            broadcast_sessions[user_id] = False
            waiting_for[user_id] = False
            
        except Exception as e:
            await event.reply(f'خطأ في الاذاعة: {str(e)}')
        finally:
            if client:
                await client.disconnect()
        return
    
    if waiting_for.get(user_id) == 'download_restricted':
        success = await download_restricted_content(user_id, text)
        if success:
            await event.reply('تم تحميل المحتوى بنجاح')
        else:
            await event.reply('فشل في تحميل المحتوى')
        waiting_for[user_id] = False
        return
    
    if waiting_for.get(user_id) == 'transfer_source':
        waiting_for[user_id] = 'transfer_target'
        user_settings[user_id]['transfer_source'] = text
        await event.reply('ارسل رابط المجموعة الهدف:', buttons=[[B1('رجوع')]])
        return
        
    elif waiting_for.get(user_id) == 'transfer_target':
        source_group = user_settings[user_id]['transfer_source']
        target_group = text
        await event.reply('جاري نقل الاعضاء...')
        asyncio.create_task(transfer_members(user_id, source_group, target_group))
        waiting_for[user_id] = False
        return
    
    if waiting_for.get(user_id) == 'add_auto_reply':
        if user_id not in auto_replies:
            auto_replies[user_id] = {'messages': [], 'sleep_time': 30, 'active': True}
        auto_replies[user_id]['messages'].append(text)
        waiting_for[user_id] = False
        await event.reply('تم اضافة كليشة الرد التلقائي', buttons=auto_reply_keyboard())
        return
        
    elif waiting_for.get(user_id) == 'remove_auto_reply':
        try:
            index = int(text) - 1
            if user_id in auto_replies and 0 <= index < len(auto_replies[user_id]['messages']):
                removed = auto_replies[user_id]['messages'].pop(index)
                await event.reply(f'تم حذف الكليشة: {removed[:50]}...', buttons=auto_reply_keyboard())
            else:
                await event.reply('رقم غير صحيح', buttons=auto_reply_keyboard())
        except:
            await event.reply('ادخل رقم صحيح', buttons=auto_reply_keyboard())
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'auto_reply_sleep':
        try:
            sleep_time = int(text)
            if user_id not in auto_replies:
                auto_replies[user_id] = {'messages': [], 'sleep_time': sleep_time, 'active': True}
            else:
                auto_replies[user_id]['sleep_time'] = sleep_time
            await event.reply(f'تم تعيين وقت النشر: {sleep_time} ثانية', buttons=auto_reply_keyboard())
        except:
            await event.reply('ادخل رقم صحيح', buttons=auto_reply_keyboard())
        waiting_for[user_id] = False
        return
    
    if waiting_for.get(user_id) == 'add_group_message':
        if user_id not in group_creation_settings:
            group_creation_settings[user_id] = {
                'auto_create': False,
                'messages': [],
                'delay': 60,
                'created_groups': []
            }
        group_creation_settings[user_id]['messages'].append(text)
        await event.reply('تم اضافة الرسالة', buttons=group_creation_keyboard())
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'remove_group_message':
        try:
            index = int(text) - 1
            if (user_id in group_creation_settings and 
                0 <= index < len(group_creation_settings[user_id]['messages'])):
                removed = group_creation_settings[user_id]['messages'].pop(index)
                await event.reply(f'تم حذف الرسالة: {removed[:50]}...', buttons=group_creation_keyboard())
            else:
                await event.reply('رقم غير صحيح', buttons=group_creation_keyboard())
        except:
            await event.reply('ادخل رقم صحيح', buttons=group_creation_keyboard())
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'set_creation_delay':
        try:
            delay = int(text)
            if user_id not in group_creation_settings:
                group_creation_settings[user_id] = {
                    'auto_create': False,
                    'messages': [],
                    'delay': delay,
                    'created_groups': []
                }
            else:
                group_creation_settings[user_id]['delay'] = delay
            await event.reply(f'تم تعيين المدة: {delay} ثانية', buttons=group_creation_keyboard())
        except:
            await event.reply('ادخل رقم صحيح', buttons=group_creation_keyboard())
        waiting_for[user_id] = False
        return
    
    if waiting_for.get(user_id) == 'add_button':
        if user_id not in custom_buttons:
            custom_buttons[user_id] = {}
        custom_buttons[user_id][text] = f"action_{text}"
        await event.reply(f'تم اضافة الزر: {text}', buttons=buttons_management_keyboard())
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'delete_button':
        try:
            index = int(text) - 1
            buttons_list = list(custom_buttons.get(user_id, {}).keys())
            if 0 <= index < len(buttons_list):
                removed_btn = buttons_list[index]
                del custom_buttons[user_id][removed_btn]
                await event.reply(f'تم حذف الزر: {removed_btn}', buttons=buttons_management_keyboard())
            else:
                await event.reply('رقم غير صحيح', buttons=buttons_management_keyboard())
        except:
            await event.reply('ادخل رقم صحيح', buttons=buttons_management_keyboard())
        waiting_for[user_id] = False
        return
    
    if waiting_for.get(user_id) == 'delete_session':
        try:
            target_id = int(text)
            if target_id in user_sessions:
                del user_sessions[target_id]
                await event.reply(f'تم حذف جلسة المستخدم: {target_id}')
            else:
                await event.reply('المستخدم غير موجود')
        except:
            await event.reply('ادخل اي دي صحيح')
        waiting_for[user_id] = False
        return
    
    if waiting_for.get(user_id) == 'activate_vip':
        try:
            target_id = int(text)
            vip_users[target_id] = True
            await event.reply(f'تم تفعيل VIP للمستخدم {target_id}')
        except:
            await event.reply('ادخل اي دي صحيح')
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'remove_vip':
        try:
            target_id = int(text)
            vip_users.pop(target_id, None)
            await event.reply(f'تم حذف VIP للمستخدم {target_id}')
        except:
            await event.reply('ادخل اي دي صحيح')
        waiting_for[user_id] = False
        return
    
    if waiting_for.get(user_id) == 'promote_admin':
        try:
            target_id = int(text)
            admin_users[target_id] = True
            await event.reply(f'تم رفع المستخدم {target_id} الى ادمن')
        except:
            await event.reply('ادخل اي دي صحيح')
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'demote_admin':
        try:
            target_id = int(text)
            admin_users.pop(target_id, None)
            await event.reply(f'تم تنزيل المستخدم {target_id} من الادمن')
        except:
            await event.reply('ادخل اي دي صحيح')
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'ban_user':
        try:
            target_id = int(text)
            banned_users[target_id] = True
            await event.reply(f'تم حظر المستخدم {target_id}')
        except:
            await event.reply('ادخل اي دي صحيح')
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'unban_user':
        try:
            target_id = int(text)
            banned_users.pop(target_id, None)
            await event.reply(f'تم فك حظر المستخدم {target_id}')
        except:
            await event.reply('ادخل اي دي صحيح')
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'activate_paid':
        try:
            target_id = int(text)
            paid_users[target_id] = True
            await event.reply(f'تم تفعيل الوضع المدفوع للمستخدم {target_id}')
        except:
            await event.reply('ادخل اي دي صحيح')
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'deactivate_paid':
        try:
            target_id = int(text)
            paid_users.pop(target_id, None)
            await event.reply(f'تم الغاء الوضع المدفوع للمستخدم {target_id}')
        except:
            await event.reply('ادخل اي دي صحيح')
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'broadcast_all':
        sent = 0
        for uid in user_sessions.keys():
            try:
                await bot.send_message(uid, text)
                sent += 1
                await asyncio.sleep(1)
            except:
                continue
        await event.reply(f'تم ارسال الاذاعة الى {sent} مستخدم')
        waiting_for[user_id] = False
        return
        
    elif waiting_for.get(user_id) == 'set_welcome_photo':
        if event.media:
            file_path = await event.download_media(file='temp_photo.jpg')
            new_url = await upload_image_to_freeimage(file_path)
            if new_url:
                global welcome_photo
                welcome_photo = new_url
                await event.reply('تم تحديث صورة الواجهة بنجاح')
                os.remove(file_path)
            else:
                await event.reply('فشل في رفع الصورة')
        else:
            await event.reply('لم ترسل صورة')
        waiting_for[user_id] = False
        return
        
    if waiting_for.get(user_id) == 'session':
        session_string = text.strip()
        waiting_for[user_id] = False
        await event.reply('جاري التحقق...')
        await verify_session(session_string, user_id, event)
        
    elif waiting_for.get(user_id) == 'message':
        user_settings[user_id]['message'] = text
        waiting_for[user_id] = False
        await event.reply('تم تعيين الكليشة', buttons=main_keyboard(user_id))
        
    elif waiting_for.get(user_id) == 'sleep':
        try:
            sleep_time = int(text)
            if sleep_time < 5:
                await event.reply('الحد الادنى 5 ثواني')
            else:
                user_settings[user_id]['sleep_time'] = sleep_time
                waiting_for[user_id] = False
                await event.reply(f'تم تعيين السليب: {sleep_time} ثانية', buttons=main_keyboard(user_id))
        except:
            await event.reply('ادخل رقم صحيح')
            
    elif waiting_for.get(user_id) == 'add_group':
        group_input = text.strip()
        await event.reply('جاري اضافة المجموعة...')
        
        try:
            session_string = user_sessions[user_id]
            client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            await client.start()
            
            if group_input.startswith('https://t.me/'):
                group_input = group_input.replace('https://t.me/', '')
            
            if group_input.startswith('@'):
                entity = await client.get_entity(group_input)
            else:
                try:
                    entity = await client.get_entity(int(group_input))
                except:
                    entity = await client.get_entity(group_input)
            
            group_info = {
                'id': entity.id,
                'title': getattr(entity, 'title', 'غير معروف'),
                'username': getattr(entity, 'username', ''),
                'type': 'خاصة' if getattr(entity, 'broadcast', False) or not getattr(entity, 'megagroup', False) else 'عامة'
            }
            
            if user_id not in user_groups:
                user_groups[user_id] = []
            
            if not any(g['id'] == group_info['id'] for g in user_groups[user_id]):
                user_groups[user_id].append(group_info)
                await event.reply(f'تم اضافة: {group_info["title"]} ({group_info["type"]})', buttons=groups_keyboard())
            else:
                await event.reply('المجموعة مضافه مسبقاً', buttons=groups_keyboard())
            
            await client.disconnect()
            
        except Exception as e:
            await event.reply(f'فشل اضافة المجموعة: {str(e)}', buttons=groups_keyboard())
            
        waiting_for[user_id] = False
        
    elif waiting_for.get(user_id) == 'remove_group':
        try:
            index = int(text.strip()) - 1
            if user_id in user_groups and 0 <= index < len(user_groups[user_id]):
                removed = user_groups[user_id].pop(index)
                await event.reply(f'تم حذف: {removed["title"]}', buttons=groups_keyboard())
            else:
                await event.reply('رقم غير صحيح', buttons=groups_keyboard())
        except:
            await event.reply('ادخل رقم صحيح', buttons=groups_keyboard())
            
        waiting_for[user_id] = False

print("البوت اشتغل بنجاح...")
print(f"اي دي الادمن: {list(admin_users.keys())}")
bot.run_until_disconnected()
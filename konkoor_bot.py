import datetime
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ChatMemberStatus

# توکن ربات
TOKEN = "8425551486:AAEHPG5ODp4NcoMSK7p7bSetf-EWF-1MDls"

# تاریخ کنکور تجربی ۱۴۰۵ (۱۲ تیر ۱۴۰۵، ساعت ۸ صبح - معادل 3 July 2026 میلادی)
KONKOOR_DATE = datetime.datetime(2026, 7, 3, 8, 0)

# شناسه کانال و گروه (لطفاً با شناسه‌های عددی جایگزین کن)
CHANNEL_ID = "@pershiiyan"  # مثل -1001234567890
MUSIC_GROUP_ID = "@musicpershii"  # مثل -1009876543210

# لیست نکات کنکوری (50 نکته)
TIPS = [
    "📚 هر روز یه مبحث جدید مرور کن تا مطالب تثبیت بشن!",
    "⏰ زمانت رو مدیریت کن و برنامه‌ریزی دقیق داشته باش.",
    "🧠 تست‌زنی منظم سرعت و دقتت رو بالا می‌بره.",
    "💪 به خودت ایمان داشته باش، تو می‌تونی بهترین باشی!",
    "😴 شب قبل از آزمون خوب بخواب تا ذهنت آماده باشه.",
    "⭐ در زیست‌شناسی، نمودارهای ژنتیک رو با دقت تمرین کن.",
    "🚀 شیمی ارگانیک رو با واکنش‌های زنجیره‌ای یاد بگیر.",
    "⭐ فیزیک رو با حل مسئله‌های واقعی زندگی تمرین کن.",
    "📖 فرمول‌های کلیدی ریاضی رو خلاصه کن و مرور کن.",
    "⭐ برای زمین‌شناسی، نقشه‌های زمین‌شناسی رو تحلیل کن.",
    "🚀 هر هفته یک آزمون آزمایشی کامل بده.",
    "⭐ تغذیه سالم و ورزش سبک تمرکزت رو بالا می‌بره.",
    "📖 استرس رو با تنفس عمیق و مدیتیشن کنترل کن.",
    "⭐ کتاب‌های مرجع رو اولویت‌بندی کن.",
    "🚀 مطالعه گروهی با دوستانت انگیزه‌ت رو زیاد می‌کنه.",
    "⭐ اشتباهات تست‌ها رو تحلیل کن و تکرار نکن.",
    "📖 زمان‌بندی مطالعه رو بر اساس ضعف‌هات تنظیم کن.",
    "⭐ ویدیوهای آموزشی رو برای درک بهتر مباحث ببین.",
    "🚀 هر ماه پیشرفتت رو با آزمون‌های قبلی مقایسه کن.",
    "⭐ موفقیت رو تجسم کن تا انگیزه‌ات چند برابر بشه!",
    "📚 در شیمی، جدول تناوبی رو مثل کف دستت حفظ کن.",
    "⏰ تست‌زنی رو زمان‌بندی کن تا سرعتت بیشتر بشه.",
    "🧠 قوانین نیوتن در فیزیک رو با مثال‌های واقعی تمرین کن.",
    "💪 هر روز یه هدف کوچک تعیین کن و بهش برس.",
    "😴 استراحت‌های کوتاه بین مطالعه باعث حفظ تمرکز می‌شه.",
    "⭐ چرخه‌های سلولی در زیست رو با دیاگرام یاد بگیر.",
    "🚀 کتاب‌های کمک‌آموزشی رو هدفمند مطالعه کن.",
    "⭐ مسائل سخت ریاضی رو اول حل کن تا اعتمادبه‌نفست بره بالا.",
    "📖 منابع معتبر رو اولویت بده و هوشمندانه مطالعه کن.",
    "⭐ با دوستان کنکوری تبادل نظر کن تا ایده‌های جدید بگیری.",
    "📚 در زیست، مبحث گوارش رو با شکل‌ها مرور کن.",
    "⭐ واکنش‌های شیمیایی رو با فلش‌کارت یاد بگیر.",
    "🚀 در فیزیک، مبحث نور رو با آزمایش‌های ساده تمرین کن.",
    "⭐ برای ریاضی، تکنیک‌های سریع محاسباتی رو یاد بگیر.",
    "📖 هر شب قبل از خواب یه مبحث کوتاه مرور کن.",
    "⭐ در شیمی، موازنه واکنش‌ها رو بارها تمرین کن.",
    "🚀 تست‌های پرتکرار کنکورهای قبلی رو حل کن.",
    "⭐ در زیست، مبحث قلب و گردش خون رو با انیمیشن یاد بگیر.",
    "📖 برنامه‌ریزی روزانه‌ات رو هر هفته بازبینی کن.",
    "⭐ با یه لبخند به خودت بگو: من می‌تونم کنکور رو بترکونم!",
    "📚 در زیست، مبحث تنفس رو با نمودارهای تنفسی مرور کن.",
    "⭐ در شیمی، مفاهیم اسید و باز رو با مثال‌های واقعی یاد بگیر.",
    "🚀 در فیزیک، مبحث کار و انرژی رو با تست‌های مفهومی تمرین کن.",
    "⭐ برای ریاضی، روابط مثلثاتی رو با شکل بصری حفظ کن.",
    "📖 هر روز یه تست چالش‌برانگیز حل کن.",
    "⭐ در زیست، دستگاه عصبی رو با نقشه‌های مغزی مرور کن.",
    "🚀 در شیمی، ترمودینامیک رو با مثال‌های روزمره یاد بگیر.",
    "⭐ در فیزیک، مبحث الکتریسیته رو با مدارهای ساده تمرین کن.",
    "📖 از اشتباهاتت یادداشت بردار تا پیشرفت کنی.",
    "⭐ با یه برنامه منظم، کنکور رو به یه ماجراجویی تبدیل کن!"
]

# لیست نمونه فایل‌های موزیک از @musicpershii (لطفاً با file_id واقعی جایگزین کن)
MUSIC_FILES = [
    {"title": "آهنگ غمگین ۱", "file_id": "SAMPLE_FILE_ID_1"},
    {"title": "آهنگ غمگین ۲", "file_id": "SAMPLE_FILE_ID_2"},
    {"title": "آهنگ دپ ۳", "file_id": "SAMPLE_FILE_ID_3"},
    {"title": "آهنگ عاشقانه ۴", "file_id": "SAMPLE_FILE_ID_4"},
    {"title": "آهنگ غمگین ۵", "file_id": "SAMPLE_FILE_ID_5"}
]

# ذخیره تنظیمات نوتیفیکیشن کاربران (chat_id: list of frequencies)
user_notifications = {}

async def check_channel_membership(bot, user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        print(f"User {user_id} status: {member.status}")  # برای دیباگ
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER], None
    except Exception as e:
        print(f"Error checking membership for user {user_id}: {e}")  # برای دیباگ
        if "chat not found" in str(e).lower():
            return False, "ربات ادمین کانال نیست یا CHANNEL_ID اشتباهه!"
        elif "user not found" in str(e).lower():
            return False, "شما در کانال عضو نیستید!"
        return False, f"خطای نامشخص: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await update.message.reply_text(
            f"🌟 برای استفاده از ربات، اول باید عضو کانال @pershiiyan بشی! ⭐\n"
            f"لینک: https://t.me/pershiiyan\n"
            f"دلیل خطا: {error_message}\n"
            f"بعد از عضویت، دوباره /start بزن."
        )
        return

    # منوی تعاملی جذاب
    keyboard = [
        [InlineKeyboardButton("⏳ روزشمار کنکور", callback_data="countdown")],
        [InlineKeyboardButton("📖 نکته کنکوری", callback_data="tip")],
        [InlineKeyboardButton("🎵 موزیک جذاب", callback_data="music")],
        [InlineKeyboardButton("🔔 تنظیم نوتیفیکیشن", callback_data="set_notification")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # پیام خوش‌آمدگویی انگیزشی
    await update.message.reply_text(
        "🌟 به ربات روزشمار کنکور تجربی ۱۴۰۵ خوش اومدی! 🚀\n"
        "با من هر روز به موفقیت نزدیک‌تر شو و با موزیک‌های جذاب روحیه‌ت رو تازه کن! 💪\n"
        "دستورات زیر رو امتحان کن:\n"
        "⏳ /countdown: زمان باقی‌مونده تا کنکور\n"
        "📖 /tip: یه نکته کنکوری تصادفی\n"
        "🎵 /music: موزیک‌های جذاب پلی‌لیست\n"
        "🔔 /setnotification: تنظیم نوتیفیکیشن (روزانه، هفتگی، ۱۲ ساعته)\n"
        "═══════\n"
        "ساخته شده توسط https://t.me/pershiiyan ⭐",
        reply_markup=reply_markup
    )

async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await update.message.reply_text(
            f"🌟 برای استفاده، عضو کانال @pershiiyan شو! ⭐\n"
            f"دلیل خطا: {error_message}"
        )
        return

    today = datetime.datetime.now()
    time_left = KONKOOR_DATE - today
    days_left = time_left.days
    hours_left = time_left.seconds // 3600
    minutes_left = (time_left.seconds % 3600) // 60
    seconds_left = time_left.seconds % 60
    
    random_tip = random.choice(TIPS)
    
    if days_left >= 0:
        await update.message.reply_text(
            f"🗓️ **روزشمار کنکور تجربی ۱۴۰۵** 🗓️\n"
            f"═══════\n"
            f"📅 **{days_left} روز**\n"
            f"⏰ **{hours_left} ساعت**\n"
            f"🕒 **{minutes_left} دقیقه**\n"
            f"⏱️ **{seconds_left} ثانیه**\n"
            f"═══════\n"
            f"🗓️ تاریخ کنکور: **۱۲ تیر ۱۴۰۵، ساعت ۸ صبح**\n"
            f"💡 **نکته روز:** {random_tip}\n"
            f"═══════\n"
            f"💪 وقتشه که بدرخشی! 🚀\n"
            f"ساخته شده توسط https://t.me/pershiiyan ⭐"
        )
    else:
        await update.message.reply_text(
            "🎉 کنکور تجربی ۱۴۰۵ تموم شد! حالا وقت برنامه‌ریزی برای آینده‌ست! 🌟\n"
            f"ساخته شده توسط https://t.me/pershiiyan ⭐"
        )

async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await update.message.reply_text(
            f"🌟 برای استفاده، عضو کانال @pershiiyan شو! ⭐\n"
            f"دلیل خطا: {error_message}"
        )
        return

    random_tip = random.choice(TIPS)
    await update.message.reply_text(
        f"📖 **نکته کنکوری:**\n{random_tip}\n"
        f"═══════\n"
        f"ساخته شده توسط https://t.me/pershiiyan ⭐"
    )

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await update.message.reply_text(
            f"🌟 برای استفاده، عضو کانال @pershiiyan شو! ⭐\n"
            f"دلیل خطا: {error_message}"
        )
        return

    # انتخاب تصادفی یک موزیک
    selected_music = random.choice(MUSIC_FILES)
    try:
        # ارسال فایل موزیک با file_id
        await update.message.reply_audio(
            audio=selected_music["file_id"],  # باید file_id واقعی بذاری
            caption=f"🎵 **موزیک جذاب** 🎵\n{random.choice(['لذت ببر! 🖤', 'روحیه‌ت رو تازه کن! 🚀', 'با این موزیک غرق شو! 💪'])}\n═══════\nساخته شده توسط https://t.me/pershiiyan ⭐"
        )
    except Exception as e:
        print(f"Error sending music to {user_id}: {e}")
        await update.message.reply_text(
            f"🎵 **موزیک جذاب** 🎵\n"
            f"متاسفانه خطایی پیش اومد! لطفاً دوباره امتحان کن.\n"
            f"═══════\n"
            f"ساخته شده توسط https://t.me/pershiiyan ⭐"
        )

async def set_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await update.message.reply_text(
            f"🌟 برای استفاده، عضو کانال @pershiiyan شو! ⭐\n"
            f"دلیل خطا: {error_message}"
        )
        return

    keyboard = [
        [InlineKeyboardButton("🔔 روزانه", callback_data="notify_daily")],
        [InlineKeyboardButton("🔔 هفتگی", callback_data="notify_weekly")],
        [InlineKeyboardButton("🔔 ۱۲ ساعته", callback_data="notify_12hour")],
        [InlineKeyboardButton("🔕 غیرفعال", callback_data="notify_off")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔔 **زمان نوتیفیکیشن رو انتخاب کن:**",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.message.chat_id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await query.message.reply_text(
            f"🌟 برای استفاده، عضو کانال @pershiiyan شو! ⭐\n"
            f"دلیل خطا: {error_message}"
        )
        return

    if query.data == "countdown":
        today = datetime.datetime.now()
        time_left = KONKOOR_DATE - today
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        minutes_left = (time_left.seconds % 3600) // 60
        seconds_left = time_left.seconds % 60
        
        random_tip = random.choice(TIPS)
        
        if days_left >= 0:
            await query.message.reply_text(
                f"🗓️ **روزشمار کنکور تجربی ۱۴۰۵** 🗓️\n"
                f"═══════\n"
                f"📅 **{days_left} روز**\n"
                f"⏰ **{hours_left} ساعت**\n"
                f"🕒 **{minutes_left} دقیقه**\n"
                f"⏱️ **{seconds_left} ثانیه**\n"
                f"═══════\n"
                f"🗓️ تاریخ کنکور: **۱۲ تیر ۱۴۰۵، ساعت ۸ صبح**\n"
                f"💡 **نکته روز:** {random_tip}\n"
                f"═══════\n"
                f"💪 وقتشه که بدرخشی! 🚀\n"
                f"ساخته شده توسط https://t.me/pershiiyan ⭐"
            )
        else:
            await query.message.reply_text(
                "🎉 کنکور تجربی ۱۴۰۵ تموم شد! حالا وقت برنامه‌ریزی برای آینده‌ست! 🌟\n"
                f"ساخته شده توسط https://t.me/pershiiyan ⭐"
            )
    
    elif query.data == "tip":
        random_tip = random.choice(TIPS)
        await query.message.reply_text(
            f"📖 **نکته کنکوری:**\n{random_tip}\n"
            f"═══════\n"
            f"ساخته شده توسط https://t.me/pershiiyan ⭐"
        )
    
    elif query.data == "music":
        selected_music = random.choice(MUSIC_FILES)
        try:
            await query.message.reply_audio(
                audio=selected_music["file_id"],  # باید file_id واقعی بذاری
                caption=f"🎵 **موزیک جذاب** 🎵\n{random.choice(['لذت ببر! 🖤', 'روحیه‌ت رو تازه کن! 🚀', 'با این موزیک غرق شو! 💪'])}\n═══════\nساخته شده توسط https://t.me/pershiiyan ⭐"
            )
        except Exception as e:
            print(f"Error sending music to {query.message.chat_id}: {e}")
            await query.message.reply_text(
                f"🎵 **موزیک جذاب** 🎵\n"
                f"متاسفانه خطایی پیش اومد! لطفاً دوباره امتحان کن.\n"
                f"═══════\n"
                f"ساخته شده توسط https://t.me/pershiiyan ⭐"
            )
    
    elif query.data == "set_notification":
        keyboard = [
            [InlineKeyboardButton("🔔 روزانه", callback_data="notify_daily")],
            [InlineKeyboardButton("🔔 هفتگی", callback_data="notify_weekly")],
            [InlineKeyboardButton("🔔 ۱۲ ساعته", callback_data="notify_12hour")],
            [InlineKeyboardButton("🔕 غیرفعال", callback_data="notify_off")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "🔔 **زمان نوتیفیکیشن رو انتخاب کن:**",
            reply_markup=reply_markup
        )
    
    elif query.data in ["notify_daily", "notify_weekly", "notify_12hour", "notify_off"]:
        frequency = query.data.replace("notify_", "")
        if frequency == "off":
            user_notifications[user_id] = []
            await query.message.reply_text("🔕 نوتیفیکیشن‌ها غیرفعال شد!")
        else:
            user_notifications[user_id] = [frequency, "weekly", "monthly"]
            await query.message.reply_text(
                f"🔔 نوتیفیکیشن {frequency} فعال شد!\n"
                f"هفتگی و ماهانه هم خودکار فعال شدن. 🚀"
            )

async def daily_countdown(context: ContextTypes.DEFAULT_TYPE):
    for chat_id, frequencies in user_notifications.items():
        if "daily" in frequencies:
            await send_countdown(context.bot, chat_id)

async def weekly_countdown(context: ContextTypes.DEFAULT_TYPE):
    for chat_id, frequencies in user_notifications.items():
        if "weekly" in frequencies:
            await send_countdown(context.bot, chat_id)

async def twelve_hour_countdown(context: ContextTypes.DEFAULT_TYPE):
    for chat_id, frequencies in user_notifications.items():
        if "12hour" in frequencies:
            await send_countdown(context.bot, chat_id)

async def monthly_countdown(context: ContextTypes.DEFAULT_TYPE):
    for chat_id, frequencies in user_notifications.items():
        if "monthly" in frequencies:
            await send_countdown(context.bot, chat_id)

async def channel_countdown(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.datetime.now()
    time_left = KONKOOR_DATE - today
    days_left = time_left.days
    hours_left = time_left.seconds // 3600
    minutes_left = (time_left.seconds % 3600) // 60
    seconds_left = time_left.seconds % 60
    
    random_tip = random.choice(TIPS)
    
    message = (
        f"🗓️ **روزشمار کنکور تجربی ۱۴۰۵** 🗓️\n"
        f"═══════\n"
        f"📅 **{days_left} روز**\n"
        f"⏰ **{hours_left} ساعت**\n"
        f"🕒 **{minutes_left} دقیقه**\n"
        f"⏱️ **{seconds_left} ثانیه**\n"
        f"═══════\n"
        f"🗓️ تاریخ کنکور: **۱۲ تیر ۱۴۰۵، ساعت ۸ صبح**\n"
        f"💡 **نکته روز:** {random_tip}\n"
        f"═══════\n"
        f"💪 وقتشه که بدرخشی! 🚀\n"
        f"ساخته شده توسط https://t.me/pershiiyan ⭐"
    ) if days_left >= 0 else (
        "🎉 کنکور تجربی ۱۴۰۵ تموم شد! حالا وقت برنامه‌ریزی برای آینده‌ست! 🌟\n"
        f"ساخته شده توسط https://t.me/pershiiyan ⭐"
    )

    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=message)
    except Exception as e:
        print(f"Error sending to channel {CHANNEL_ID}: {e}")

async def send_countdown(bot, chat_id):
    is_member, error_message = await check_channel_membership(bot, chat_id)
    if not is_member:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=f"🌟 برای دریافت نوتیفیکیشن، عضو کانال @pershiiyan شو! ⭐\nدلیل خطا: {error_message}"
            )
        except Exception as e:
            print(f"Error sending membership warning to {chat_id}: {e}")
        return

    today = datetime.datetime.now()
    time_left = KONKOOR_DATE - today
    days_left = time_left.days
    hours_left = time_left.seconds // 3600
    minutes_left = (time_left.seconds % 3600) // 60
    seconds_left = time_left.seconds % 60
    
    random_tip = random.choice(TIPS)
    
    message = (
        f"🗓️ **روزشمار کنکور تجربی ۱۴۰۵** 🗓️\n"
        f"═══════\n"
        f"📅 **{days_left} روز**\n"
        f"⏰ **{hours_left} ساعت**\n"
        f"🕒 **{minutes_left} دقیقه**\n"
        f"⏱️ **{seconds_left} ثانیه**\n"
        f"═══════\n"
        f"🗓️ تاریخ کنکور: **۱۲ تیر ۱۴۰۵، ساعت ۸ صبح**\n"
        f"💡 **نکته روز:** {random_tip}\n"
        f"═══════\n"
        f"💪 وقتشه که بدرخشی! 🚀\n"
        f"ساخته شده توسط https://t.me/pershiiyan ⭐"
    ) if days_left >= 0 else (
        "🎉 کنکور تجربی ۱۴۰۵ تموم شد! حالا وقت برنامه‌ریزی برای آینده‌ست! 🌟\n"
        f"ساخته شده توسط https://t.me/pershiiyan ⭐"
    )

    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Error sending to {chat_id}: {e}")

def main():
    # راه‌اندازی ربات
    application = Application.builder().token(TOKEN).build()

    # ثبت دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("countdown", countdown))
    application.add_handler(CommandHandler("tip", tip))
    application.add_handler(CommandHandler("music", music))
    application.add_handler(CallbackQueryHandler(button))

    # نوتیفیکیشن‌ها
    job_queue = application.job_queue
    if job_queue:
        job_queue.run_daily(
            daily_countdown,
            time=datetime.time(8, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=3, minutes=30)))
        )
        job_queue.run_repeating(
            twelve_hour_countdown,
            interval=datetime.timedelta(hours=12),
            first=datetime.time(8, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=3, minutes=30)))
        )
        job_queue.run_repeating(
            weekly_countdown,
            interval=datetime.timedelta(days=7),
            first=datetime.time(8, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=3, minutes=30)))
        )
        job_queue.run_repeating(
            monthly_countdown,
            interval=datetime.timedelta(days=30),
            first=datetime.time(8, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=3, minutes=30)))
        )
        job_queue.run_repeating(
            channel_countdown,
            interval=datetime.timedelta(hours=12),
            first=datetime.time(8, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=3, minutes=30)))
        )
    else:
        print("JobQueue is not available. Please ensure python-telegram-bot[job-queue] is installed.")

    # شروع ربات
    print("ربات شروع شد...")
    application.run_polling()

if __name__ == "__main__":
    main()

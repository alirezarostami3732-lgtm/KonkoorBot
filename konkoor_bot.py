import datetime
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ChatMemberStatus

# ===========================
# نسخه ربات
BOT_VERSION = "v1.0.3"
# ===========================

# توکن ربات
TOKEN = "8425551486:AAEHPG5ODp4NcoMSK7p7bSetf-EWF-1MDls"

# تاریخ کنکور تجربی ۱۴۰۵ (۱۲ تیر ۱۴۰۵، ساعت ۸ صبح - معادل 3 July 2026 میلادی)
KONKOOR_DATE = datetime.datetime(2026, 7, 3, 8, 0)

# شناسه کانال و گروه
CHANNEL_ID = "@pershiiyan"
MUSIC_GROUP_ID = "@musicpershii"

# لیست نکات کنکوری
TIPS = [
    "📚 هر روز یه مبحث جدید مرور کن تا مطالب تثبیت بشن!",
    "⏰ زمانت رو مدیریت کن و برنامه‌ریزی دقیق داشته باش.",
    "🧠 تست‌زنی منظم سرعت و دقتت رو بالا می‌بره.",
    "💪 به خودت ایمان داشته باش، تو می‌تونی بهترین باشی!",
    "😴 شب قبل از آزمون خوب بخواب تا ذهنت آماده باشه.",
    # ... بقیه نکات همانطور که قبل بود
]

# لیست نمونه فایل‌های موزیک
MUSIC_FILES = [
    {"title": "آهنگ غمگین ۱", "file_id": "SAMPLE_FILE_ID_1"},
    {"title": "آهنگ غمگین ۲", "file_id": "SAMPLE_FILE_ID_2"},
    {"title": "آهنگ دپ ۳", "file_id": "SAMPLE_FILE_ID_3"},
    {"title": "آهنگ عاشقانه ۴", "file_id": "SAMPLE_FILE_ID_4"},
    {"title": "آهنگ غمگین ۵", "file_id": "SAMPLE_FILE_ID_5"}
]

# ذخیره تنظیمات نوتیفیکیشن کاربران
user_notifications = {}

# ==========================================
# چک کردن عضویت در کانال
async def check_channel_membership(bot, user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER], None
    except Exception as e:
        if "chat not found" in str(e).lower():
            return False, "ربات ادمین کانال نیست یا CHANNEL_ID اشتباهه!"
        elif "user not found" in str(e).lower():
            return False, "شما در کانال عضو نیستید!"
        return False, f"خطای نامشخص: {e}"

# ==========================================
# هندلر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await update.message.reply_text(
            f"🌟 برای استفاده از ربات، اول باید عضو کانال {CHANNEL_ID} بشی! ⭐\n"
            f"لینک: https://t.me/pershiiyan\n"
            f"دلیل خطا: {error_message}\n"
            f"بعد از عضویت، دوباره /start بزن."
        )
        return

    keyboard = [
        [InlineKeyboardButton("⏳ روزشمار کنکور", callback_data="countdown")],
        [InlineKeyboardButton("📖 نکته کنکوری", callback_data="tip")],
        [InlineKeyboardButton("🎵 موزیک جذاب", callback_data="music")],
        [InlineKeyboardButton("🔔 تنظیم نوتیفیکیشن", callback_data="set_notification")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🌟 به ربات روزشمار کنکور تجربی ۱۴۰۵ خوش اومدی! 🚀\n"
        f"با من هر روز به موفقیت نزدیک‌تر شو و با موزیک‌های جذاب روحیه‌ت رو تازه کن! 💪\n"
        f"دستورات زیر رو امتحان کن:\n"
        f"⏳ /countdown: زمان باقی‌مونده تا کنکور\n"
        f"📖 /tip: یه نکته کنکوری تصادفی\n"
        f"🎵 /music: موزیک‌های جذاب پلی‌لیست\n"
        f"🔔 /setnotification: تنظیم نوتیفیکیشن (روزانه، هفتگی، ۱۲ ساعته)\n"
        f"═══════\n"
        f"ساخته شده توسط https://t.me/pershiiyan ⭐\n"
        f"نسخه ربات: {BOT_VERSION}",
        reply_markup=reply_markup
    )

# ==========================================
# هندلر /countdown
async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await update.message.reply_text(
            f"🌟 برای استفاده، عضو کانال {CHANNEL_ID} شو! ⭐\n"
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

# ==========================================
# هندلر /tip
async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await update.message.reply_text(
            f"🌟 برای استفاده، عضو کانال {CHANNEL_ID} شو! ⭐\n"
            f"دلیل خطا: {error_message}"
        )
        return

    random_tip = random.choice(TIPS)
    await update.message.reply_text(
        f"📖 **نکته کنکوری:**\n{random_tip}\n"
        f"═══════\n"
        f"ساخته شده توسط https://t.me/pershiiyan ⭐"
    )

# ==========================================
# هندلر /music
async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await update.message.reply_text(
            f"🌟 برای استفاده، عضو کانال {CHANNEL_ID} شو! ⭐\n"
            f"دلیل خطا: {error_message}"
        )
        return

    selected_music = random.choice(MUSIC_FILES)
    try:
        await update.message.reply_audio(
            audio=selected_music["file_id"],
            caption=f"🎵 **موزیک جذاب** 🎵\n{random.choice(['لذت ببر! 🖤','روحیه‌ت رو تازه کن! 🚀','با این موزیک غرق شو! 💪'])}\n"
                    f"═══════\nساخته شده توسط https://t.me/pershiiyan ⭐"
        )
    except Exception as e:
        await update.message.reply_text(
            f"🎵 **موزیک جذاب** 🎵\nمتاسفانه خطایی پیش اومد! لطفاً دوباره امتحان کن.\n"
            f"═══════\nساخته شده توسط https://t.me/pershiiyan ⭐"
        )

# ==========================================
# هندلر /set_notification
async def set_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await update.message.reply_text(
            f"🌟 برای استفاده، عضو کانال {CHANNEL_ID} شو! ⭐\n"
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

# ==========================================
# هندلر CallbackQuery
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id
    bot = context.bot

    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await query.message.reply_text(
            f"🌟 برای استفاده، عضو کانال {CHANNEL_ID} شو! ⭐\n"
            f"دلیل خطا: {error_message}"
        )
        return

    if query.data == "countdown":
        await countdown(query, context)
    elif query.data == "tip":
        await tip(query, context)
    elif query.data == "music":
        await music(query, context)
    elif query.data == "set_notification":
        await set_notification(query, context)
    elif query.data.startswith("notify_"):
        frequency = query.data.replace("notify_", "")
        if frequency == "off":
            user_notifications[user_id] = []
            await query.message.reply_text("🔕 نوتیفیکیشن‌ها غیرفعال شد!")
        else:
            user_notifications[user_id] = [frequency, "weekly", "monthly"]
            await query.message.reply_text(f"🔔 نوتیفیکیشن {frequency} فعال شد!\nهفتگی و ماهانه هم خودکار فعال شدن. 🚀")

# ==========================================
# ارسال خودکار روزشمار
async def send_countdown(bot, chat_id):
    is_member, error_message = await check_channel_membership(bot, chat_id)
    if not is_member:
        try:
            await bot.send_message(chat_id=chat_id, text=f"🌟 برای دریافت نوتیفیکیشن، عضو کانال {CHANNEL_ID} شو! ⭐\nدلیل خطا: {error_message}")
        except:
            pass
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
        f"💡 **نکته روز:** {random_tip}\n"
        f"═══════\n"
        f"💪 وقتشه که بدرخشی! 🚀\n"
        f"ساخته شده توسط https://t.me/pershiiyan ⭐"
    )

    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except:
        pass

# ==========================================
# Main
def main():
    application = Application.builder().token(TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("countdown", countdown))
    application.add_handler(CommandHandler("tip", tip))
    application.add_handler(CommandHandler("music", music))
    application.add_handler(CommandHandler("setnotification", set_notification))
    application.add_handler(CallbackQueryHandler(button))

    # JobQueue مثال: ارسال روزانه به کانال
    job_queue = application.job_queue
    job_queue.run_repeating(
        lambda context: send_countdown(context.bot, CHANNEL_ID),
        interval=datetime.timedelta(hours=24),
        first=datetime.datetime.now()
    )

    print(f"✅ ربات نسخه {BOT_VERSION} شروع شد...")
    application.run_polling()

# ==========================================
if __name__ == "__main__":
    main()

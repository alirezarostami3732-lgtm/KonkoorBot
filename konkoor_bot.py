import datetime
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ChatMemberStatus

# ==========================
# ======== تنظیمات =========
# ==========================
BOT_VERSION = "v1.0.8"
TOKEN = "8425551486:AAEHPG5ODp4NcoMSK7p7bSetf-EWF-1MDls"  # جایگزین کنید
CHANNEL_ID = "https://t.me/pershiiyan"       # جایگزین کنید

# تاریخ کنکور تجربی ۱۴۰۵
KONKOOR_DATE = datetime.datetime(2026, 7, 3, 8, 0)

# لیست نکات کنکوری
TIPS = [
    "📚 هر روز یه مبحث جدید مرور کن تا مطالب تثبیت بشن!",
    "⏰ زمانت رو مدیریت کن و برنامه‌ریزی دقیق داشته باش.",
    "🧠 تست‌زنی منظم سرعت و دقتت رو بالا می‌بره.",
    "💪 به خودت ایمان داشته باش، تو می‌تونی بهترین باشی!",
    "😴 شب قبل از آزمون خوب بخواب تا ذهنت آماده باشه."
]

# نمونه فایل‌های موزیک (فقط file_id باید واقعی شود)
MUSIC_FILES = [
    {"title": "آهنگ غمگین ۱", "file_id": "SAMPLE_FILE_ID_1"},
    {"title": "آهنگ عاشقانه ۲", "file_id": "SAMPLE_FILE_ID_2"}
]

# ذخیره تنظیمات نوتیفیکیشن کاربران
user_notifications = {}

# ==========================
# ======== توابع ===========
# ==========================
async def check_channel_membership(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER], None
    except Exception as e:
        if "chat not found" in str(e).lower():
            return False, "ربات ادمین کانال نیست یا CHANNEL_ID اشتباهه!"
        elif "user not found" in str(e).lower():
            return False, "شما در کانال عضو نیستید!"
        return False, str(e)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot
    is_member, error_message = await check_channel_membership(bot, user_id)
    if not is_member:
        await update.message.reply_text(f"🌟 لطفا عضو کانال شوید! {error_message}")
        return

    keyboard = [
        [InlineKeyboardButton("⏳ روزشمار کنکور", callback_data="countdown")],
        [InlineKeyboardButton("📖 نکته کنکوری", callback_data="tip")],
        [InlineKeyboardButton("🎵 موزیک جذاب", callback_data="music")],
        [InlineKeyboardButton("🔔 تنظیم نوتیفیکیشن", callback_data="set_notification")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🌟 ربات کنکور {BOT_VERSION} شروع شد! 🚀",
        reply_markup=reply_markup
    )

async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.datetime.now()
    time_left = KONKOOR_DATE - today
    days, hours, minutes, seconds = time_left.days, time_left.seconds // 3600, (time_left.seconds % 3600) // 60, time_left.seconds % 60
    tip = random.choice(TIPS)
    await update.message.reply_text(
        f"🗓️ روزشمار کنکور:\n📅 {days} روز\n⏰ {hours} ساعت\n🕒 {minutes} دقیقه\n⏱️ {seconds} ثانیه\n💡 نکته روز: {tip}"
    )

async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(TIPS))

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    music = random.choice(MUSIC_FILES)
    await update.message.reply_audio(audio=music["file_id"], caption=f"🎵 {music['title']}")

async def set_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔔 روزانه", callback_data="notify_daily")],
        [InlineKeyboardButton("🔔 هفتگی", callback_data="notify_weekly")],
        [InlineKeyboardButton("🔔 ۱۲ ساعته", callback_data="notify_12hour")],
        [InlineKeyboardButton("🔕 غیرفعال", callback_data="notify_off")]
    ]
    await update.message.reply_text("🔔 زمان نوتیفیکیشن:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id
    data = query.data

    if data.startswith("notify_"):
        freq = data.replace("notify_", "")
        if freq == "off":
            user_notifications[user_id] = []
            await query.message.reply_text("🔕 نوتیفیکیشن‌ها غیرفعال شد!")
        else:
            user_notifications[user_id] = [freq]
            await query.message.reply_text(f"🔔 نوتیفیکیشن {freq} فعال شد!")

# ==========================
# ======== JobQueue =========
# ==========================
async def send_countdown(bot, chat_id):
    today = datetime.datetime.now()
    time_left = KONKOOR_DATE - today
    days, hours, minutes, seconds = time_left.days, time_left.seconds // 3600, (time_left.seconds % 3600) // 60, time_left.seconds % 60
    tip = random.choice(TIPS)
    await bot.send_message(chat_id=chat_id, text=f"🗓️ روزشمار:\n📅 {days} روز\n⏰ {hours} ساعت\n🕒 {minutes} دقیقه\n⏱️ {seconds} ثانیه\n💡 نکته روز: {tip}")

async def daily_job(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in user_notifications:
        if "daily" in user_notifications[chat_id]:
            await send_countdown(context.bot, chat_id)

async def channel_job(context: ContextTypes.DEFAULT_TYPE):
    await send_countdown(context.bot, CHANNEL_ID)

# ==========================
# ======== Main ===========
# ==========================
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("countdown", countdown))
    app.add_handler(CommandHandler("tip", tip))
    app.add_handler(CommandHandler("music", music))
    app.add_handler(CallbackQueryHandler(button))

    # JobQueue
    jobq = app.job_queue
    jobq.run_daily(daily_job, time=datetime.time(8, 0))
    jobq.run_repeating(channel_job, interval=datetime.timedelta(hours=12), first=datetime.time(8, 0))

    print(f"ربات KonkoorBot {BOT_VERSION} شروع شد!")
    app.run_polling()

if __name__ == "__main__":
    main()

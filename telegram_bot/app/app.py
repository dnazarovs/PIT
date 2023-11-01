import logging, requests, json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from datetime import datetime

# Constants
TOKEN = '6896759918:AAELCJsCVtDz8xLSwLb4g12XyFkuDKoZUWE'

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Starts a conversation
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Schedule", callback_data="schedule")],
        [InlineKeyboardButton("User", callback_data="user")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Welcome to NP calendar",
                                   reply_markup=reply_markup)


# Handle button clicks
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()

    if query.data == "schedule":
        await schedule(update, context)
    elif query.data == "user":
        await user(update, context)
    else:
        await schedule_params(update, context, query.data)


# Gets user info
async def user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    source = update.message or update.callback_query
    u = source.from_user
    user_text = f'<b>First Name:</b> {u.first_name}\n'
    user_text += f'<b>Last Name:</b> {u.last_name}\n'
    user_text += f'<b>Username:</b> {u.username}\n'
    user_text += f'<b>ID:</b> {u.id}\n'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=user_text, parse_mode=ParseMode.HTML)


# Gets list of events
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1 day", callback_data="1")],
        [InlineKeyboardButton("2 days", callback_data="2")],
        [InlineKeyboardButton("3 days", callback_data="3")],
        [InlineKeyboardButton("1 week", callback_data="4")],
        [InlineKeyboardButton("2 weeks", callback_data="5")],
        [InlineKeyboardButton("1 month", callback_data="6")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="What period?", reply_markup=reply_markup)


async def schedule_params(update: Update, context: ContextTypes.DEFAULT_TYPE, day_type):
    # Get list of events
    schedule_json = requests.get(f'http://159.223.29.15:5000/schedule/{day_type}').content

    # Load the JSON string into a dictionary
    schedule_dict = json.loads(schedule_json)

    # Get all events
    schedule_text = ''
    for date, events in schedule_dict.items():
        # Get weekday name
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        weekday = date_obj.strftime("%A")

        # Add weekday and date
        schedule_text += f'\n<b><u>{weekday}</u></b> {date}\n'
        for event in events:
            # Add event time and description
            schedule_text += f"• <b>{event['t_start']} - {event['t_end']}</b>\n"
            schedule_text += f"{event['lecture']}\n\n"

    # Create keyboard inline buttons
    keyboard = [
        [InlineKeyboardButton("Schedule", callback_data="schedule")],
        [InlineKeyboardButton("User", callback_data="user")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the events
    await context.bot.send_message(chat_id=update.effective_chat.id, text=schedule_text, parse_mode=ParseMode.HTML,
                                   reply_markup=reply_markup)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    userf_handler = CommandHandler('user', user)
    schedule_handler = CommandHandler('schedule', schedule)
    button_handler = CallbackQueryHandler(button)

    application.add_handler(start_handler)
    application.add_handler(userf_handler)
    application.add_handler(schedule_handler)
    application.add_handler(button_handler)

    application.run_polling()
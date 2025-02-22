import logging
import configparser
import asyncio
from pathlib import Path
from uuid import uuid4
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    InlineQueryHandler,
    filters,
)
from denodo_wrapper import upload_file, DenodoAPI
from file_validator import csv_is_valid


# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Command Handlers
async def start(update, context):
    """Send a welcome message when the /start command is issued."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Welcome to our bot!"
    )

async def query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /query command in Telegram"""

    if not context.args:
        await update.message.reply_text("❌ Please provide a question.")
        return

    question_text = ' '.join(context.args)
    await update.message.reply_text("Querying Denodo... Please be patient, as its speed is beyond our control 🥲.")

    try:
        denodo_client = DenodoAPI(base_url="http://localhost:8008", username="admin", password="admin")
        
        response = await asyncio.to_thread(denodo_client.answer_question, question_text)
        
        answer = response.get("answer", "No answer found.")
    
    except asyncio.TimeoutError:
        answer = "⏳ API took too long to respond. Try again later."
    
    except Exception as e:
        answer = f"Error: {str(e)}"

    await update.message.reply_text(answer)

async def inline_caps(update, context):
    """Handle inline queries to convert text to uppercase."""
    query = update.inline_query.query
    if not query:
        return
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper()),
        )
    ]
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def help_message(update, context):
    """Print help every time unknown command or no command is sent"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Help message. TODO: update" # TODO: update help message
    )

async def attachment(update, context):
    download_path = context.bot_data.get("download_path")
    denodo_repository_path = context.bot_data.get("denodo_repository_path")

    message = update.message
    attachment = message.effective_attachment

    if not attachment:
        await message.reply_text("No attachment found")
        return

    # If the attachment is a list (e.g. for photos), select the largest size.
    if isinstance(attachment, (list, tuple)):
        file_obj = attachment[-1]
    else:
        file_obj = attachment

    new_file = await file_obj.get_file()
    
    file_name = getattr(message.document, 'file_name', None) or f"file_{new_file.file_id}"
    file_path = download_path / file_name

    file_path.parent.mkdir(parents=True, exist_ok=True)

    await new_file.download_to_drive(custom_path=file_path)

    if not csv_is_valid(file_path):
        await message.reply_text("The uploaded file is not a valid CSV.")
        return

    await message.reply_text("Uploading CSV. This could take a while... When ready, we will notify you :)")
    # Using asyncio because denodo_wrapper is a blocking library
    upload_success = await asyncio.to_thread(upload_file, file_path, denodo_repository_path)


    if upload_success:
        await message.reply_text("File uploaded successfully.")
    else:
        await message.reply_text("File upload failed.")

async def unknown(update, context):
    """Inform the user that the command is unknown."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command."
    )

def parse_config(config_file="bot.conf"):
    """Read and return the bot config from the configuration file."""
    config = {}

    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)

    try:
        config["token"] = config_parser["telegram"]["token"]
        config["download_path"] = Path(config_parser["telegram"]["download_path"])
        config["denodo_repository_path"] = Path(config_parser["telegram"]["denodo_repository_path"])
    except KeyError as e:
        logger.error(f"Missing token in configuration file: {e}")
        raise
    except e:
        logger.error(f"Something occured while reading config: {e}")
        raise

    return config


def main():
    """Initialize and run the Telegram bot."""
    config = parse_config()
    application = ApplicationBuilder().token(config["token"]).build()
    application.bot_data["download_path"] = config["download_path"]
    application.bot_data["denodo_repository_path"] = config["denodo_repository_path"]

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("query", query))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), help_message))
    application.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), attachment))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Start polling for updates from Telegram
    application.run_polling()

if __name__ == "__main__":
    main()

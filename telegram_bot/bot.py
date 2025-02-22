import logging
import configparser
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
from denodo_wrapper import upload_file

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

async def caps(update, context):
    """Convert the user's message to uppercase."""
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_caps
    )

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

    message = update.message
    attachment = message.effective_attachment
    caption = update.message.caption

    if not attachment:
        await message.reply_text("No attach")
        return

    new_file = await attachment.get_file()
    file_name = getattr(message.document, 'file_name', None) or f"file_{new_file.file_id}"
    file_path = download_path / file_name

    file_path.parent.mkdir(parents=True, exist_ok=True)

    await new_file.download_to_drive(custom_path=file_path)

    # TODO: Don't block event loop (make sure this execution is asynchronous)
    upload_file(file_path)

    await message.reply_text(f"Respuesta")

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

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("caps", caps))
    application.add_handler(InlineQueryHandler(inline_caps))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), help_message))
    application.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), attachment))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Start polling for updates from Telegram
    application.run_polling()

if __name__ == "__main__":
    main()

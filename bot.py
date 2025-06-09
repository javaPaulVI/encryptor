from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)
from encryptor import Encryptor

encryptor = Encryptor()

ASKING_INPUT = 0  # Conversation state

async def start_encrypt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please send me the text you want to encrypt.")
    return ASKING_INPUT  # Wait for user input

async def do_encrypt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    encrypted = encryptor.encrypt_message(user_input)
    await update.message.reply_text(f"Encrypted text: {encrypted}")
    return ConversationHandler.END  # End conversation

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Encryption cancelled.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token('YOUR_BOT_TOKEN').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('encrypt', start_encrypt)],
        states={
            ASKING_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, do_encrypt)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

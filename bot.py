from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import os

# Palabras prohibidas para filtrar
palabras_prohibidas = [
    'malo', 'compro', 'vendo', 'barato', 'spam',
    'venta', 'jugosa', 'se vende', 'en venta', 'publicidad'
]

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("¡Hola! Estoy activo y vigilando los mensajes.")

# Manejo de mensajes
async def manejar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = update.message.text.lower() if update.message.text else ""
    if any(palabra in texto for palabra in palabras_prohibidas):
        try:
            await update.message.delete()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="🚫 Mensaje eliminado por contenido inapropiado."
            )
        except Exception:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ No tengo permisos para borrar mensajes."
            )

def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensajes))

    app.run_polling()

if __name__ == "__main__":
    main()















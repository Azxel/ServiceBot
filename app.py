import google.generativeai as genai

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# informacion del bot
token = '6539036957:AAF5jJF6gOp8enFDdZOwUryD1l0C6tQOZ8g'
username = 'chat_rd_t_bot'

# informacion de la api
api_key = 'AIzaSyAjVk7sAULPEExMKXd-0IllLGjsnDpFl94'

# configuracion 
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# commands
async def start(update: Update, context: ContextTypes):
    await update.message.reply_text("Hola, soy un bot. Está en fase de prueba")
async def help(update: Update, context: ContextTypes):
    await update.message.reply_text("Hola mucho gusto, en que puedo ayudarte?")

# respuesta a los mensajes 
def handle_response(text: str, context: ContextTypes, update: Update):
    proccesed_text = text.lower()
    print("Procesando")
    response = model.generate_content([proccesed_text])
    print("Fin del Proceso")
    return response.text

# 
async def handle_message(update: Update, context: ContextTypes):
    message_type = update.message.chat.type # private, group, subgroup, channel
    text = update.message.text

    if message_type == 'group':
        if text.startswith(username):
            new_text = text.replace(username, '')
            response = handle_response(new_text, context, update)
        else:
            return
    else:
        response = handle_response(text, context, update)

    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes):
    print(context.error)
    await update.message.reply_text("Ha ocurrido un error")

if __name__ == '__main__':
    # creamos la app
    print('Iniciando bot ...')
    app = Application.builder().token(token).build() 

    # creamos commnads
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))

    # creamos respuestas
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # creamos errores
    app.add_error_handler(error)

    # iniciar bot
    print('Bot iniciado')
    app.run_polling(poll_interval=1, timeout=3)
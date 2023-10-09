import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import typing
from typing import Final
from re import findall
from random import randint
import tomllib

BOT_USERNAME: Final = 'phil'
solutions: int = 2
answers: list = ['yes', 'ja', 'doch', 'yeah', 'genau', 'si', 'oui', 'affirm', 'positiv']
n_answers: list = ['nein', 'no', 'nerv nicht', 'quatsch', 'falsch', 'negativ']
wakeupcalls: list = ['phil', 'welche', 'abstimmen', 'stimmen', 'was haltet ihr davon', 'wie findet ihr']
counter: int = 0

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Servus, ich bins Phil.")

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def handle_responses(text: str, user: str) -> str:
    processed: str = text.lower()
    numbers: list = findall(r'\d+', processed)
    global counter
    global solutions
    print(f'counter: {counter}')
    print(f'Nutzer: {user}')
    print(f'Processed: "{processed}"')
    if 'phil' in processed and 'Leo' == user:
        counter = 1
        return f"Mein Erschaffer! Wie darf ich weiterhelfen?"
    elif 'pscht!' in processed and 'Leo' == user:
        counter = 0
        return None
    elif any(start in processed for start in wakeupcalls) and counter == 0:
        counter = 1
        return "JAAA. Wie viele Möglichkeiten gibt's?"
    elif len(numbers) >= 1 and counter > 0:
        solutions = round(int(numbers[0]))
        counter = 2
        return f"Okay es gibt also {solutions} Lösungen. Soll ich für euch entscheiden?"
    elif any(yes in processed for yes in answers) and counter > 1:
        counter = 0
        return f"Dachte ich mir. Nehmt einfach die {randint(1, solutions)}. Die ist sowieso am besten..."
    elif any(no in processed for no in n_answers) and counter > 1:
        counter = 0
        return f"Mir doch egal. Nehmt einfach die {randint(1, solutions)}. Die ist sowieso am besten..."
    elif counter > 0:
        return 'Das verstehe ich nicht?'
    

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    print(update.message.from_user)

    if message_type == 'group' or message_type == 'supergroup':
            # new_text: str = text.replace(BOT_USERNAME, '').strip()
        response: str = handle_responses(text, update.message.from_user.first_name)
    else:
        response: str = handle_responses(text, update.message.chat.first_name)
    
    print('Bot:', response)
    if response is not None:
        await update.message.reply_text(response)


if __name__ == '__main__':
    with open("token.toml", "rb") as f:
        TOKEN = tomllib.load(f)
    application = ApplicationBuilder().token(TOKEN['token']).build()
    
    # Commands
    start_handler = CommandHandler('start', start_command)
    #echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # Messages
    msg_handler = MessageHandler(filters.TEXT, handle_message)

    #run
    application.add_handler(start_handler)
    application.add_handler(msg_handler)
    application.run_polling()


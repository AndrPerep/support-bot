# import os
# import telegram
#
# from dotenv import load_dotenv
#
#
# if __name__ == '__main__':
#     load_dotenv()
#     tg_token = os.getenv('TG_TOKEN')
#     tg_chat_id = os.getenv('TG_CHAT_ID')
#
#     bot = telegram.Bot(tg_token)
#
#     bot.send_message(chat_id=tg_chat_id, text='hi')
#     print('hi')

# _________________________________________________________________________________________________________________
# from telegram import ForceReply, Update
# from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
#
#
#
# # Define a few command handlers. These usually take the two arguments update and
# # context.
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /start is issued."""
#     user = update.effective_user
#     await update.message.reply_html(
#         rf"Hi {user.mention_html()}!",
#         reply_markup=ForceReply(selective=True),
#     )
#
#
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /help is issued."""
#     await update.message.reply_text("Help!")
#
#
# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Echo the user message."""
#     await update.message.reply_text(update.message.text)
#
#
# def main() -> None:
#     """Start the bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token("TOKEN").build()
#
#     # on different commands - answer in Telegram
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("help", help_command))
#
#     # on non command i.e message - echo the message on Telegram
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
#
#     # Run the bot until the user presses Ctrl-C
#     application.run_polling()
#
#
# if __name__ == "__main__":
#     main()

#_________________________________________________________________

import telegram
from telegram.error import NetworkError, Unauthorized

from time import sleep
from dotenv import load_dotenv
import os

update_id = None


def main():
    global update_id

    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    bot = telegram.Bot(tg_token)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None


    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
        chat_id = update.message.chat_id
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            update.message.reply_text(update.message.text)


if __name__ == '__main__':
    main()

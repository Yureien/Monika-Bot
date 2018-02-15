import logging
import os
from threading import Timer
from telegram.ext import Updater, CommandHandler, RegexHandler

from modules.common_functions import Common

# For security reasons, the original token for the bot is stored in my VPS.
# The token mentioned here is just a test token. If you want to contribute,
# please create a test bot with @BotFather and add its token in the except.
isDevMode = False
try:
    TOKEN = os.environ['TELEGRAM_TOKEN']
except:
    TOKEN = "537036751:AAGYK7ZzutTTMuPUb777vdPvW2kmw0f3S0U"
    isDevMode = True
PORT = int(os.environ.get('PORT', '6969'))  # Port is dynamically served by VPS.

print("Is running in development mode: ", isDevMode)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

funcs = Common(isDevMode)
dispatcher.add_handler(CommandHandler('credits', funcs.credits))
dispatcher.add_handler(CommandHandler('start', funcs.start))
dispatcher.add_handler(CommandHandler('urban_dictionary', funcs.urban_dictionary, pass_args=True))
dispatcher.add_handler(CommandHandler('decide', funcs.decide))
dispatcher.add_handler(CommandHandler('roll_dice', funcs.roll_dice))
dispatcher.add_handler(CommandHandler('sticker_dl', funcs.download_sticker))
dispatcher.add_handler(CommandHandler('shrug', funcs.shrug))
dispatcher.add_handler(CommandHandler('table', funcs.table, pass_args=True))
dispatcher.add_handler(CommandHandler('quote', funcs.quote, pass_args=True))

dispatcher.add_handler(RegexHandler(funcs.regex_text, funcs.regex))

print("Starting Monika Bot...")
# For my VPS, webhook is used. However, for development,
# the polling method is used as webhook requires SSL.
if not isDevMode:
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://telegram.monika.sohamsen.me/" + TOKEN)
    updater.idle()
else:
    if 'IS_TRAVIS' in os.environ:  # Terminate after 10s if Travis
        updater.start_polling()
        Timer(10.0, updater.stop).start()
    else:
        updater.start_polling()
        updater.idle()

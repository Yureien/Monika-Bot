import logging
import requests
import json
import os
from random import randint
from telegram.ext import Updater, CommandHandler

from common_functions import credits, start, urban_dictionary, decide, \
    roll_dice, download_sticker, shrug, table

# For security reasons, the original token for the bot is stored in Heroku.
# The token mentioned here is just a test token. If you want to contribute,
# please create a test bot with @BotFather and add its token in the except.
isDevMode = False
try:
    TOKEN = os.environ['TELEGRAM_TOKEN']
except:
    TOKEN = "537036751:AAGYK7ZzutTTMuPUb777vdPvW2kmw0f3S0U"
    isDevMode = True
PORT = int(os.environ.get('PORT', '8443'))  # Port is dynamically served by Heroku.

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('credits', credits))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('urban_dictionary', urban_dictionary, pass_args=True))
dispatcher.add_handler(CommandHandler('decide', decide))
dispatcher.add_handler(CommandHandler('roll_dice', roll_dice))
dispatcher.add_handler(CommandHandler('sticker_dl', download_sticker))
dispatcher.add_handler(CommandHandler('shrug', shrug))
dispatcher.add_handler(CommandHandler('table', table, pass_args=True))

print("Starting Monika Bot...")
# For Heroku, webhook is used. However, for development,
# the polling method is used as webhook requires SSL.
if not isDevMode:
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://lilmonix3-bot.herokuapp.com/" + TOKEN)
    updater.idle()
else:
    updater.start_polling()


import logging
import requests
import json
import os
from random import randint
from telegram.ext import Updater, CommandHandler

TOKEN = os.environ['TELEGRAM_TOKEN']
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

def start(bot, update):
    update.message.reply_text("Hello all! I am Monika bot. If you do not know me, I suggest you play Doki Doki!")

def urban_dictionary(bot, update, args):
    term = ' '.join(args)
    ud_api = "http://api.urbandictionary.com/v0/define?term=" + term
    ud_reply = json.loads(requests.get(ud_api).content)['list']
    if len(args) == 0:
        update.message.reply_text("USAGE: /urban_dictionary <Word>")
    elif len(ud_reply) != 0:
        ud = ud_reply[0]
        reply_text = "<b>{0}</b>\n<a href='{1}'>{1}</a>\n<i>By {2}</i>\n\nDefinition: {3}\n\nExample: {4}".format(
            ud['word'], ud['permalink'], ud['author'], ud['definition'], ud['example'])
        update.message.reply_text(reply_text, parse_mode='HTML')
    else:
        update.message.reply_text("Term not found")

def decide(bot, update):
    r = randint(1, 100)
    if r <= 45:
        update.message.reply_text("Yes.")
    elif r <= 90:
        update.message.reply_text("No.")
    else:
        update.message.reply_text("Maybe.")

def roll_dice(bot, update):
    r = randint(1, 6)
    update.message.reply_text("Rolled a %d." % (r))

def hello(bot, update):
    update.message.reply_text(
        'Hello {}!'.format(update.message.from_user.first_name))

dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('urban_dictionary', urban_dictionary, pass_args=True))
dispatcher.add_handler(CommandHandler('decide', decide))
dispatcher.add_handler(CommandHandler('roll_dice', roll_dice))

print("Starting Monika Bot...")
try:
    PORT = int(os.environ['PORT'])
except:
    PORT = 33333
updater.start_webhook(port=PORT)
updater.idle()

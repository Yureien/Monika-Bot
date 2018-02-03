import re
import requests
import json
from random import randint

from . import quotes as qut


class Common:

    def __init__(self):
        self.regex_text = "s/([a-zA-Z0-9_\-+ \*\(\)!@#$%.\^&{}\[\]:;\"\'<>,\?]+)/([a-zA-Z0-9_\-+ \*\(\)!@#$%.\^&{}\[\]:;\"\'<>,\?]+)/?"  # noqa
        self.quotes = qut.Quotes()

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Hello! I am Monika bot. If you do not know me, I suggest you " +
                         "play Doki Doki!\n\nI am a multipurpose bot, and I can do many things. " +
                         "To know more, [click here](https://github.com/FadedCoder/Monika-Bot).",
                         parse_mode="Markdown")

    def shrug(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="¯\_(ツ)_/¯")

    def table(self, bot, update, args):
        if len(args) == 0:
            update.message.reply_text("USAGE: /table flip|unflip")
        else:
            if args[0].lower() == "flip":
                bot.send_message(chat_id=update.message.chat_id, text="(╯°□°）╯彡 ┻━┻")
            elif args[0].lower() == "unflip":
                bot.send_message(chat_id=update.message.chat_id, text="┬─┬ ノ(°-°ノ)")
            else:
                update.message.reply_text("USAGE: /table flip|unflip")

    def urban_dictionary(self, bot, update, args):
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

    def decide(self, bot, update):
        r = randint(1, 100)
        if r <= 45:
            update.message.reply_text("Yes.")
        elif r <= 90:
            update.message.reply_text("No.")
        else:
            update.message.reply_text("Maybe.")

    def roll_dice(self, bot, update):
        r = randint(1, 6)
        update.message.reply_text("Rolled a %d." % (r))

    def credits(self, bot, update):
        update.message.reply_text(
            'Made by *Soham Sen* - @FadedChaos.\nWebsite - [sohamsen.me](http://sohamsen.me).\n\n' +
            'Want to contribute to this? Or want more features? [Click here](https://github.com/FadedCoder/Monika-Bot).',
            parse_mode='Markdown'
        )

    def download_sticker(self, bot, update):
        update.message.reply_text(str(update))

    def regex(self, bot, update):
        try:
            text = update.message.reply_to_message.text
            a, b = re.findall(self.regex_text, update.message.text)[0]
            x = re.findall(a, text)
            for i in x:
                text = text.replace(i, b)
            bot.send_message(chat_id=update.message.chat_id, text=text,
                             reply_to_message_id=update.message.reply_to_message.message_id)
        except Exception:
            pass  # Ignored for now.

    def quote(self, bot, update, args):
        help_text = "USAGE: /quote all|quote_id|<reply to a message to add quote>"
        if len(args) == 1:
            tqs = self.quotes.count_quotes(update.message.chat_id)
            try:
                if int(args[0]) > tqs:
                    update.message.reply_text("Quote not found.\n\n" + help_text)
                else:
                    q = self.quotes.get_quote(update.message.chat_id, int(args[0]))
                    reply_str = "Quote #{0}:\n\n{1}".format(q['quote_id'], q['quote'])
                    bot.send_message(chat_id=update.message.chat_id,
                                     text=reply_str)
            except ValueError:
                if args[0].lower() == "all":
                    _qstr = "Quote {0}:\n{1}]\n\n"
                    reply_str = "All quotes in this chat:\n\n"
                    for i in range(1, tqs + 1):
                        reply_str += _qstr.format(i, self.quotes.get_quote(
                            update.message.chat_id, i)['quote'])
                    bot.send_message(chat_id=update.message.chat_id, text=reply_str)
                else:
                    update.message.reply_text(help_text)
        elif len(args) == 0:
            try:
                message = update.message.reply_to_message
                qid = self.quotes.add_quote(message.chat_id, message.message_id,
                                            message.from_user.id, re.escape(message.text))
                bot.send_message(chat_id=update.message.chat_id,
                                 text="Added quote #{}.".format(qid))
            except AttributeError:
                bot.send_message(chat_id=update.message.chat_id, text="Random Quote:\n\n" +
                                 self.quotes.get_quote(update.message.chat_id)['quote'] +
                                 "\n\n" + help_text)
        else:
            update.message.reply_text(help_text)

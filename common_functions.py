def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=
                     "Hello all! I am Monika bot. If you do not know me, I suggest you play Doki Doki!")

def shrug(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="¯\_(ツ)_/¯")

def table(bot, update, args):
    if len(args) == 0:
        update.message.reply_text("USAGE: /table flip|unflip")
    else:
        if args[0] == "flip":
            bot.send_message(chat_id=update.message.chat_id, text="(╯°□°）╯彡 ┻━┻")
        elif args[0] == "unflip":
            bot.send_message(chat_id=update.message.chat_id, text="┬─┬ ノ(°-°ノ)")
        else:
            update.message.reply_text("USAGE: /table flip|unflip")

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

def credits(bot, update):
    update.message.reply_text(
        'Made by *Soham Sen* - @FadedChaos.\nWebsite - [sohamsen.me](http://sohamsen.me).\n\n' +
        'Want to contribute to this? Or want more features? [Click here](https://github.com/FadedCoder/Monika-Bot).',
        parse_mode='Markdown'
    )

def download_sticker(bot, update):
    update.message.reply_text(str(update.message))

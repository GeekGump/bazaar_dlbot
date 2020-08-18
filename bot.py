from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from bazaar_dl import get_details, get_download_link
from config import BOT_TOKEN


def start_command(update, contex):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    contex.bot.send_message(
        chat_id,
        'سلام ✋\n\n✅ اگه لینک یا نام پکیج برنامه ها'
        'از کافه بازار را برای من بفرستی من اون را برات'
        'دانلود میکنم یا لینک بهت میدم خودت دانلود کنی.\n\n'
        '📣 راستی، میتونی با روش زیر برنامه یا بازی'
        'مورد نظر خودت را در کافه بازار جستجو کنی:\n'
        '`@bazaar_dlbot Instagram`\n\n\n'
        '🧑‍💻 Developer: Matin Baloochestani\n'
        '🖥 Source code is available on '
        '[GitHub](https://github.com/Matin-B/bazaar_dlbot)',
        reply_to_message_id=message_id,
        parse_mode=ParseMode.MARKDOWN
    )


def text_message(update, contex):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    message_text = update.message.text
    if '/video/' in message_text or '/serial/' in message_text:
        contex.bot.send_message(
            chat_id,
            'در حال حاظر فیلم و سریال پشتیبانی نمیشود.'
        )
    else:
        if '/app/' in message_text:
            package_name = message_text.split('/app/')[-1]
        else:
            package_name = message_text
        app_details = get_details(package_name)
        download_link = get_download_link(package_name)
        name = app_details['name']
        icon = app_details['icon']
        short_description = app_details['short_description']
        description = app_details['description']
        author_name = app_details['author_name']
        author_url = app_details['author_url']
        install_count_range = app_details['install_count_range']
        review_count = app_details['review_count']
        version_name = app_details['version_name']
        version_code = app_details['version_code']
        last_updated = app_details['last_updated']
        contex.bot.send_photo(
            chat_id,
            icon,
            f'📱 App Name: {name}\n'
            f'📦 Package Name: `{package_name}`\n'
            f'♦️ Version: {version_name}({version_code})\n'
            f'🔄 Last Updated: {last_updated}\n'
            f'🔰 Installs Count: {install_count_range}\n'
            f'💬 Short Description:\n`{short_description}`\n\n'
            f'🔗 Download Link:\n{download_link}',
            reply_to_message_id=message_id,
            parse_mode=ParseMode.MARKDOWN,
        )


updater = Updater(BOT_TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start_command))
updater.dispatcher.add_handler(MessageHandler(Filters.text, text_message))

updater.start_polling()

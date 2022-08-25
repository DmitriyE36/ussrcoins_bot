from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
import structlog
import settings
from ussrcoins.parser import get_coin_price, get_coin_url

logging.basicConfig(level = logging.INFO)
logger = structlog.getLogger()

def start_user(update, context):
        logger.debug('Вызван /start')
        update.message.reply_text('Введите год интересующей Вас монеты с 1921 по 1991 в формате "ГГГГ"')
        return 1
def year_coins_user(update, context):
    try:
        input_year = update.message.text
        logger.debug(input_year)
        if '1947' in input_year:
            update.message.reply_text('В 1947,1959,1960 годах не было выпуска монет, введите другой')
        elif '1959' in input_year:
            update.message.reply_text('В 1947,1959,1960 годах не было выпуска монет, введите другой')
        elif '1960' in input_year:
            update.message.reply_text('В 1947,1959,1960 годах не было выпуска монет, введите другой')
        else:
            context.user_data['input_year'] = input_year
            coin_url = get_coin_url(input_year)
            coins_name = coin_url.keys()
            coins = '\n '.join(coins_name)
            update.message.reply_text(f'В {input_year} году чеканили монеты достоинством:\n {coins}\n\n Введите нужный Вам номинал из списка')
            return 2
    except(AttributeError):
        update.message.reply_text('Введите год из указанного периода')
        return 1
     
def coin_user(update, context):
    input_coin = update.message.text
    logger.debug(input_coin)
    input_year = context.user_data['input_year']
    coin_url = get_coin_url(input_year)
    if input_coin in coin_url:
        url = coin_url[input_coin]
        safety_price = get_coin_price(url)
        safe_pr = '\n'.join(['{0}: {1}'.format(k,v) for k, v in safety_price.items()])
        update.message.reply_text(f'Стоимость монеты по степени сохранности:\n {safe_pr}\n\n Для нового запроса нажмите /start' )
        return ConversationHandler .END
    else:
        update.message.reply_text('Введите номинал монеты так, как он указан в списке')
        return 2
    
def new_request(update, context):
    update.message.reply_text('Поробуйте новый запрос, нажмите /start')

def coin_bot():
    ussrbot = Updater(settings.APY_KEY, use_context=True)
    dp = ussrbot.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_user)],
        states={
            1: [MessageHandler(Filters.text, year_coins_user)],
            2: [MessageHandler(Filters.text, coin_user)]
        },
        fallbacks=[MessageHandler(Filters.all, new_request)]
    )
    dp.add_handler(conv_handler)
    logger.info('Бот стартовал')
    ussrbot.start_polling()
    ussrbot.idle()

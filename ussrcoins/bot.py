from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
import structlog
import settings
from ussrcoins.parser import get_coin_price, get_coin_url

logging.basicConfig(level = logging.INFO)
logger = structlog.getLogger()

def start_user(update, context):
    logger.debug('Вызван /start')
    update.message.reply_text('Введите год интересующей Вас монеты с 1921 по 1930')
    return 1

def year_coins_user(update, context):
    input_year = update.message.text
    logger.debug(input_year)
    context.user_data['input_year'] = input_year
    coin_url = get_coin_url(input_year)
    coins_name = coin_url.keys()
    coins = ', '.join(coins_name)
    update.message.reply_text(f'Введите название монеты из предложенного списка: [{coins}]')
    return 2
     
def coin_user(update, context):
    input_coin = update.message.text
    logger.debug(input_coin)
    context.user_data['input_coin'] = input_coin
    input_year = context.user_data['input_year']
    coin_url = get_coin_url(input_year)
    url = coin_url[input_coin]
    safety_price = get_coin_price(url)
    update.message.reply_text(f'Стоимость монеты по степени сохранности:\n {safety_price}')
    return ConversationHandler .END
   
def coin_bot():
    ussrbot = Updater(settings.APY_KEY, use_context=True)
    dp = ussrbot.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_user)],
        states={
            1: [MessageHandler(Filters.text, year_coins_user)],
            2: [MessageHandler(Filters.text, coin_user)]
        },
        fallbacks=[CommandHandler("start", start_user)]
    )
    dp.add_handler(conv_handler)
    logger.info('Бот стартовал')
    ussrbot.start_polling()
    ussrbot.idle()

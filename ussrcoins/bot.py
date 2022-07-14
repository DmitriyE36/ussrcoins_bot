from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
import structlog
import settings
from ussrcoins.parser import get_coins, get_coin_url

logging.basicConfig(level = logging.INFO)
logger = structlog.getLogger()

def start_user(update, context):
    logger.debug('Вызван /start')
    update.message.reply_text('Введите номинал монеты в формате "X коп. (Х руб.) ХХХХ года"')
    return 1
  
def coin_user(update,context):
    input_coin = update.message.text
    context.user_data['input_coin'] = input_coin
    url = get_coin_url(input_coin)
    coin_dict = get_coins(url)
    safety = coin_dict.keys()
    safe = ', '.join(safety)
    update.message.reply_text(f'Введите степень сохранности монеты из предложенного списка {safe}')
    return 2

def safety_user(update,context): 
    input_safety = update.message.text
    input_coin = context.user_data['input_coin']
    url = get_coin_url(input_coin)
    logger.debug(input_safety)
    coin_dict = get_coins(url)
    price_coin = coin_dict[input_safety]
    logger.debug(price_coin)
    update.message.reply_text(f'Стоимость монеты: {price_coin}')
    return ConversationHandler .END

def coin_bot():
    ussrbot = Updater(settings.APY_KEY, use_context=True)
    dp = ussrbot.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_user)],
        states={
            1: [MessageHandler(Filters.text, coin_user)],
            2: [MessageHandler(Filters.text, safety_user)]
        },
        fallbacks=[CommandHandler("start", start_user)]
    )
    dp.add_handler(conv_handler)
    logger.info('Бот стартовал')
    ussrbot.start_polling()
    ussrbot.idle()

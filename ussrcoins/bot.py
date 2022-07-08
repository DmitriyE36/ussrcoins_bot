from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import structlog
import settings
from ussrcoins.parser import url, get_coins

logging.basicConfig(level = logging.INFO)
logger = structlog.getLogger()


def start_user(update, context):
    logger.debug('Вызван /start')
    update.message.reply_text('Введите степень сохранности монеты из предложенного списка (G, VG, F, VF, XF, AU, UNC, Proof)')
    
def coin_user(update, context):    
    input_safety = update.message.text
    logger.debug(input_safety)
    fcoins_dict = get_coins(url)
    price_coin = fcoins_dict[input_safety]
    logger.debug(price_coin)
    update.message.reply_text(f'Стоимость монеты: {price_coin}')

def coin_bot():
    ussrbot = Updater(settings.APY_KEY, use_context=True)
    dp = ussrbot.dispatcher
    dp.add_handler(CommandHandler("start", start_user))
    dp.add_handler(MessageHandler(Filters.text, coin_user))
    logger.info('Бот стартовал')
    ussrbot.start_polling()
    ussrbot.idle()

"""
if __name__ == '__main__':
    coin_bot()
"""
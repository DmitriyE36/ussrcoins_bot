import requests
from bs4 import BeautifulSoup

coin_urls = {
    '10 коп. 1921 года': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12572.asp',
    '15 коп. 1921 года': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12766.asp',
    '20 коп. 1921 года': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12952.asp',
    '50 коп. 1921 года': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13141.asp',
    '1 руб. 1921 года': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13210.asp'
}

def get_coin_url(coin: str)->str:
    url = coin_urls.get(coin)
    return url

def get_coins(url):
    result = requests.get(url)
    result.raise_for_status()
    soup = BeautifulSoup(result.content, 'html.parser')
    table_coins = soup.findAll('tr', class_='tr-mobile')
    safety = []
    price = []
    for coins in table_coins:
        safety.append(coins.find('b').text)
        price.append(coins.find('br').previous_element)
    coins_dict = dict(zip(safety, price))
    return coins_dict

    

import requests
from bs4 import BeautifulSoup

coin_urls = {
    '1921':{'10 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12572.asp', '15 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12766.asp', '20 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12952.asp', '50 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13141.asp', '1 рубль': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13210.asp'},
    '1922':{'10 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12573.asp', '15 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12767.asp', '20 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12955.asp', '50 копеек ПЛ': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13143.asp', '50 копеек АГ': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13142.asp', '1 рубль ПЛ': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13215.asp', '1 рубль АГ': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13213.asp'},
    '1923':{'10 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12574.asp', '15 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12769.asp', '20 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12957.asp'},
    '1924':{'1 копейка гурт рубчатый': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr11812.asp', '1 копейка гурт гладкий': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr11813.asp', '2 копейки гурт рубчатый': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12012.asp', '2 копейки гурт гладкий': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12013.asp', '3 копейки гурт рубчатый': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12179.asp', '3 копейки гурт гладкий': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12182.asp', '5 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12413.asp', '10 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12575.asp', '15 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12770.asp', '20 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12959.asp', '50 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13155.asp', '1 рубль': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13218.asp'},
    '1925':{'Полкопейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr11986.asp', '1 копейка': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr11817.asp', '2 копейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12019.asp', '10 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12576.asp', '15 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12777.asp', '20 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12962.asp', '50 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13161.asp'},
    '1926':{'1 копейка': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr11820.asp', '2 копейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12022.asp', '3 копейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12187.asp', '5 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12420.asp', '50 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13164.asp'},
    '1927':{'Полкопейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr11987.asp', '1 копейка': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr11822.asp', '2 копейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12023.asp', '3 копейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12191.asp', '5 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12425.asp', '10 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12578.asp', '15 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12804.asp', '20 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12965.asp', '50 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr13166.asp'},
    '1928':{'Полкопейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr11988.asp', '1 копейка': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr11825.asp', '2 копейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12024.asp', '3 копейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12193.asp', '5 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12426.asp', '10 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12587.asp', '15 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12806.asp', '20 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12966.asp'},
    '1929':{'1 копейка': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr11827.asp', '2 копейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12027.asp', '3 копейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12195.asp', '5 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12428.asp', '10 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12619.asp', '15 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12810.asp', '20 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12968.asp'},
    '1930':{'1 копейка': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr11828.asp', '2 копейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12028.asp', '3 копейки': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12197.asp', '5 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12429.asp', '10 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12624.asp', '15 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12811.asp', '20 копеек': 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12970.asp'},
}

def get_coin_url(year: str)->str:
    coin_url = coin_urls.get(year)
    return coin_url

def get_coin_price(url):
    result = requests.get(url)
    result.raise_for_status()
    soup = BeautifulSoup(result.content, 'html.parser')
    table_coins = soup.findAll('tr', class_='tr-mobile')
    safety = []
    price = []
    for coins in table_coins:
        safety.append(coins.find('b').text)
        price.append(coins.find('br').previous_element)
    safety_price = dict(zip(safety, price))
    return safety_price

    

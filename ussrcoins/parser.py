import requests
from bs4 import BeautifulSoup

url = 'https://www.fcoins.ru/catalog/catalogussr/catalogussr12572.asp'
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

"""
if __name__ == '__main__':
    fcoins_dict = get_coins(url)
    print(fcoins_dict)
"""
    

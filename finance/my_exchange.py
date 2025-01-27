from bs4 import BeautifulSoup as bs
import requests
from django.utils.timezone import now

current_datetime = now()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


class Val_para:
    def __init__(self, website, datetime, name, buy, sell):
        self.datetime = datetime
        self.name = name
        self.buy = buy
        self.sell = sell
        self.website = website

def get_price(row):
    txt=''
    for i in row:
        #print(i)
        if i.isdigit():
            txt+=i
        if i =='.' or i ==',':
            txt = txt+'.'
        else:
            pass
    price = float(txt)
    return price

def get_currency_rates():
    global headers
    url = 'https://www.royalexchange.cz/kurzovni-listek/'
    page = requests.get(url, headers=headers)



    soup = bs(page.text, 'lxml')
    d = {}
    td = soup.find_all('td')
    counter=0
    for i in td:
        counter+=1
        d[counter] = i.text
    #print(d)

    data = []
    data.append(Val_para(url, current_datetime, d[12], get_price(d[12+2]), get_price(d[12+3]))) #USD
    data.append(Val_para(url, current_datetime, d[3], get_price(d[3 + 2]), get_price(d[3+3])))#EUR
    data.append(Val_para(url, current_datetime, d[21], get_price(d[21+2]), get_price(d[21+3])))#GBP
    data.append(Val_para(url, current_datetime, d[156], get_price(d[156+2]), get_price(d[156+3])))#UAH

    # print(f'{url} downloaded successful at {now_d_t}')

    return data





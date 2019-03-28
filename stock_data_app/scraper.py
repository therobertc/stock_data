from bs4 import BeautifulSoup as BS 
import requests
from math import log, floor


def get_page_source_code(url):
    print('Connecting to website...')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        resp = requests.get(url, headers = headers)
        soup = BS(resp.content, "html.parser")
        print("Connection established!")
        return soup

    except Exception as e:
        print(e)


def scrape_data():
    """ scrape stock name, price and volume """
    soup = get_page_source_code("https://www.tradingview.com/markets/stocks-usa/market-movers-active/")
    stock_table = soup.select(".tv-data-table__tbody tr")
    
    stock_data = []

    for data in stock_table:
        stock_name = data.find("a").get_text(strip=True)
        stock_price = data.select("td")[1].get_text(strip=True)
        percentage_change = data.select("td")[2].get_text(strip=True)
        rating = data.select("td")[4].get_text(strip=True)
        stock_volume = data.select("td")[5].get_text(strip=True)

        details = {

                "name": stock_name,
                "price": stock_price,
                "change": percentage_change,
                "rating": rating,
                "volume": stock_volume,
                
                    }
        stock_data.append(details)
    return stock_data


def number_conversion(number):
    """ convert numbers to their respective unit i.e 1,000,000 to 1M """
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])

def sort_func(stock_data):

    # for data in stock_data:
    #     print(data)
    price_range = float(number_conversion(1000000)[:-1])
    if float(stock_data.get('price')) < 5.0 and float(stock_data.get('volume')[:-1]) > price_range:
        return True 
    else:
        return False 

def sorted_data():
    """ sort stock data based on price and volume -> price < $5 and volume > 1,000,000 """
    stock_data = scrape_data()
    filtered_data = list(filter(sort_func, stock_data))
    return filtered_data

# print(scrape_data())
# sorted_data()
# print(number_conversion(1000000))
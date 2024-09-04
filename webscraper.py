from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

url = 'https://www.flipkart.com/search?q=lenovo'
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Accept-Language':'en-US'
}

while True:
    response = requests.get(url, headers = headers)
    print(response.status_code)
    if response.status_code == 529:
        print("Received status code 529. Waiting before retrying...")
        time.sleep(10)
    else:
        break

soup = BeautifulSoup(response.content, 'html.parser')
d = {"product":[],"price":[],"rating":[]}
price = soup.find_all("div", class_='Nx9bqj _4b5DiR')

for ele in price:
    d['price'].append(ele.get_text(strip=True))
products = soup.find_all("div", class_='KzDlHZ')

for product in products:
    d["product"].append(product.get_text(strip=True))
ratings = soup.find_all("div", class_='XQDdHH')

for rating in ratings:
  d["rating"].append(rating.get_text(strip=True))

for i in range(len(d["product"])):
    print(d['product'][i]+" - "+d['price'][i]+" - "+d['rating'][i])


d['rating'] = d['rating'][:len(d['product'])]
df = pd.DataFrame(d)
df.to_excel('d.xlsx')

import requests
import math

url_base1 = 'https://www.lamoda.ru/catalogsearch/result/?q='
prompt = input().split()

url_final = url_base1 + prompt[0]
if len(prompt) > 1:
    for i in range (1,len(prompt)):
        url_final = url_final + "%20" + prompt[i]

r = requests.get(url_final)
front_page = r.text

index_begin = front_page.find('</h2><span class="d-catalog-header__product-counter">')
index_end = 0

for i in range(index_begin + 53, len(front_page)):
    if not front_page[i].isdigit():
        index_end = i
        break

quantity = int(front_page[index_begin + 53: index_end])
page_numbers = math.ceil(quantity/60)

articles = []
brands = []
prices = []
sales = []
summ_sales = []
names = []
country = []

for i in range(len(front_page)-12):
    if front_page[i: i + 12] == '<a href="/p/':
        index_article1 = (i + 12)
        for j in range(index_article1, len(front_page)):
            if front_page[j] == "/":
                index_article2 = j
                articles.append(str(front_page[index_article1:index_article2].upper()))
                break


for i in articles:

    url = 'https://www.lamoda.ru/p/' + i
    text = (requests.get(url)).text
    index_brands1 = text.find('Другие товары ') + 14
    for j in range(index_brands1, len(text)):
        if text[j] == "\n":
            index_brands2 = j
            break

    brands.append(str(text[index_brands1:index_brands2]))

    index_names1 = text.find('<title>') + 7
    for j in range(index_names1, len(text)):
        if text[j] == ",":
            index_names2 = j
            break
    names.append(str(text[index_names1:index_names2]))

    index_sales = text.find('"price":') + 8
    index_sales_final = index_sales
    while str(text[index_sales_final]) in "1234567890":
        index_sales_final += 1
    sales.append(text[index_sales:index_sales_final])

    index_price = text.find('"price":', text.find('"price":') + 1) + 8
    if text[index_price]=='"':
        index_price += 1
    index_price_final = index_price
    while str(text[index_price_final]) in "1234567890 ":
        index_price_final += 1
    prices.append(text[index_price:index_price_final].replace(" ",""))
    summ_sales.append(abs(int(prices[-1]) - int(sales[-1])))

    index_country = text.find('Страна производства","value":"') + 30
    index_country_final = index_country
    while str(text[index_country_final]) != '"':
        index_country_final+=1
    country.append(text[index_country:index_country_final])

for i in range(len(prices)-1):
    for j in range(i, len(prices)-1):
        if prices[i] > prices[j]:
            prices[j], prices[i] = prices[i], prices[j]
            

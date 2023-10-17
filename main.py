import requests
import math

url_base1 = 'https://www.lamoda.ru/catalogsearch/result/?q='
prompt = input().split()

url_final = url_base1 + prompt[0]
if len(prompt) > 1:
    
    for i in range (1, len(prompt)):
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

for i in range(1,page_numbers + 1):
    page = (requests.get(url_final + '&page=' + str(i))).text
    
    for j in range(len(page)-12):
    
        if page[j: j + 12] == '<a href="/p/':
            index_article1 = (j + 12)
            for k in range(index_article1, len(page)):
            
                if page[k] == "/":
                    index_article2 = k
                    articles.append(str(page[index_article1:index_article2].upper()))
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
    
    if text[index_price] == '"':
        index_price += 1
    index_price_final = index_price
    
    while str(text[index_price_final]) in "1234567890 ":
        index_price_final += 1
        
    prices.append(text[index_price:index_price_final].replace(" ",""))
    summ_sales.append(abs(int(prices[-1]) - int(sales[-1])))

    index_country = text.find('Страна производства","value":"') + 30
    index_country_final = index_country
    
    while str(text[index_country_final]) != '"':
        index_country_final += 1
        
    country.append(text[index_country:index_country_final])


for i in range(len(prices)-1):
    for j in range(len(prices) - i -1):
        if int(prices[j]) < int(prices[j+1]):
            
            prices[j], prices[j+1] = prices[j+1], prices[j]
            articles[j], articles[j+1] = articles[j+1], articles[j]
            names[j], names[j+1] = names[j+1], names[j]
            brands[j], brands[j+1] = brands[j+1], brands[j]
            summ_sales[j], summ_sales[j+1] = summ_sales[j+1], summ_sales[j]
            country[j], country[j+1] = country[j+1], country[j]

with open("table.txt","w+",encoding='utf-8') as file:
    file.write("Id                  Price               Sale                Name                          Brand               Country               ")
    for i in range(len(prices)):
        string = articles[i] + " "*(20-len(articles[i])) + str(prices[i]) + " "*(20-len(str(prices[i]))) + str(summ_sales[i]) + " "*(20-len(str(summ_sales[i])))
        string = string + names[i] + " "*(30-len(names[i])) + brands[i] + " "*(20-len(brands[i])) + country[i] + " "*(20-len(country[i])) + "\n"
        file.write(string)
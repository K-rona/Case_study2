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
manufacturers = []

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

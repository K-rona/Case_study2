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

begining = front_page.find('<div class="x-product-card-description__microdata-wrap">')
for k in range(60):
    index_begin = front_page[begining:].find('class="x-product-card__card"><a href="/p/')
    for h in range(index_begin + 41, len(front_page)):
        if front_page[h] == "/":
            index_end = h
            break
    articles.append(str(front_page[index_begin + 41:index_end]))
    begining = index_end

print(articles)

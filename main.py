import requests
import math

url_base1 = 'https://www.lamoda.ru/catalogsearch/result/?q='
prompt = input()

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

for i in range(1, page_numbers + 1):

    text = (requests.get(url_final + 'page=' + str(i))).text
    links = text.split('<div class="x-product-card-description__microdata-wrap">')

    for j in range(1, len(links)):
        item_card = links[j]
        if item_card.find('class="x-product-card-description__price-new') == -1:
            price_index1 = item_card.find('style="white-space: nowrap;">')
            for k in range(price_index1 + 29, len(item_card)):
                if not item_card[k].isdigit():
                    price_index2 = k
                    break
            prices += int(item_card[price_index1:price_index2])

for i in range(1, page_numbers + 1):

    text = (requests.get(url_final + 'page=' + str(i))).text
    index_article1 = text.find('src="//a.lmcdn.ru/img236x341/R/T/')
    for j in range(index_article1 + 33, len(text)):
        if text[j] == "_":
            index_article2 = j
            break
    articles.append(str(text[index_article1 + 33:index_article2]))

    begin = index_article2
    for k in range(begin, len(text)):
        index_begin = text[begin:].find('<a href="/p/')
        for h in range(index_begin + 12, len(text)):
            if text[h] == "/":
                index_end = h
        articles.append(str(text[index_begin + 12:index_end]))
        begin = index_end

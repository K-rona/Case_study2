import requests

url_base1 = 'https://www.lamoda.ru/catalogsearch/result/?q='
prompt = input()

url_final = url_base1 + prompt

r = requests.get(url_final)
front_page = r.text

index_begin = front_page.find('</h2><span class="d-catalog-header__product-counter">')
index_end = 0

for i in range(index_begin + 53, len(front_page)):
    if not front_page[i].isdigit():
        index_end = i
        break

quantity = int(front_page[index_begin + 53: index_end])
page_numbers = quantity//60

articles = []
brands = []
prices = []
manufacturers = []

from bs4 import BeautifulSoup
import re
import requests

search_keyword = input("What are you looking for? ")

url = f"https://www.newegg.com/p/pl?d={search_keyword}&N=4131"
result = requests.get(url).text
doc = BeautifulSoup(result, "html.parser") 

page_t = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_t).split("/")[-2].split(">")[-1][:-1])

items_found = {}

for page in range(1, pages + 1):
    url = f"https://www.newegg.com/p/pl?d={search_keyword}&N=4131&page={page}"
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser") 
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(search_keyword))
    
    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue
        
        link = parent['href']
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_="price-current").find("strong").string
            items_found[item] = {"price": price, "link": link}
        except:
            pass 

sorted_items = sorted(items_found.items(), key = lambda x: x[1]['price'])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("==================================")


# for item in items:
#         parent = item.parent
#         if parent.name != "a":
#             continue

#         link = parent['href']
#         next_parent = item.find_parent(class_="item-container")
        
#         price = next_parent.find(class_="price-current").find("strong").string
#         items_found[item] = {"price": price, "link": link}
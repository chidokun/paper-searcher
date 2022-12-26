from bs4 import BeautifulSoup
import requests
import sys

SEARCH_LINK = 'https://paperswithcode.com/search?q_meta=&q_type=&q={}'


def extract_page(item):
    title = item.find('h1')
    title = title.find('a')
    return {
        "title": title.text,
        "link": "https://paperswithcode.com" + title["href"]
    }

def show_help():
    print("Usage: python main.py \"[name of article]\"")

def search_code_page(item):
    print("\033[1;34mSelect:\033[0m", item["title"])
    page_content = requests.get(item["link"])
    content_parser = BeautifulSoup(page_content.text, "html.parser")
    code_table = content_parser.find('div', { "class": "code-table"})
    code_full_list = code_table.find('div', { 'id': 'implementations-full-list'})
    return [ code["href"] for code in code_full_list.findAll(class_="code-table-link") ]

def search_page(query):
    response = requests.get(SEARCH_LINK.format(query))

    parser = BeautifulSoup(response.text, 'html.parser')
    container = parser.find('div', { 'class': 'infinite-container'})
    items = container.findAll(class_='item')
    return [ extract_page(item) for item in items ] 

def show_select_items(items):
    print("\033[1;32m>>\033[0m You mean?")
    for i in range(len(items)):
        print("  [{}] {} ({})".format(i, items[i]["title"], items[i]["link"]))
    try:
        select = int(input("Your choice: "))
        return items[select]
    except:
        print("\033[1;31mInvalid selection! Please try again!\033[0m")
        return show_select_items(items)

    

def show_code_result(result):
    for i in result:
        print("\033[1;32m*\033[0m {}".format(i))

def main(argv):
    query = argv[1]
    if not query:
        show_help()
        return

    print("\033[1;34mSearch:\033[0m", query)
    items = search_page(query)
    n = len(items)
    if n == 0:
        print("\033[1;32m>>\033[0m No result!")
        return
    if n == 1:
        result = search_code_page(items[0])
        show_code_result(result)
    if n > 1:
        select = show_select_items(items)
        result = search_code_page(select)
        show_code_result(result)


if __name__ == "__main__":
    main(sys.argv)
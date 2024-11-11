from typing import AnyStr
import json
import requests
from bs4 import BeautifulSoup

num_page = 1


def page(num_page):
    response = requests.get(f"https://quotes.toscrape.com/page/{num_page}/")

    if response.status_code == 200:

        cards_from_one_page = {}
        arr = []

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="quote")


        for card in cards:

            text = card.find("span", class_="text").text
            cards_from_one_page["text"] = text

            by = card.find("small", class_="author").text
            cards_from_one_page["by"] = by

            tags = card.find("div", class_="tags")
            tag_f = tags.find_all("a", class_="tag")
            tags_arr = []
            for tag in tag_f:
                tags_arr.append(tag.text)

            cards_from_one_page["tags"] = tags_arr

            arr.append(cards_from_one_page.copy())

        return arr, num_page
    else:
        return None, num_page

def file_wroter(page_number):
    data, num_page = page(page_number)
    if data == None:
        print(f"Data is empty, try again, number page is {num_page}")
    if data != None:
        json.dump(data, open("data.json", "a+", encoding="utf-8"))
        print(f"Wrote in JSON file, page = {num_page}")

import requests
from bs4 import BeautifulSoup
import pydash as _
import json
import urllib.parse
import re

url = 'https://www.straitstimes.com'


def get_category():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # div.block-menu-primary > div.navbar-primary > ul#block-mainnavigation > li
    categories = []
    for li in soup.select('#block-mainnavigation > li'):
        category = {}
        category['name'] = li.a.text
        category['url'] = li.a['href']
        category['subcategories'] = []
        for subcategory in li.select('ul > li'):
            category['subcategories'].append({
                'name': subcategory.a.text,
                'url': subcategory.a['href']
            })
        categories.append(category)
    # remove duplicate category name
    result = []
    for category in categories:
        if not _.find(result, lambda x: x['name'] == category['name']):
            result.append(category)
    return result

def get_post_by_category(category_name):
    response = requests.get(url + category_name)
    soup = BeautifulSoup(response.text, "html.parser")
    content_div = soup.select_one('div.view.view-articles > div.view-content.row')
    list_post = []
    for element in content_div.select('div.view-content.row > div.views-row'):
        card = element.select_one('div.card')
        post = {'title': card.select_one('h5.card-title').text.strip(),
                'url': card.a['href'],
                'image': card.select_one('div.card-media').div.div.picture.img['src'],
                'created_at': int(card.select_one('div.card-time').time['data-created-timestamp']),
                }
        list_post.append(post)
    return list_post

import requests
from bs4 import BeautifulSoup
import pydash as _
import json
import urllib.parse
import re

from src.config import cookies, headers

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
    return _.filter_(result, lambda x: x['url'] != '/')

def get_post_by_category(category_name, page=0):
    url_page = url + category_name + '?page=' + str(page)
    response = requests.get(url_page)
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


def get_post_detail(post_url):
    response = requests.get(url + post_url , cookies = cookies , headers = headers)
    data = []
    soup = BeautifulSoup(response.content, "lxml")

    # Get the title of the post
    try:
        title = soup.find('h1', {'class': 'headline'}).text.strip()
    except:
        title = None

    # Get the main content of the post
    try:
        # Assuming the content is in a specific div. Adjust the class name as needed.
        content_div = soup.find('div', {'class': 'layout layout--onecol'})
        html_content = str(content_div)  # Get the raw HTML content of the post
    except:
        html_content = None

    # Get all images in the content
    images = []
    try:
        img_tags = content_div.find_all('img')
        for img in img_tags:
            img_url = img.get('src')
            if img_url:
                images.append(img_url)
    except:
        pass

    # Get all linked CSS files (external)
    css_links = []
    try:
        link_tags = soup.find_all('link', {'rel': 'stylesheet'})
        for link in link_tags:
            css_url = link.get('href')
            if css_url:
                css_links.append(css_url)
    except:
        pass

    # Get inline CSS (if any within the content)
    inline_css = []
    try:
        style_tags = soup.find_all('style')
        for style in style_tags:
            inline_css.append(style.text)
    except:
        pass

    return {
        'title': title,
        'html_content': html_content,  # Raw HTML of the post content
        'images': images,  # List of image URLs
        'css_links': css_links,  # List of external CSS URLs
        'inline_css': inline_css  # Any inline CSS found
    }
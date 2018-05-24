#! /usr/bin/env python

# Doesn't run in Windows Terminal due to some sort of console font issue
# Can get the output by running it through idle in the terminal with command
# "py -3.6 -midlelib -r .\wuxiascrape.py"

# For Linux "python3 wuxiascrape.py"
from __future__ import print_function
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import io
import sys
import re
import time

url = 'https://www.wuxiaworld.com/novel/i-shall-seal-the-heavens/issth-book-1-chapter-1'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
windows_write_file = 'C:\code\WebScraper\WebScraper\wuxiaoutput.txt'
wuxia_index_page = 'https://www.wuxiaworld.com/novel/i-shall-seal-the-heavens'
wuxia_fiction_title = "/novel/i-shall-seal-the-heavens/"
wuxia_domain = 'https://www.wuxiaworld.com'
req_index = Request(wuxia_index_page, headers={'User-Agent': 'Mozilla/5.0'})
search_param = 'div'
attr_1_param = 'class'
attr_2_param = 'fr-view'


def safe_print(s):
    try:
        print(s)
    except UnicodeEncodeError:
        if sys.version_info >= (3,):
            print(s.encode('utf8').decode(sys.stdout.encoding))
        else:
            print(s.encode('utf8'))

def extract_wuxia_urls(req_index):
    # Try and extract the urls from the fictionn's index page on WuxiaWorld
    list_of_urls = []
    
    page = urlopen(req_index).read().decode("utf-8")
    soup = BeautifulSoup(page, 'html.parser')
    page_links = soup.find_all("div", {"class": "panel panel-default"})
    #print(len(page_links))
    for d in page_links:
        links = d.find_all('a', href=True)[0:4]
        for a in links:
            #list_of_urls.append(a.get('href'))
            if wuxia_fiction_title in a.get('href'):
                list_of_urls.append(a.get('href'))
    
    #print(list_of_urls)
    #print(len(list_of_urls))

    return list_of_urls

def get_wuxia_content(req, search_param, attr_1_param, attr_2_param):
    # query website and return html to variable 'page'
    page = urlopen(req).read().decode("utf-8")
    # parse html in page variable into BeautifulSoup format
    soup = BeautifulSoup(page, 'html.parser')

    # try to get the div with the content that we want
    page_content = soup.find(search_param, attrs={attr_1_param: attr_2_param})
    soup_text = page_content.get_text()

    # try and strip away the html leading and trailing the text
    stripped_content = re.sub(r'\<[^>]*\>', '', soup_text)

    content = stripped_content.encode("utf-8", "ignore").decode("utf-8")
    content = content.replace("Previous Chapter", "")
    content = content.replace("Next Chapter", "")
    content = content.replace(".", ". ")
    content = content.replace("  ", " ")

    with io.open(windows_write_file, 'a', encoding="utf-8") as f:
        f.write(content)
        safe_print(content)

i = 0

list_of_urls = extract_wuxia_urls(req_index)

for foo in list_of_urls:
    request = Request((wuxia_domain + foo), headers={'User-Agent': 'Mozilla/5.0'})
    get_wuxia_content(request, search_param, attr_1_param, attr_2_param)
    i += 1
    print("Content for chapter " + str(i) + " parsed \n")
    time.sleep(2)
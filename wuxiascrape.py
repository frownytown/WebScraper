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

url = 'https://www.wuxiaworld.com/novel/i-shall-seal-the-heavens/issth-book-1-chapter-1'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
windows_write_file = 'C:\code\WebScraper\WebScraper\wuxiaoutput.txt'

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


def get_page_content(req, search_param, attr_1_param, attr_2_param):
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

    with io.open(windows_write_file, 'w', encoding="utf-8") as f:
        f.write(content)
        safe_print(content)


get_page_content(req, search_param, attr_1_param, attr_2_param)

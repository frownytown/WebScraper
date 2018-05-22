from bs4 import BeautifulSoup
import re
import sys
import time

try:
	# python 3
	from urllib.request import Request, urlopen
except ImportError:
	# Fall back to python 2 version
	from urllib2 import urlopen	

url = 'https://www.wuxiaworld.com/novel/i-shall-seal-the-heavens/issth-book-1-chapter-1'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

search_param = 'div'
attr_1_param = 'class'
attr_2_param = 'fr-view'


def get_page_content(req, search_param, attr_1_param, attr_2_param):
	# query website and return html to variable 'page'
	page = urlopen(req).read().decode("utf-8")
	# parse html in page variable into BeautifulSoup format
	soup = BeautifulSoup(page, 'html.parser')

	# try to get the div with the content that we want
	page_content = soup.find(search_param, attrs={attr_1_param:attr_2_param})
	soup_text = page_content.get_text()

	# try and strip away the html leading and trailing the text
	stripped_content = re.sub(r'\<[^>]*\>', '', soup_text)
	print(type(stripped_content))
	content = stripped_content.encode("utf-8", "replace").decode("utf-8")
	# print statements (use command line to redirect this to txt file)
	print(content)

get_page_content(req, search_param, attr_1_param, attr_2_param)
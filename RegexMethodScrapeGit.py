#! /usr/bin/env python

# Beginning with python
# import libraries
from bs4 import BeautifulSoup
import re

try:
	# python 3
	from urllib.request import urlopen
except ImportError:
	# Fall back to python 2 version
	from urllib2 import urlopen

# url variable table
# add url
index_page_url = ''
# domain name / add begining domain
domain_name = ''

def extract_urls(index_page):
	# create list to store urls
	list_of_urls = []

	fiction_index = urlopen(index_page)
	soup = BeautifulSoup(fiction_index, 'html.parser')
	soup.prettify()
	# try to get urls from table
	table_content = soup.find('table', id='chapters')
	# get the rows
	for anchor in table_content.find_all('a', href=True, limit=50):
		list_of_urls.append(anchor.get('href'))

	return list_of_urls

def url_generator(list_of_urls):
	# turn list into useable links
	for url in list_of_urls:
		get_page_content((domain_name + url))

def get_page_content(url):
	# query website and return html to variable 'page'
	page = urlopen(url)
	# parse html in page variable into BeautifulSoup format
	soup = BeautifulSoup(page, 'html.parser')

	# try to get the div with the content that we want
	page_content = soup.find('div', attrs={'class':'chapter-inner chapter-content'})
	soup_text = page_content.get_text()

	# try and strip away the html leading and trailing the text
	stripped_content = re.sub(r'\<[^>]*\>', '', soup_text)

	# print statements
	print(stripped_content)

if __name__ == '__main__':
	#get_page_content(url)
	list_of_urls = extract_urls(index_page_url)
	url_generator(list_of_urls)

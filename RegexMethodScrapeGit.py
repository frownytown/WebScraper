#! /usr/bin/env python

# Beginning with python
# import libraries
from __future__ import print_function
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import sys
import time
import io


# setting some variables for us with specific websites html tags
royalroad_div = 'div'
royalroad_attrs_1 = 'class'
royalroad_attrs_2 = 'chapter-inner chapter-content'
# url variable table
index_page_url = 'https://royalroadl.com/fiction/11209/the-legend-of-randidly-ghosthound'
fictionpress_url = 'https://www.fictionpress.com/s/2961893/1/Mother-of-Learning'
fictionpress_url_part_1 = 'https://www.fictionpress.com/s/2961893/'
fictionpress_url_part_2 = 1
fictionpress_url_part_3 = '/Mother-of-Learning'

# domain name
domain_name = 'https://royalroadl.com'

fictionpress_search = 'div'
fictionpress_attrs_1 = 'class'
fictionpress_attrs_2 = 'storytext xcontrast_txt nocopy'

# FictionPress Drop Down Parsing Variables
fictionpress_drop_tag_for_find_1 = 'select'
fictionpress_drop_tag_for_find_2 = 'chap_select'
fictionpress_drop_tag_options = 'option'

# WuxiaWorld variables
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


def selector_function(url):
    selector_variable = ''
    try:
        isinstance(url, str) == True
        if "royal" in url:
            selector_variable = "royal"

        elif "fictionpress" in url:
            selector_variable = "fictionpress"

        elif "wuxia" in url:
            selector_variable = "wuxiaworld"

    except:
        e = sys.exc_info()[0]
        print("Exception: " + str(e), file=sys.stdout)

    return selector_variable


def extract_urls(index_page):
    # create list to store urls FOR INDEX PAGES (e.x RoyalRoadl)
    list_of_urls = []

    try:
        fiction_index = urlopen(index_page)
    except IOError:
        print("URL malformed or not found", file=sys.stdout)

    soup = BeautifulSoup(fiction_index, 'html.parser')
    soup.prettify()
    # try to get urls from table
    table_content = soup.find('table', id='chapters')
    # get the rows
    for anchor in table_content.find_all('a', href=True, limit=5):
        list_of_urls.append(anchor.get('href'))

    return list_of_urls


def drop_down_parser(starting_page):
    # for use with drop down menu (FictionPress)

    try:
        initial_page = urlopen(starting_page)
    except IOError:
        print("URL malformed or not found", file=sys.stdout)

    soup = BeautifulSoup(initial_page, 'html.parser')
    soup.prettify()
    # figure out how many chapters there are by selecting whole menu first
    drop_down_content = soup.find(fictionpress_drop_tag_for_find_1,
                                  id=fictionpress_drop_tag_for_find_2)
    # then find all the "option" tags in the menu
    options = drop_down_content.find_all(fictionpress_drop_tag_options)
    # find the number of elements
    number_of_chaps = len(options)
    print("This fiction has " + str(number_of_chaps) + " chapters")

    return number_of_chaps


def fictionpress_loop_url(number_of_chapters):
    # small function for creating the list of URLs we are going to use
    fiction_list_of_urls = []
    loop_count = 1

    while loop_count <= number_of_chapters:
        fiction_list_of_urls.append(fictionpress_url_part_1 + str(
            loop_count) + fictionpress_url_part_3)
        loop_count += 1
        print(fictionpress_url_part_1 + str(
            loop_count) + fictionpress_url_part_3 + " added", file=sys.stdout)
    return fiction_list_of_urls


def url_generator(list_of_urls, location_selection):
    # counter variable
    i = 0

    # figure out what website we are at and act accordingly
    try:
        if location_selection == "royal":
            # turn list into useable links
            for url in list_of_urls:
                get_page_content((domain_name + url), royalroad_div,
                                 royalroad_attrs_1, royalroad_attrs_2)
                i += 1
                print("Content for chapter " + str(i) + " parsed \n",
                      file=sys.stdout)
                time.sleep(2)

        elif location_selection == "fictionpress":
            for url in list_of_urls:
                get_page_content(url, fictionpress_search,
                                 fictionpress_attrs_1, fictionpress_attrs_2)
                i += 1
                print("Content for chapter " + str(i) + " parsed \n",
                      file=sys.stdout)
                time.sleep(2)


    except:
        e = sys.exc_info()[0]
        print("Exception: " + str(e), file=sys.stdout)


def get_page_content(url, search_param, attr_1_param, attr_2_param):
    # query website and return html to variable 'page'
    page = urlopen(url)
    # parse html in page variable into BeautifulSoup format
    soup = BeautifulSoup(page, 'html.parser')

    # try to get the div with the content that we want
    page_content = soup.find(search_param, attrs={attr_1_param: attr_2_param})
    soup_text = page_content.get_text()

    # try and strip away the html leading and trailing the text
    stripped_content = re.sub(r'\<[^>]*\>', '', soup_text)

    # print statements (use command line to redirect this to txt file)
    print(stripped_content)


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

    with io.open(windows_write_file, 'w', encoding="utf-8") as f:
        f.write(content)
        safe_print(content)


if __name__ == '__main__':

    print(sys.argv)
    location = input("Which website?: ")
    location = selector_function(location)
    try:
        if location == "royal":
            list_of_urls = extract_urls(index_page_url)
            # this function calls get_page_content()
            url_generator(list_of_urls, location)
        elif location == "fictionpress":
            number_of_chapters = drop_down_parser(fictionpress_url)
            # print("drop_down_parser passed", file=sys.stdout)
            fiction_list_of_urls = fictionpress_loop_url(number_of_chapters)
            # print("fictionpress_loop_url passed", file=sys.stdout)
            url_generator(fiction_list_of_urls, location)
        # print("url generator and get_page_content passed", file=sys.stdout)
        elif location == "wuxiaworld":
            get_wuxia_content(req, search_param, attr_1_param, attr_2_param)

    except:
        e = sys.exc_info()[0]
        print("Exception: " + str(e), file=sys.stdout)

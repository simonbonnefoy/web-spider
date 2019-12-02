#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

import re


def is_link_from_domain(link):
    '''
    :param link:
    :return bool:
    function that checks if the link found belongs to the domain of the target url.
    retrun true is the link belongs to the same domain.
    '''

def join_url(link):
    return urljoin(target_url, link)

target_url = 'http://192.168.1.10/mutillidae/'

response = requests.get(target_url)
#print(response.text)
links = re.findall('(?:href=")(.*?)"',response.content.decode())
#print(links)
for url in links:
    if url and '#' not in url:
        url = join_url(url)
        print(url)
        if target_url in url:
            print('URL belongs to the target domain!')




#soup = bs(response.text, 'html.parser')
#print(soup.prettify())

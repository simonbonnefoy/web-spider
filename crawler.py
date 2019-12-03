#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import time
import re


def join_url(link):
    return urljoin(target_url, link)

#target_url = 'http://192.168.1.10/mutillidae/'
target_url = 'https://pharmacieagroparc.com/'
target_links = []
target_mails = []
def crawl(url):
    print('Crawling through %s'%url)
    response = requests.get(url)

    #retrieve all the links, from the href tag
    try:
        links = re.findall('(?:href=")(.*?)"',response.content.decode('cp1252'))
        #mails = re.findall(' *[\w_.\-]*@\w*.\w*',response.content.decode('cp1252'))
        mails = re.findall('[\w_.\-]{3,}@\w*.\w{2,}',response.content.decode('cp1252'))
        for mail in mails:
            if mail not in target_mails:
                print(mail, url)
                target_mails.append(mail)

        #regexp to search for mail. Match alphanum -_. chars @ alphanum.alphanum

        #loop over the links found in the page
        for link in links:

            #check if the link is not null
            if link and '#' not in link:

                #make sure the link is absolute
                link = join_url(link)
                #print(link)

                #Check if the link belongs to the domain
                if target_url in link and link not in target_links:

                    #for now, forget about the files
                    if '.ico' in link or '.pdf' in link:
                        continue

                    #add link to the list
                    target_links.append(link)
              #      print(url)

                    #Crawl the new link
                    crawl(link)
    except:
        pass



if __name__ == '__main__':
    crawl(target_url)
    print('Links found \n')
    for link in target_links:
        print(link)
    print('Mails found \n')
    for mail in target_mails :
        print(mail)





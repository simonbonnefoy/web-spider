#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import time
import re


class Crawler():
    def __init__(self, target_url, verbose=0):
        self.target_url = target_url
        self.target_files = []
        self.target_links = []
        self.target_mails = []
        self.verbose = verbose

    def join_url(self, link):
        return urljoin(target_url, link)

    def run(self):
        '''method to start crawling the web'''
        self.crawl(self.target_url)

    def crawl(self, url):
        '''method in charge of crawling the web'''
        if self.verbose == 1: print('Crawling through %s' %url)

        #retrieving the web page to check for elements
        response = requests.get(url)

        #retrieve all the links, from the href tag
        try:
            #get all the links according to the href balise
            links = re.findall('(?:href=")(.*?)"',response.content.decode('cp1252'))

            #regexp to search for mail. Match alphanum -_. chars @ alphanum.alphanum
            mails = re.findall('[\w_.\-]{3,}@\w*.\w{2,}',response.content.decode('cp1252'))

            #storing all the new mails found
            for mail in mails:
                if mail not in self.target_mails:
                    print(mail)
                    self.target_mails.append(mail)

            #loop over the links found in the page
            for link in links:

                #check if the link is not null
                if link and '#' not in link:

                    #make sure the link is absolute
                    link = self.join_url(link)

                    ##Check if the link belongs to the domain and not already registered
                    if self.target_url in link and link not in self.target_links:

                        #for now, forget about the files
                        if '.ico' in link or '.pdf' in link or '.jpg' in link:
                            if link not in self.target_files:
                                self.target_files.append(link)

                        #add link to the list
                        self.target_links.append(link)

                        #Crawl the new link
                        self.crawl(link)
        except:
            pass

    def get_summary(self):
        '''print summary of what was found'''
        self.get_links()
        self.get_mails()
        self.get_files()

    def get_links(self):
        '''print links found'''
        print('\n********************************* \n')
        print('Links found \n')
        for link in self.target_links:
            print(link)

    def get_mails(self):
        '''print mails found'''
        print('\n********************************* \n')
        print('Mails found \n')
        for mail in self.target_mails :
            print(mail)

    def get_files(self):
        '''print files found'''
        print('\n********************************* \n')
        print('Files found \n')
        for file in self.target_files :
            print(file)



if __name__ == '__main__':
    target_url = 'http://192.168.1.10/mutillidae/'
    #target_url = 'https://pharmacieagroparc.com/'

    verbose = 0
    crawler = Crawler(target_url, verbose)
    crawler.run()
    crawler.get_summary()






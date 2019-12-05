#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import time
import re
import shutil
import os

class Crawler():
    def __init__(self, target_url, verbose=0, dl_files=False, ext=[]):
        self._target_url = target_url
        self.target_files = []
        self.target_links = []
        self.target_mails = []
        self.verbose = verbose
        self.downloaded_files = []
        self.file_extension = ext
        self.dl_files = dl_files
        self.social_media = []
        self.use_file_extension = len(self.file_extension)>0
        print('Use file extension', len(self.file_extension),self.use_file_extension)
        print('verbose', self.verbose)

    def join_url(self, link):
        return urljoin(self._target_url, link)

    def set_target_url(self, target_url):
        self._target_url = target_url

    def run(self):
        '''method to start crawling the web'''
        self.crawl(self._target_url)

    def crawl(self, url):
        '''method in charge of crawling the web'''
        if self.verbose > 0:
            print('Crawling through %s' %url)

        #retrieving the web page to check for elements
        response = requests.get(url)
        if self.verbose > 2: print(response.text)
#        print(response.text)

        #retrieve all the links, from the href tag
        try:
            #get all the links according to the href balise
            #links = re.findall('(?:href="|\')(.*?)\'|"',response.content.decode('cp1252'))
            #this regexp deals with both simple and double quote around the link
            #############################################
       #     links = re.findall('(?:href=["\'])(.*?)["\']',response.content.decode('cp1252'))
            #############################################

            #############################################
            soup = bs(response.text, 'html.parser')
            links = []
            for link in soup.findAll(href=True):
                links.append(link.get('href'))
            #############################################



            if self.verbose > 1: print(links)

            #retrieving mails from the source code if any
            self.search_mails(response)

            #loop over the links found in the page
            for link in links:

                #check if the link is not null
                #if link and '#' not in link:
                if link:

                    #Check is link is from social media
                    if self.link_is_social_media(link) and link not in self.social_media_links:
                        self.social_media_links.append(link)

                    #make sure the link is absolute
                    link = self.join_url(link)

                    ##Check if the link belongs to the domain and not already registered
                    if self._target_url in link and link not in self.target_links:

                        #check if file is interesting or listing or download
                        if self.use_file_extension and self.check_file_extension(link) and link not in self.target_files:
                            print('Found interesting file')
                            #if link not in self.target_files:
                            self.target_files.append(link)
                            if self.dl_files:
                                self.download_file(link)
                       # elif '.pdf' in link:
                       #     if link not in self.downloaded_files:
                       #         print(link)

                        else:
                            #add link to the list
                            self.target_links.append(link)

                            #Crawl the new link
                            self.crawl(link)
        except:
            pass

    def search_mails(self, html_source):
        '''method to check for email address in the html source code'''
        # regexp to search for mail. Match alphanum -_. chars @ alphanum.alphanum
        # mails = re.findall('[\w_.\-]{3,}@\w*.\w{2,}',html_source.content.decode('cp1252'))
        mails = re.findall('[\w_.\-]{3,}@\w*.\w{2,}', html_source.content.decode())

        # storing all the new mails found
        for mail in mails:
            if mail not in self.target_mails:
                print(mail)
                self.target_mails.append(mail)

    def check_file_extension(self, url):
        '''Check if the file extension is interesting.'''
        for ext in self.file_extension:
            if ext in url:
                return True
        return False

    def link_is_social_media(self, link):
        if 'facebook.com' in link or 'instagram.com' in link or 'twitter.com' in link:
            if self.verbose > 0 : print('Found social media link: %s' %link)
            return True
        return False

    def download_file(self, url):
        #retrieving file name from url
        filename = os.path.basename(url)
        print('Downloading the file %s' %filename)

        #retrieving file source
        response = requests.get(url, stream=True)

        #creating file on local system
        local_file = open(filename,'wb')

        #set stream to True to return stream content
        response.raw.decode_content = True

        #copying file to local system
        shutil.copyfileobj(response.raw, local_file)

        #closing everything
        local_file.close()
        del response

        #add file to list of downloaded files
        self.downloaded_files.append(url)

   # def is_file(self, url):
   #     for ext in self.file_extension:
   #         if ext in url:
   #             return True

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

    def get_social_media(self):
        '''print social found'''
        print('\n********************************* \n')
        print('Social media found \n')
        for link in self.social_media:
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
    #target_url = 'http://192.168.1.10/mutillidae/'
    target_url = 'https://pharmacieagroparc.com/'

    verbose = 1
    crawler = Crawler(target_url, verbose)
    crawler.run()
    crawler.get_summary()






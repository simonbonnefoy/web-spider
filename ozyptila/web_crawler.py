from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re
import shutil
import os
import threading
import pycurl
import time
from io import BytesIO
import certifi
import definitions
import utilities

class WebCrawler:
    def __init__(self, target_url, download_extensions, verbose = 0):
        self._target_url = target_url
        self.target_files = []
        self.target_links = []
        self.target_mails = []
        self.verbose = verbose
        self.downloaded_extensions = download_extensions
        self.downloaded_files_list = []
        self.social_media_links = []

    def join_url(self, link):
        return urljoin(self._target_url, link)

    def set_target_url(self, target_url):
        self._target_url = target_url

    def run(self):
        '''method to start crawling the web'''
       # if self.verbose == 0:
       #     crawler_thread = threading.Thread(target=self.crawl, args = (self._target_url,))
       #     print_thread = threading.Thread(target=self.print_running, args=(crawler_thread,))
       #     crawler_thread.start()
       #     crawler_thread.join()
       #     print_thread.start()

       #     print_thread.join()

#        else:
        self.crawl(self._target_url)

    def print_running(self, thread):
        banner = ['|', '/', '-', "\\"]
        i = 0
       # while self.crawler_thread.isAlive():
        while True:
                print('Crawler is running %s' %banner[i%4], sep = '', end = '\r', flush=True)
                print(thread.isAlive())
                #print('Crawler is running %s' %banner[i%4])
                time.sleep(0.1)
                i += 1

#    def print_running2(self):
#        banner = ['|', '/', '-', "\\"]
#        i = 0
#        while i < 50:
#            print('Crawler is crawling %s' %banner[i%4], sep = '', end = '\r', flush=True)
#            time.sleep(0.1)
#            i += 1

    def crawl(self, url):
        '''method in charge of crawling the web'''

        if self.verbose > 0:
            print('Crawling through %s' %url)

        # The \x1b[2K\r is used to clean the line until the end, So we can print shorter string
        # and get rid of all the previous line
        print('%sCrawling through %s' % (utilities.ERASE_LINE,url), end='\r', flush=True)
        #retrieving the web page to check for elements
        buffer = BytesIO()
        requests = pycurl.Curl()
        requests.setopt(requests.URL, url)

        #Buffer where data will be writter
        requests.setopt(requests.WRITEDATA, buffer)

        #Follow if forward
        requests.setopt(requests.FOLLOWLOCATION, 1)

        #Add certificate if https
        if 'https' in url:
            requests.setopt(requests.CAINFO, certifi.where())
        #launch requests
        requests.perform()

        #cloase object
        requests.close()

        #store response in buffer object
        response = buffer.getvalue()

        if self.verbose > 2: print(response)

        #retrieve all the links, from the href tag
        try:
            #get all the links according to the href balises
            soup = bs(response, 'html.parser')
            links = []
            for link in soup.findAll(href=True):
                links.append(link.get('href'))

            if self.verbose > 1: print(links)

            #retrieving mails from the source code if any
            self.search_mails(response)

            #loop over the links found in the page
            for link in links:

                #check if the link is not null
                if link and '#' not in link:

                    #Check is link is from social media and append to list
                    self.search_social_media_link(link)

                    #make sure the link is absolute
                    link = self.join_url(link)

                    ##Check if the link belongs to the domain and not already registered
                    if self._target_url in link and link not in self.target_links:

                        #check if file is interesting or listing or download
                        if self.contains_file(link) and link not in self.target_files:
                            #if self.verbose > 1 : print('\033[KFound file %s' %link)
                            #print('\033[KFound file %s' %link)
                            print('%sFound file %s' %(utilities.CURSOR_UP_ONE,link))
                            self.target_files.append(link)
                            if len(self.downloaded_extensions) > 0 and link not in self.downloaded_files_list:
                                self.download_file(link)

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
        mails = re.findall('[\w_.\-]{3,}@\w*.\w{2,}', html_source.decode())

        # storing all the new mails found
        for mail in mails:
            if mail not in self.target_mails:
                #print('\033[K\nFound email %s \n' %mail)
                print('%s\nFound email %s \n' % (utilities.CURSOR_UP_ONE, mail))
                self.target_mails.append(mail)

    def contains_file(self, url):
        '''Check if the file extension is interesting.'''
        for ext in definitions.file_extension:
            if ext in url:
                return True
        return False

    def search_social_media_link(self, link):
            for social in definitions.social_media :
                if social in link and link not in self.social_media_links:
                    print('%s\nFound social media link %s\n' % (utilities.CURSOR_UP_ONE,link))
                    self.social_media_links.append(link)

    def download_file(self, url):
        #retrieving file name from url
        for ext in self.downloaded_extensions:
            if ext in url:
                #format the output directory, adding / removing dots
                ext_path = os.getcwd() + '/' + ext[1:]
                if os.path.exists(ext_path):
                    pass
                else:
                    os.makedirs(ext_path)

                #retrieving file name to download
                filename_to_dl = os.path.basename(url)

                #making file name on local server to download

                file_local =ext_path+'/'+filename_to_dl
                print('Downloading %s to  %s' %(filename_to_dl,file_local))

                #opening file descriptor to write file
                file_descriptor = open(file_local, "wb")

                #retrieving file source with pycurl
                requests = pycurl.Curl()
                requests.setopt(requests.URL, url)
                requests.setopt(requests.WRITEDATA, file_descriptor)

                #Follow if forward
                requests.setopt(requests.FOLLOWLOCATION, 1)

                #Add certificate if https
                if 'https' in url:
                    requests.setopt(requests.CAINFO, certifi.where())

                #launch requests
                requests.perform()
                #close objects
                requests.close()
                file_descriptor.close()

                #add downloaded file to the list
                self.downloaded_files_list.append(url)



    def get_summary(self):
        '''print summary of what was found'''
        self.get_links()
        self.get_mails()
        self.get_files()
        self.get_social_media()

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
        for link in self.social_media_links:
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


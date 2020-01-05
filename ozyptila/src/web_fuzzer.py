import queue
import threading
from multiprocessing.dummy import Pool
import copy
from io import BytesIO
import certifi
import sys
import pycurl
import src.utilities as utilities
import src.definitions as definitions
import time
from src.logger import web_fuzzer_logger
import src.logger as logger

class WebFuzzer():
    def __init__(self, target_url_list, wordlist, verbose=0):
        self.target_url_q = utilities.build_url_queue(target_url_list)
        self.wordlist = utilities.build_wordlist(wordlist)
        self.wordlist_queue = utilities.build_wordlist_queue(wordlist)
        self.wordlist_file = wordlist
        self.target_files = []
        self.verbose = verbose
        self.thread = []
        web_fuzzer_logger.setLevel(logger.level[self.verbose])

    def run(self, n_threads=1):
        """Method to run the web fuzzer on the website
        Implementation of multi threading to be checked"""

        while not self.target_url_q.empty():
           self.wordlist_queue = utilities.build_wordlist_queue(self.wordlist_file)
           url = self.target_url_q.get().rstrip()
           for i in range(n_threads):
               t = threading.Thread(target=self.fuzz, args=(url,))
               t.start()
               self.thread.append(t)

           for thread in self.thread:
               thread.join()
            # self.fuzz(self.target_url_q.get().rstrip())
            # self.fuzz()

        #    pool.close()
        #    pool.join()

    # def fuzz(self, url):
    def fuzz(self, url):
        """method that fuzzes the target web site"""
#        url = self.target_url_q.get().rstrip()


        # creating pycurl and buffer object
        # to send http(s) requests
        #buffer = BytesIO()
        requests = pycurl.Curl()

        # Looping over all the file names in the dictionnary
        # until queue is empty
        #for file in self.wordlist:
        while not self.wordlist_queue.empty():

            # get file name to test from list queue
            file = self.wordlist_queue.get().rstrip()

            # Check if url is / ended
            if url[-1] != '/': url += '/'

            # creating the url to check
            link = url + str(file.decode())
            web_fuzzer_logger.debug('testing %s' %link)
            #if self.verbose > 0: print(link)

            # set and sent get requests to link
           # requests.setopt(requests.WRITEDATA, buffer)
            requests.setopt(requests.CAINFO, certifi.where())

            #loop over the extensions defined in definitions.py
            for ext in definitions.web_page_extensions:
                link_with_extension = link + ext
                print('%sFuzzing on %s' % (utilities.ERASE_LINE, link_with_extension), end='\r', flush=True)
                requests.setopt(requests.URL, link_with_extension)
                buffer = BytesIO()
                requests.setopt(requests.WRITEDATA, buffer)
                requests.perform()

                # retrieve the body of the requets
                response = buffer.getvalue()

                # retrieving code response
                if requests.getinfo(requests.RESPONSE_CODE) != 404:
                    #print( '%s%s [code:%i, size:%i]' % (utilities.CURSOR_UP_ONE,link_with_extension,
                    #                                 requests.getinfo(requests.RESPONSE_CODE), sys.getsizeof(response)))
                    web_fuzzer_logger.info( '%s%s [code:%i, size:%i]' % (utilities.CURSOR_UP_ONE,link_with_extension,
                                                        requests.getinfo(requests.RESPONSE_CODE), sys.getsizeof(response)))

                    # add link to list of links found
                    if link not in self.target_files:
                        self.target_files.append(link)

                        # Add link the url queue to be fuzzed in some further rounds
                        self.target_url_q.put(link)

        # closing pycurl object
        requests.close()

    def add_known_links(self, known_links):
        """This method adds all the link already know from
        previous search to the queue"""

        # Check if object is a list or not, and convert it to good format
        if isinstance(known_links, str):
            known_links = [known_links]
        elif isinstance(known_links, list):
            pass

        # Fill the queue object with the urls already known
        for url in known_links:
            web_fuzzer_logger.info('Adding link to the fuzzer queue %s' % url)
            self.target_url_q.put(url)

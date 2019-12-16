import queue
import threading
from multiprocessing.dummy import Pool
import copy
from io import BytesIO
import certifi
import sys
import pycurl
import utilities


class WebFuzzer():
    def __init__(self, target_url_list, wordlist, verbose=0):
        self.target_url_q = utilities.build_url_q(target_url_list)
        self.wordlist = wordlist
        self.wordlist_q = utilities.build_wordlist(wordlist)
        self.target_files = []
        self.verbose = verbose

    def run(self):
        """Method to run the web fuzzer on the website
        Implementation of multi threading to be checked"""
        # for i in range (2):
        #    t = threading.Thread(target=self.fuzz(self.target_url))
        #    t.start()
        #    t.join()
        # Until queue is not empty, keep loopin on urls
        # while not self.target_url_q.empty():
        # self.fuzz(self.target_url_q.get().rstrip())

        # while not self.target_url_q.empty():
        #    pool = Pool(2)
        #    asyncresponse = pool.map(self.fuzz(self.target_url_q.get().rstrip()))
        #    pool.close()
        #    pool.join()

        while not self.target_url_q.empty():
           # for i in range(4):
           #     t = threading.Thread(target=self.fuzz())
           #     t.start()
           #     t.join()
            # self.fuzz(self.target_url_q.get().rstrip())
             self.fuzz()

        #    pool.close()
        #    pool.join()

    # def fuzz(self, url):
    def fuzz(self):
        """method that fuzzes the target web site"""
        url = self.target_url_q.get().rstrip()
        print('Fuzzing on %s' % url)
        # We need to recreate the queue everty time
        # since the get method remove items
        file_list_q = utilities.build_wordlist(self.wordlist)

        # creating pycurl and buffer object
        # to send http(s) requests
        buffer = BytesIO()
        requests = pycurl.Curl()

        # Looping over all the file names in the dictionnary
        # until queue is empty
        while not file_list_q.empty():
            # get file name to test from list queue
            file = file_list_q.get().rstrip()

            # Check if url is / ended
            if url[-1] != '/': url += '/'

            # creating the url to check
            link = url + str(file.decode())
            if self.verbose > 0: print(link)

            # set and sent get requests to link
            requests.setopt(requests.URL, link)
            requests.setopt(requests.WRITEDATA, buffer)
            requests.setopt(requests.CAINFO, certifi.where())
            requests.perform()

            # retrieve the body of the requets
            response = buffer.getvalue()

            # retrieving code response
            if requests.getinfo(requests.RESPONSE_CODE) != 404:
                print(
                    '%s [code:%i, size:%i]' % (link, requests.getinfo(requests.RESPONSE_CODE), sys.getsizeof(response)))

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
            print('Adding link to the queue %s' % url)
            self.target_url_q.put(url)
        # print(list(self.target_url_q.queue))

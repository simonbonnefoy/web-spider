import requests
import queue
import threading
from multiprocessing.dummy import Pool
import copy

class WebFuzzer():
    def __init__(self, target_url_list, wordlist):
        self.target_url_q = self.set_target_url_q(target_url_list)
        self.wordlist = wordlist
        self.wordlist_q = self.build_wordlist(wordlist)
        self.target_files = []

    def set_target_url_q(self, url_list):
        '''Set the queue for the urls already know of the target
        A string or a list can be given as parameter'''

        #Creating the Queue object
        target_url_queue = queue.Queue()

        #Check if object is a list or not, and convert it to good format
        if isinstance(url_list,str):
            url_list = [url_list]
        elif isinstance(url_list,list):
            pass

        #Fill the queue object with the urls already known
        for url in url_list:
            target_url_queue.put(url)

        #return the queue object containing the urls
        return target_url_queue

    def run(self):
        '''Method to run the web fuzzer on the website
        Implementation of multi threading to be checked'''
        #for i in range (2):
        #    t = threading.Thread(target=self.fuzz(self.target_url))
        #    t.start()
        #    t.join()
        #Until queue is not empty, keep loopin on urls
        while not self.target_url_q.empty():
            self.fuzz(self.target_url_q.get().rstrip())
            #pool = Pool(2)
            #asyncresponse = pool.map(self.fuzz(self.target_url_q.get().rstrip()))
            #pool.close()
            #pool.join()

    def fuzz(self, url):
        '''method that fuzzes the target web site'''
        #Looping over all the file names in the dictionnary
        #until queue is empty
        print(url)
        #url_list_q = copy.copy(self.wordlist_q)

        #We need to recreate the queue everty time
        #since the get method remove items
        url_list_q = self.build_wordlist(self.wordlist)
        while not url_list_q.empty():
            file = url_list_q.get().rstrip()

            #Check if url is / ended
            if  url[-1] != '/': url += '/'

            #creating the url to check
            link = url + str(file.decode())
            print(link)

            #Getting the link
            response = requests.get(link)

            #retrieving code response
            print(link, response.status_code)

    def add_known_links(self, known_links):
        '''This method gives all the link already know from
        previous search'''

        #Check if object is a list or not, and convert it to good format
        if isinstance(known_links,str):
            known_links = [known_links]
        elif isinstance(known_links,list):
            pass

        #Fill the queue object with the urls already known
        for url in known_links:
            print('Adding link to the queue %s' %url)
            self.target_url_q.put(url)
        #print(list(self.target_url_q.queue))


    def build_wordlist(self, wordlist_file):
        '''Method to set the dictionnary used to brute force
        directories in a Queue object for multi-threading'''

        print("Building the word list")
        # read in the word list
        fd = open(wordlist_file,"rb")
        raw_words = fd.readlines()
        fd.close()
        #found_resume = False
        words= queue.Queue()

        for word in raw_words:
            word = word.rstrip()
            words.put(word)
            #if self.resume is not None:
            #    if found_resume:
            #        words.put(word)
            #    else:
            #        if word == self.resume:
            #            found_resume = True
            #            print("Resuming wordlist from: %s" % self.resume)
            #else:
            #    words.put(word)

        return words

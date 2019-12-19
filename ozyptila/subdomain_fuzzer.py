from io import BytesIO
import certifi
import sys
import pycurl
import queue
import utilities
import threading
import time

class SubDomainFuzzer():
    def __init__(self, target_url, wordlist, verbose=0):
        self.target_url = target_url
        self.target_sub_domains = []
        self.wordlist_q = utilities.build_wordlist(wordlist)
        self.verbose =  verbose

    def run(self, n_threads=1):
        #run the subdomain fuzzer
        thread_list = []
        #for n_threads in range(8):
        for n in range (n_threads):
           thread = threading.Thread(target=self.fuzz_subdomain, args=(self.target_url,))
           thread.start()
        for thread in thread_list:
            thread.join()


    def print_num(self,i):
        for k in range(10):
            print('*'*i)
            time.sleep(i)
    def fuzz_subdomain(self, url):

        #creating pycurl object and buffer to store results
        buffer = BytesIO()
        requests = pycurl.Curl()

        #looping over subdomains
        while not self.wordlist_q.empty():

            #making the name of the subdomain
            sub_domain = self.wordlist_q.get().decode()
            sub_domain_url = self.create_subdomain(url, sub_domain)

            #Setting the pycurl object
            requests.setopt(requests.URL, sub_domain_url)
            requests.setopt(requests.WRITEDATA, buffer)
            requests.setopt(requests.CAINFO, certifi.where())

            #if self.verbose > 0 : print(sub_domain_url)
            print('%sFuzzing on %s' % (utilities.ERASE_LINE, sub_domain_url), end='\r', flush=True)

            #if the subdomain cannot be resolved, pycurl throws an error
            try:
                requests.perform()

                #retrieve the body of the requets
                response = buffer.getvalue()

                #retrieving code response
                if requests.getinfo(requests.RESPONSE_CODE) != 404:
                    print( '%s%s [code:%i, size:%i]' % (utilities.CURSOR_UP_ONE,sub_domain_url,
                                                        requests.getinfo(requests.RESPONSE_CODE), sys.getsizeof(response)))
                    #print('%s [code:%i, size:%i]' %(sub_domain_url, requests.getinfo(requests.RESPONSE_CODE), sys.getsizeof(response)))

                    # add link to list of links found
                    if sub_domain_url not in self.target_sub_domains:
                        self.target_sub_domains.append(sub_domain_url)

            except pycurl.error:
                continue

        #closing pycurl object
        requests.close()


    def create_subdomain(self, url, sub_domain):

        if self.target_url.startswith('https://'):
            sub_domain_url = self.target_url.replace('https://', 'https://%s.' % sub_domain)
            return sub_domain_url

        if self.target_url.startswith('http://www.'):
            sub_domain_url = self.target_url.replace('http://www.', 'http://%s.' % sub_domain)
            return sub_domain_url

        if self.target_url.startswith('http://'):
            sub_domain_url = self.target_url.replace('http://', 'http://%s.' % sub_domain)
            return sub_domain_url

        if self.target_url.startswith('https://www.'):
            sub_domain_url = self.target_url.replace('https://www.', 'https://%s.' % sub_domain)
            return sub_domain_url


    def get_summary(self):
        print('*******************************************')
        print('\nSubdmains found with status code != 404\n')
        print('*******************************************')
        for link in self.target_sub_domains:
            print(link)


#!/usr/bin/env python3
from web_crawler import WebCrawler
from web_fuzzer import WebFuzzer
import optparse
import os

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="target_url", \
            help="URL you want to start crawling from")

    parser.add_option("-c", "--crawl", dest="is_crawl", \
                      default = 1,\
                      help="Crawl the web site from the url.\n "
                       'Set to 0 if you don\'t want to crawl')

    parser.add_option("-f", "--fuzz", dest="is_fuzz_folders", \
                      help="Fuzz the folders with the given wordlist    \n\n "
                           "example: -f wordlist.txt")

    parser.add_option("-s", "--subdomains", dest="is_fuzz_subdomains", \
                      help="Fuzz subdomains with the given wordlist.       \n "
                        "example: -s wordlist.txt")
    parser.add_option("-v", "--verbose", dest="verbose", \
                      default = 0, \
            help="set the verbosity level (0,1,2,3)")

    parser.add_option("-d", "--download", dest="download_extension", \
                      default = '',\
                      help="Set the files extension you want to download \n "
                           "example: -x .jpg,.png,.pdf (default = none)")

    (options, arguments) = parser.parse_args()

    #check that extension are provided if download
#    if options.download_files and len(options.file_extension)==0:
#        print('--download needs to be provided with a file exentsion')
#        exit(0)

    return options


if __name__ == '__main__':
    # retrieving options
    options = get_arguments()
    #Converting the ext string into a list of string
    if options.download_extension:
        download_extensions = [str(i) for i in options.download_extension.split(',')]
    else:
        download_extensions = []

    #retrieve target url
    target_url = options.target_url
    is_crawl = int(options.is_crawl)
    folders_wordlist = options.is_fuzz_folders
    subdomains_wordlist = options.is_fuzz_subdomains

    #Set Verbose
    verbose = int(options.verbose)

    if is_crawl != 0:
        #Create Crawler object
        crawler = WebCrawler(target_url, download_extensions, verbose)

        #Start crawler
        crawler.run()

        #Retrieve info when crawler is done.
        crawler.get_summary()

        #list to store good links from crawler
        target_link_crawl = []

        #retrieving the good link from the crawler
        for link in crawler.target_links:
            # if the link is a file, i.e., last part contains a dot
            # we just take the dirname
            print(link)
            if link == target_url:
                pass
            else:
                if '.' not in os.path.basename(link) and '?' not in os.path.basename(link):
                    link = target_link_crawl.append(link)
                else:
                    link = os.path.dirname(link)
            print(link)
            #if link not present in the final list, we add it
            if link not in target_link_crawl:
                target_link_crawl.append(link)


    if folders_wordlist:
        folders_fuzzer = WebFuzzer(target_url, folders_wordlist, verbose)
        # w = WebFuzzer('https://pharmacieagroparc.com', 'common.txt')
        try:
            if target_link_crawl:
                folders_fuzzer.add_known_links(target_link_crawl)
                folders_fuzzer.run()
        except:
            folders_fuzzer.run()


    if subdomains_wordlist:
        w = WebFuzzer(target_url, subdomains_wordlist)
        # w = WebFuzzer('https://pharmacieagroparc.com', 'common.txt')
        w.run()



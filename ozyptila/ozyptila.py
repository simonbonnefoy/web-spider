#!/usr/bin/env python3
from web_crawler import WebCrawler
from web_fuzzer import WebFuzzer
from subdomain_fuzzer import SubDomainFuzzer
# import optparse
import argparse
import os


def get_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-u', '--url', dest='target_url',
                        help='Set the target url.')
    parser.add_argument("-c", "--crawl", dest="is_crawl",
                        default=False,
                        action='store_true',
                        help="Crawl the web site from the url. ")

    parser.add_argument("-f", "--fuzz", dest="is_fuzz_folders",
                        help="Fuzz the folders with the given wordlist    \n\n "
                             "example: -f wordlist.txt")

    parser.add_argument("-s", "--subdomains", dest="is_fuzz_subdomains",
                        help="Fuzz subdomains with the given wordlist.       \n "
                             "example: -s wordlist.txt")
    parser.add_argument("-v", "--verbose", dest="verbose",
                        default=0,
                        help="set the verbosity level (0,1,2,3)")

    parser.add_argument("-d", "--download", dest="download_extension",
                        default='',
                        help="Set the files extension you want to download \n "
                             "example: -x .jpg,.png,.pdf (default = none)")
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    # retrieving arguments
    arguments = get_arguments()
    # Converting the ext string into a list of string
    if arguments.download_extension:
        download_extensions = [str(i) for i in arguments.download_extension.split(',')]
    else:
        download_extensions = []

    # retrieve target url
    target_url = arguments.target_url
    is_crawl = arguments.is_crawl
    folders_wordlist = arguments.is_fuzz_folders
    subdomains_wordlist = arguments.is_fuzz_subdomains

    # Set Verbose
    verbose = int(arguments.verbose)

    if is_crawl:
        # Create Crawler object
        crawler = WebCrawler(target_url, download_extensions, verbose)

        # Start crawler
        crawler.run()

        # Retrieve info when crawler is done.
        crawler.get_summary()

        # list to store good links from crawler
        target_link_crawl = []

        # retrieving the good link from the crawler
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
            # if link not present in the final list, we add it
            if link not in target_link_crawl:
                target_link_crawl.append(link)

    if folders_wordlist:
        folders_fuzzer = WebFuzzer(target_url, folders_wordlist, verbose)
        try:
            if target_link_crawl:
                folders_fuzzer.add_known_links(target_link_crawl)
                folders_fuzzer.run()
        except:
            folders_fuzzer.run()

    if subdomains_wordlist:
        sub_domain_fuzz = Sub = SubDomainFuzzer(target_url, subdomains_wordlist, verbose)
        sub_domain_fuzz.run()

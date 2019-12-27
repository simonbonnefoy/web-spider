#!/usr/bin/env python3
from web_crawler import WebCrawler
from web_fuzzer import WebFuzzer
from subdomain_fuzzer import SubDomainFuzzer
import argparse
import os
import definitions


def get_arguments():
    parser = argparse.ArgumentParser(description='Ozyptilla help.')
    parser.add_argument('-u', '--url', dest='target_url',
                        help='Set the target url.')
    parser.add_argument("-c", "--crawl", dest="is_crawl",
                        default=False,
                        action='store_true',
                        help="Crawl the web site from the url. ")

    parser.add_argument("-f", "--fuzz", dest="is_fuzz_folders",
                        default=False,
                        action='store_true',
                        help="Fuzz the folders of the target url")

    parser.add_argument("-fd", "--folder-wordlist", dest="folders_wordlist",
                        help="Wordlist used to fuzz the folders    \n\n "
                             "example: -fd wordlist.txt")

    parser.add_argument("-s", "--subdomains", dest="is_fuzz_subdomains",
                        default=False,
                        action='store_true',
                        help="Fuzz subdomains with the given wordlist.       \n "
                             "example: -s wordlist.txt")

    parser.add_argument("-sd", "--subdomain-wordlist", dest="subdomains_wordlist",
                        help="Wordlist used to fuzz the folders    \n\n "
                             "example: -fd wordlist.txt")
    parser.add_argument("-v", "--verbose", dest="verbose",
                        default=0,
                        help="set the verbosity level (0,1,2,3)")

    parser.add_argument("-d", "--download", dest="download_extension",
                        default='',
                        help="Set the files extension you want to download \n "
                             "example: -x .jpg,.png,.pdf (default = none)")

    parser.add_argument("-j", "--threads", dest="n_threads",
                        default='1',
                        help="Number of parallel thread to throw\n")

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
    # check if crawling is requested
    is_crawl = arguments.is_crawl

    # check if folder fuzzer is requested
    is_fuzz_folders = arguments.is_fuzz_folders
    folders_wordlist = arguments.folders_wordlist

    # check if subdomain fuzzer is requested
    is_fuzz_sudbomains = arguments.is_fuzz_subdomains
    subdomains_wordlist = arguments.subdomains_wordlist

    # Get number of threads
    n_threads = int(arguments.n_threads)
    # Set Verbose
    verbose = int(arguments.verbose)

    # Creating list to store links and subdomains found
    links_found = []
    folders_found = []
    subdomains_found = []

    # Start the crawler if requested
    if is_crawl:
        # Create Crawler object
        crawler = WebCrawler(target_url, download_extensions, verbose)

        # Start crawler
        crawler.run()

        # Retrieve info when crawler is done.
        #crawler.get_summary()

        # Retrieve the links from the crawler
        links_found = crawler.target_links

    # Start the folders fuzzer if requested
    if is_fuzz_folders:

        # Create list to store folder from crawler to be used in folder fuzzer
        target_folder_crawl = []

        # retrieving the good link from the crawler to parse them to the
        # folder fuzzer
        if is_crawl:
            for link in links_found:

                # Check the links from the crawler to use them in the fuzzer
                if link == target_url:
                    pass
                else:
                    # if the link is a file, i.e., last part contains a dot
                    # we just take the dirname
                    if '.' not in os.path.basename(link) and '?' not in os.path.basename(link):
                        link = link
                    else:
                        link = os.path.dirname(link)

                # if link not present in the final list, we add it
                if link not in target_folder_crawl:
                    if verbose > 0:
                        print('Add link to the web fuzzer: %s' %link)
                    target_folder_crawl.append(link)

        folders_fuzzer = WebFuzzer(target_url, folders_wordlist, verbose)
        try:
            if target_link_crawl:
                folders_fuzzer.add_known_links(target_folder_crawl)
                folders_fuzzer.run(n_threads)
        except NameError:
            folders_fuzzer.run(n_threads)

        # Retrieve the folders from fuzz
        folders_found = folders_fuzzer.target_files

    # Start the subdomains fuzzer if requested
    if is_fuzz_sudbomains:
        subdomain_fuzz = SubDomainFuzzer(target_url, subdomains_wordlist, verbose)
        subdomain_fuzz.run(n_threads)

        # Retrieve the subdomain from fuzz
        subdomains_found = subdomain_fuzz.target_sub_domains

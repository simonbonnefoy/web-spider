#!/usr/bin/env python3
from web_crawler import WebCrawler
from web_fuzzer import WebFuzzer
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="target_url", \
            help="URL you want to start crawling from")
    parser.add_option("-v", "--verbose", dest="verbose", \
                      default = 0, \
            help="set the verbosity level (0,1,2,3)")
    parser.add_option("-d", "--download", action='store_true',
                      default = False, \
                      dest="download_files", \
                      help="Download the files found on the server, according"
                      "to the extension provided."
                      "Example: -d .jpg,.pdf")

    parser.add_option("-x", "--ext", dest="file_extension", \
                      default = '',\
                      help="Set the files extension you want to search \n "
                           "example: -x .jpg,.png,.pdf (default = all)")

    (options, arguments) = parser.parse_args()

    #check that extension are provided if download
    if options.download_files and len(options.file_extension)==0:
        print('--download needs to be provided with a file exentsion')
        exit(0)

    return options


if __name__ == '__main__':
    # retrieving options
    options = get_arguments()
    #Converting the ext string into a list of string
    if options.file_extension:
        extensions = [str(i) for i in options.file_extension.split(',')]
    else:
        extensions = []

    #retrieve target url
    target_url = options.target_url

    #Set option to download files
    dl_files = options.download_files

    #Set Verbose
    verbose = int(options.verbose)

    #Create Crawler object
    crawler = WebCrawler(target_url, verbose, dl_files, extensions)

    #Start crawler
    crawler.run()

    #Retrieve info when crawler is done.
    crawler.get_summary()

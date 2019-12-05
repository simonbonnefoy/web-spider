#!/usr/bin/env python3
from crawler import Crawler
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

    target_url = options.target_url
    #target_url = 'http://192.168.1.10/mutillidae/'
    #target_url = 'https://pharmacieagroparc.com/'

    dl_files = options.download_files
    verbose = int(options.verbose)
    crawler = Crawler(target_url, verbose, dl_files, extensions)
    crawler.run()
    crawler.get_summary()

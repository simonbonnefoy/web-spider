Ozyptila is a web spider and fuzzer.

Ozyptila crawls a web site from a starting url.
It analyses from the source code of the web pages the links present.
Ozyptilla will explore all the links found, recursively, until all the 
links have been analyzed. This allows to find some 'hidden' links, 
or links left in comments. 
Ozyptilla also searches for email, files and social network links.
Files from a given extension can be downloaded on the flight as ozyptilla is 
crawling the web.

Ozyptilla can also be used as a fuzzer.
You can fuzz the url of a web site, searching for hidden folders, files
and sudbomains.
You need to provide a wordlist in both case.
Multi-threading is implemented for the use of fuzzing.


################################

Get started

################################

To get started, create a new python environment and source it

    $ python3 -m venv env
    $ source env/bin/activate


Then clone the repository and run the Makefile

    $ git clone https://gitlab.com/sbonnefoy/web-spider.git
    $ cd ozyptilla
    $ make

This will install the dependencies required.
You can then run the different test to check the functionalities

    $make check

You can find out how to use ozyptilla:

    $ python3 ozyptila.py -h
    usage: ozyptila.py [-h] [-u TARGET_URL] [-c] [-f] [-fd FOLDERS_WORDLIST] [-s] [-sd SUBDOMAINS_WORDLIST] [-v VERBOSE] [-d DOWNLOAD_EXTENSION] [-j N_THREADS]

    Ozyptilla help

    optional arguments:
      -h, --help            show this help message and exit
     -u TARGET_URL, --url TARGET_URL
                             Set the target url.
    -c, --crawl           Crawl the web site from the url.
    -f, --fuzz            Fuzz the folders of the target url
    -fd FOLDERS_WORDLIST, --folder-wordlist FOLDERS_WORDLIST
                            Wordlist used to fuzz the folders example: -fd wordlist.txt
    -s, --subdomains      Fuzz subdomains with the given wordlist. example: -s wordlist.txt
    -sd SUBDOMAINS_WORDLIST, --subdomain-wordlist SUBDOMAINS_WORDLIST
                         Wordlist used to fuzz the folders example: -fd wordlist.txt
    -v VERBOSE, --verbose VERBOSE
                         set the verbosity level (0,1,2,3)
    -d DOWNLOAD_EXTENSION, --download DOWNLOAD_EXTENSION
                         Set the files extension you want to download example: -x .jpg,.png,.pdf (default = none)
    -j N_THREADS, --threads N_THREADS
                        Number of parallel thread to throw



Examples:

Crawl the mutillidae web site, with a bit more verbosity

    $ python3 web-crawler.py -u http://192.168.1.10/mutillidae/ -v 1

Crawl the mutillidae web site, with a bit more verbosity, requesting to
download .pdf files

    $ python3 web-crawler.py -u http://192.168.1.10/mutillidae/ -v 1 -d .pdf

#################################

Librairies needed:

    pip install bs4
    pip install pycurl
    pip install certifi
    pip install pytest




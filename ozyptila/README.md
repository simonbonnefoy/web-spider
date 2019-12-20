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
You can fuzz the url of a web site, searching for hidden folders of files
and for sudbomains.
You need to provide a wordlist in both case.
Multi-threading is implemented for the use of fuzzing.

Find out how to use it with:
python3 ozyptila.py -h

Examples:
Crawl the mutillidae web site, with a bit more verbosity
$ python3 web-crawler.py -u http://192.168.1.10/mutillidae/

Crawl the mutillidae web site, with a bit more verbosity, requesting to
download .pdf files
$ python3 web-crawler.py -u http://192.168.1.10/mutillidae/ -v 1 -x .pdf -d


Makefile:
A Makefile is present in the project. It will install all 
the required dependencies for you, and run some test (to be done)

#################################

Librairies needed:

pip install bs4
pip install pycurl
pip install certifi




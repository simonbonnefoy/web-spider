Ozyptila is a web spider, or crawler

Ozyptila crawls the web site from a startin url you have to provided.
I can identify files, according to the extension that you have to specify, 
and download them for you. 
It can also find the email address present in the source code of the pages, 
and report about social network links found.


Find out how to use it with:
python3 ozyptila.py -h

Examples:
Crawl the mutillidae web site, with a bit more verbosity
$ python3 web-crawler.py -u http://192.168.1.10/mutillidae/ -v 1

Crawl the mutillidae web site, with a bit more verbosity, asking to consider
.pdf files as distinct, and download them.
$ python3 web-crawler.py -u http://192.168.1.10/mutillidae/ -v 1 -x .pdf -d


Librairies needed:

pip install beautifulsoup4


************************************************************************
Additional documentation (for futur implementation?).
Download images with python
https://www.dev2qa.com/how-to-download-image-file-from-url-use-python-requests-or-wget-module/


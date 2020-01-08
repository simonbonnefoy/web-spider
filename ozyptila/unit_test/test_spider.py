import pytest
import sys
import os
'''This is to add the location of the modules, so they can be imported
Maybe using the PYTHONPATH would be better, but not working so far'''
from pathlib import Path
folder = os.path.dirname(os.getcwd())
sys.path.append(folder)

#Now the module can be imported
from src.web_crawler import WebCrawler
from src.web_fuzzer import WebFuzzer
from src.subdomain_fuzzer import SubDomainFuzzer


def test_spider():
    crawler = WebCrawler('https://example.com/', '', 1)

    # Start crawler
    assert None == crawler.run()

def test_web_fuzzer():
    folders_fuzzer = WebFuzzer('https://example.com', './test_wordlist.txt', 0)
    assert None == folders_fuzzer.run(4)

def test_subdomain_fuzzer():
    subdomain_fuzz = SubDomainFuzzer('htps://example.com', './test_wordlist.txt', 0)
    assert None == subdomain_fuzz.run(2)


import pytest
from src.web_crawler import WebCrawler
from src.web_fuzzer import WebFuzzer
from src.subdomain_fuzzer import SubDomainFuzzer



def test_spider():
    crawler = WebCrawler('https://example.com/', '', 1)

    # Start crawler
    assert None == crawler.run()

def test_web_fuzzer():
    folders_fuzzer = WebFuzzer('https://example.com', './unit_test/test_wordlist.txt', 0)
    assert None == folders_fuzzer.run(4)

def test_subdomain_fuzzer():
    subdomain_fuzz = SubDomainFuzzer('htps://example.com', './unit_test/test_wordlist.txt', 0)
    assert None == subdomain_fuzz.run(2)


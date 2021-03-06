#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""crtsh.py - This script allows you to get domains and subdomains related to
a company/parent domain based on SSL Certfications at crt.sh
"""

__author__ = "ESBarto"
__license__ = "GPL"

# Python standard libraries
from requests.sessions import Session
from collections import OrderedDict
from bs4 import BeautifulSoup
from argparse import ArgumentParser


# Site to scrap and headers
SITE = "https://crt.sh/"
DEFAULT_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) \
Gecko/20100101 Firefox/68.0"
DEFAULT_HEADERS = OrderedDict(
    (
        ("User-Agent", DEFAULT_AGENT),
        ("Accept-Encoding", "gzip, deflate, br"),
        ("Accept-Language", "en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6")
    )
)


class crt_handler(Session):
    """crt_handler manage requests and BeautifulSoup
    to scrap and get tables information in site response

    :param proxy: An optional proxy (https://127.0.0.1:8080)
    :type proxy: str
    """
    def __init__(self, proxy: str = None):
        super().__init__()

        self.headers = DEFAULT_HEADERS
        self.proxies = {
            'http': proxy,
            'https': proxy
        }
    
    def get_subdomains(self, parent_domain: str) -> set:
        """Sends request to crt site and scrapes to
        find subdomains in response html

        :param domain: Domain to get info
        :type domain: str

        :returns: domains:
        :rtype: set
        """
        domains = set()

        params = {"q": parent_domain}
        with self.get(SITE, params=params) as response:
            soup = BeautifulSoup(response.content, "html.parser")
            table_contents = soup.find_all("table")

            if table_contents:
                table_contents = table_contents[2].find_all("tr")

            for row_contents in table_contents:
                site_box = row_contents.find_all("td")
                if site_box:
                    domain = site_box[4].get_text(' ').split()
                    [domains.add(d.replace('*.', '')) for d in domain if parent_domain in d]
        
        return domains
    
    def print_domains(self, domains: set) -> None:
        """Prints domains on screen
        
        :param domains: A set of domains
        :type domains: set
        """
        for domain in domains:
            print(domain)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--domain", help="A valid domain name (example.com)")

    args = parser.parse_args()

    handler = crt_handler()
    domains = handler.get_subdomains(args.domain)
    handler.print_domains(domains)

#%%
'''------- imports -------'''
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd


'''------- globals -------'''
bulbapedia_base_url = 'https://bulbapedia.bulbagarden.net'
bulbapedia_sets_url = bulbapedia_base_url + '/wiki/List_of_Pok%C3%A9mon_Trading_Card_Game_expansions'


'''------- classes -------'''
class Soup:
    """
    A class representing the bs4.BeautifulSoup object scraped from a webpage

    Attributes
    ----------
    soup : bs4.BeautifulSoup
        Represents the soup itself

    Methods
    -------
    expansion_names()
        Returns a list of expansion names from the bulbapedia sets url
    table_after_h2(span_id)
        Returns the table element immediately after a span element with a specified id. The
        format of interest is <h2><span id=span_id></span></h2><table>...
    """

    def __init__(self, soup):
        self.soup = soup

    def expansion_names(self):
        expansions_names = []
        for el in self.soup.find_all('span', class_='mw-headline'):
            element_id = el.get('id')
            expansions_names.append(element_id)
        return expansions_names

    def table_after_h2(self, span_id):
        """
        Args
        ----
        span_id : str
            The id of a span element within an h2 tag preceding the table of interest
        """
        h2_element = self.soup.find('span', id=span_id).parent
        # The <table> containing all sets will appear directly beneath the <h2> tag containing
        # the expansion name
        next_table = h2_element.findNext('table')
        return next_table


'''------- functions -------'''
def url_to_soup(url: str):
    """
    Accepts a url and returns the scraped BeautifulSoup soup using html.parser.
    Args:
        url (str): The url whose content you wish to scrape
    Returns:
        soup: A bs4.BeautifulSoup class containing the html content of the url
    """
    request = requests.get(url, verify=False)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def set_names_and_urls(bs4_table):
    """
    Parses through a <table> element and extracts the set name and url on Bulbapedia
    Args:
        bs4_table: A bs4.BeautifulSoup object representing the table of interest
    Returns:
        set_names_and_urls_dict (dict): A dictionary with the set name and url
    """
    set_hypertext_tags = bs4_table.find_all(title=re.compile('(TCG)'))
    set_names = [el.string for el in set_hypertext_tags]
    set_urls = [el['href'] for el in set_hypertext_tags]
    set_names_and_urls_dict = {}
    set_names_and_urls_dict['set_names'] = set_names
    set_names_and_urls_dict['set_urls'] = set_urls
    return set_names_and_urls_dict


# def card_name_and_num(bs4_table):
    # TODO: search td.strings for a '/'. Then find card somehow, maybe a regex looking
    # for open and close parentheses?


'''------- script -------'''
soup = url_to_soup(bulbapedia_sets_url)
bulbapedia_expansions_soup = Soup(soup)
expans_names = bulbapedia_expansions_soup.expansion_names()
expansions_dict = {}
for expansion in expans_names:
    bs4_table = bulbapedia_expansions_soup.table_after_h2(span_id = expansion)
    sets_and_urls = set_names_and_urls(bs4_table)
    expansions_dict[expansion] = sets_and_urls
print(expansions_dict)
# %%

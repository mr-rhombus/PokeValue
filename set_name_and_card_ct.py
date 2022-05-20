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

class Set:
    """
    A class representing a Pokemon Card set

    Attributes
    ----------
    name : str
        Name of the set
    url : str
        URL to page on Bulbapedia site
    expansion: str
        The expansion the set belongs to
    card_ct: int
        The number of cards in the set
    """

    def __init__(self, name, url, expansion, card_ct):
        self.name = name
        self.url = bulbapedia_base_url + url
        self.expansion = expansion
        self.card_ct = card_ct


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
    hypertext_tags = bs4_table.find_all(title=re.compile('(TCG)'))
    names = [el.string for el in hypertext_tags]
    url_extensions = [el['href'] for el in hypertext_tags]
    names_and_url_extensions = dict(zip(names, url_extensions))
    return names_and_url_extensions


# def card_name_and_num(bs4_table):
    # TODO: search td.strings for a '/'. Then find card somehow, maybe a regex looking
    # for open and close parentheses?


'''------- script -------'''
soup = url_to_soup(bulbapedia_sets_url)
bulbapedia_expansions_soup = Soup(soup)
expans_names = bulbapedia_expansions_soup.expansion_names()
sets = {}
for expansion in expans_names:
    expansion_tbl = bulbapedia_expansions_soup.table_after_h2(span_id = expansion)
    names_and_url_extensions = set_names_and_urls(expansion_tbl)
    for k,v in names_and_url_extensions.items():
        new_set = Set(k, v, expansion, 'N/A')
        sets[k] = new_set

base_set = sets['Base Set']
base_set_soup = url_to_soup(base_set.url)
x = base_set_soup.find_all(string=re.compile('^\d+\/\d+$'), limit=1)  # Match first #/### instance
card_ct = x[0].strip()
base_set.card_ct = card_ct
print(base_set.card_ct)
# TODO: Update __repr__ dunder method to print name, expansion, card ct
# %%

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

    def __str__(self):
        return f'The {self.name} has {self.card_ct} cards, and is part of {self.expansion}'


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

def card_count(set_: Set) -> int:
    """
    Takes a Set object and returns the card count in the set
    Args:
        set (Set): A set object representing an expansion set scraped from Bulbapedia
    Returns:
        card_ct (int): The total # of cards in the set
    """
    soup = url_to_soup(set_.url)
    card_num = soup.find_all(string=re.compile('^\d+\/\d+$'), limit=1)  # Match first #/### instance
    try:
        card_ct = card_num[0].strip().split('/')[1]
    # HACK: Handles sets with no card counts in Bulbapedia page
    except:
        card_ct = None
    return card_ct

def card_names(set_: Set):
    soup = url_to_soup(set_.url)
    name = set_.name



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

# for set_ in sets.values():
#     set_.card_ct = card_count(set_)

# TODO: Drill down to get card name and num. Search for "Set list(s)" h2. Span id = "Set_list(s)",
# then grab following table -> use table_after_h2 fn. Then walk through table and apply #/###
# pattern!

print(sets['Base Set'])
# %%

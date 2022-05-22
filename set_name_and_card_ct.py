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
class WebpageSoup:
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
        re_match = f'{span_id}.*?'
        h2_element = self.soup.find('span', id=re.compile(re_match)).parent
        # The <table> containing all sets will appear directly beneath the <h2> tag containing
        # the expansion name
        next_table = h2_element.findNext('table')
        return next_table


class TableSoup:
    """
    A class representing the bs4.BeautifulSoup object of a table element

    Attributes
    ----------
    table : bs4.BeautifulSoup
        The table element

    Methods
    -------
    set_names()
        Returns a list of set names from a table on the Bulbapedia expansions page
    url_extensions()
        Returns a list of set url extensions from a table on the Bulbapedia expansions page
    """
    def __init__(self, table):
        self.table = table
    
    def set_names(self) -> str:
        hypertext_tags = self.table.find_all(title=re.compile('(TCG)'))
        names = [el.string for el in hypertext_tags]
        return names

    def url_extensions(self) -> str:
        hypertext_tags = (self.table.find_all(title=re.compile('(TCG)')))
        url_extensions = [el['href'] for el in hypertext_tags]
        return url_extensions


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

    def __repr__(self):
        return self.name


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


'''------- script -------'''
homepage_soup = url_to_soup(bulbapedia_sets_url)
homepage = WebpageSoup(homepage_soup)
expans_names = homepage.expansion_names()
sets = {}

for expansion in expans_names:
    expansion_table = homepage.table_after_h2(span_id = expansion)
    table_soup = TableSoup(expansion_table)
    set_names = table_soup.set_names()
    url_extensions = table_soup.url_extensions()
    names_and_url_extensions = dict(zip(set_names, url_extensions))
    for set_,ext in names_and_url_extensions.items():
        url = bulbapedia_base_url + ext
        new_set = Set(name=set_, url=url, expansion=expansion, card_ct='N/A')
        sets[set_] = new_set

# # for set_ in sets.values():
# #     set_.card_ct = card_count(set_)

# # TODO: Create card class to capture name and num (and eventually price?). Turn card finder
# # into a function. Maybe turn table into a class with "find_sets" and "find_cards" as methods?
# set_ = sets['Base Set']
# set_name = set_.name
# set_url = set_.url
# set_soup = Soup(url_to_soup(set_url))
# cards_tbl = set_soup.table_after_h2(span_id = 'Set_list')
# cards = cards_tbl.find_all('a', title = re.compile(set_name))
# for card in cards:
#     # title="<card_name> (set_name <card_num>)"
#     title = card['title']
#     title_split = title.split('(')
#     card_name = title_split[0][:-1]
#     card_num = re.search('\d+', title_split[1].replace(')', ''))[0]
#     print(card_name, card_num)
# %%

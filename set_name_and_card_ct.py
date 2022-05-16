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


def expansions_names(soup):
    """
    Accepts the soup scraped from bulbapedia_sets_url and returns a list of expansion names.
    Args:
        soup: The soup scraped from bulbapedia_sets_url
    Returns:
        expansions_names (list): A list of expansion names
    """
    expansions_names = []
    for el in soup.find_all('span', class_='mw-headline'):
        element_id = el.get('id')
        expansions_names.append(element_id)
    return expansions_names


def table_after_h2(soup, span_id: str):
    """
    Accepts the soup scraped from the bulbapedia_sets_url and returns following table
    element. The format of interest here is <h2><span id=span_id></span></h2><table>...
    Args:
        soup: The soup scraped from the bulbapedia url
        span_id: The id of the span within the h2 tag preceding the table of interest
    Returns:
        next_table: A bs4.BeautifulSoup class containing the table element of interest

        set_names_and_urls (dict): A dictionary of the form {'set_names': [set1, set2, ...], 
        'set_urls': [url1, url2, ...]}
    """
    # Find the header with the expansion name in it
    h2_element = soup.find('span', id={span_id}).parent
    # The <table> containing all sets will appear directly beneath the <h2> tag containing
    # the expansion name
    next_table = h2_element.findNext('table')
    return next_table


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


def card_name_and_num(bs4_table):
    # TODO: search td.strings for a '/'. Then find card somehow, maybe a regex looking
    # for open and close parentheses?


'''------- script -------'''
soup = url_to_soup(bulbapedia_sets_url)
expans_names = expansions_names(soup)
expansions_dict = {}
for expansion in expans_names:
    bs4_table = table_after_h2(soup, expansion)
    sets_and_urls = set_names_and_urls(bs4_table)
    expansions_dict[expansion] = sets_and_urls
print(expansions_dict)
# %%

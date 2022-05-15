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


def expansion_set_names_and_urls(soup, expansion_name) -> dict:
    """
    Accepts the soup scraped from the bulbapedia_sets_url and returns a list of set names in
    the given expansion.
    Args:
        soup: The soup scraped from the bulbapedia url
    Returns:
        set_names_and_urls (dict): A dictionary of the form {'set_names': [set1, set2, ...], 
        'set_urls': [url1, url2, ...]}
    """
    # Find the header with the expansion name in it
    expansion_name_h2 = soup.find('span', id=expansion_name).parent
    # The <table> containing all sets will appear directly beneath the <h2> tag containing
    # the expansion name
    expansion_set_table = expansion_name_h2.findNext('table')
    set_hypertext_tags = expansion_set_table.find_all(title=re.compile('(TCG)'))
    set_names = [el.string for el in set_hypertext_tags]
    set_urls = [el['href'] for el in set_hypertext_tags]
    set_names_and_urls = {}
    set_names_and_urls['set_names'] = set_names
    set_names_and_urls['set_urls'] = set_urls
    return set_names_and_urls


'''------- script -------'''
soup = url_to_soup(bulbapedia_sets_url)
expans_names = expansions_names(soup)
expansions_dict = {}
for expansion in expans_names:
    set_names_and_urls_dict = expansion_set_names_and_urls(soup, expansion)
    expansions_dict[expansion] = set_names_and_urls_dict
print(expansions_dict)
# %%

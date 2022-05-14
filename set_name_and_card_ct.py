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
    Accepts a url and returns the scraped BeautifulSoup soup using html.parser
    Args:
        url (str): The url whose content you wish to scrape
    Returns:
        soup (): 
    """
    requests = requests.get(sets_url, verify=False)
    soup = BeautifulSoup(requests.text, 'html.parser')
    return soup


'''------- script -------'''
x = url_to_soup(bulbapedia_sets_url)
print(x)
# %%

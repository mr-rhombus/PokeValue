#%%
'''------- imports -------'''
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd
import warnings
import os
warnings.filterwarnings('ignore')


'''------- globals -------'''
set_and_card_ct = pd.read_excel('Set_and_Card_Ct.xlsx', index_col=0)


'''------- code -------'''
card_db = pd.DataFrame()

def card_value():
    tmp_row = pd.DataFrame()  # to be appended to card_db
    
    card_name_full = input("Enter the Pokemon name EXACTLY as shown (ex. Charizard ex): ")
    card_and_set_num = input("Enter the card number and set number found at the bottom of the card \
                        Exactly as shown (ex. 4/130): ")
#     card_feats = input("Does the card have any special features - EX, G LV X, First Edition, Shadowless? ")
#     card_mega = input("Is the card a Mega Evolution? ")
#     return card_name_full, card_and_set_num #, card_feats, card_mega
    card_num = card_and_set_num.split('/')[0]
    set_num = int(card_and_set_num.split('/')[1])
    
    # determine which set(s) correspond to the the card count
    potential_sets = [el.replace(' ','-') for el in list(set_and_card_ct[set_and_card_ct['Card Count'] == set_num]['Set Name'])]

    url_list = [f"https://www.pricecharting.com/game/pokemon-{set_}/{card_name_full}-{card_num}"
                for set_ in potential_sets]
    for url in url_list:
        r = requests.get(url, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        try:
            price = [el.text.strip() for el in soup.select('#used_price > .js-price')][0]
        except: pass
    print(f'Your {card_name_full.title()}, ungraded, is worth up to {price}!')
    
#     # append to card db
#     tmp_row['Card Name'] = card_name_full.title()
#     tmp_row['Card and Set Number'] = card_and_set_num
#     tmp_row['Est. Ungraded Price'] = f'${price}'
#     card_db.append(tmp_row)

card_value()
#%%
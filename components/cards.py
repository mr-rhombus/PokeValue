import os
from lxml.cssselect import CSSSelector

import constants
from components import web


class Expansion:
    def __init__(self, name, url, set_count, cards):
        self.name = name
        self.url = url
        self.set_count = set_count
        self.cards = cards

    def __str__(self):
        return f'The {self.name} expansion has {self.set_count} cards'

    def get_pictures(self):
        expansion_slug = self.name.lower().replace(' ', '-')
        pkmncards_expansion_url = os.path.join(constants.pkmncards_base_url, 'set', expansion_slug)
        pkmncards_soup = web.Soup(pkmncards_expansion_url)
        sel = CSSSelector('img.card-image')
        x = [el.get('src') for el in sel(pkmncards_soup)]
        print(x)
        for card in self.cards:
            pass


    def to_excel(self):
        '''
        cols
        - expansion name
        - expansion card ct
        - card name
        - card #
        - url to picture?
        '''
        pass


class Card:
    """Represents an individual pokemon card. Comprised of the card name, card number, and total number of cards in the set (excluding "special" types of rare cards)
    """
    def __init__(self, name, card_number, set_count):
        self.name = name
        self.card_number = card_number
        self.set_count = set_count

    def __str__(self):
        return f'{self.name} {self.card_number}/{self.set_count}'
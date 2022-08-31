import requests, re
requests.packages.urllib3.disable_warnings()
from etl_helpers import web_elements

bulbapedia_base_url = 'https://bulbapedia.bulbagarden.net'
bulbapedia_sets_url = bulbapedia_base_url + '/wiki/List_of_Pokémon_Trading_Card_Game_expansions'


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

    def set_urls(self) -> str:
        hypertext_tags = (self.table.find_all(title=re.compile('(TCG)')))
        urls = [el['href'] for el in hypertext_tags]
        return urls


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
    def __init__(self, name, url, expansion, card_ct, cards):
        self.name = name
        self.url = bulbapedia_base_url + url
        self.expansion = expansion
        self.card_ct = card_ct
        self.cards = cards

    def __repr__(self):
        return self.name


class Card:
    """
    A class representing an individual Pokemon card

    Attributes
    ----------
    name : str
        The card name
    number : int
        The card number
    set_ct : int
        The number of cards in the set the card belongs to
    set_name : str
        The name of the set the card belongs to
    expansion_name : str
        The name of the expansion the card belongs to
    """
    def __init__(self, name, number, set_ct, set_name, expansion_name):
        self.name = name
        self.number = number
        self.set_ct = set_ct
        self.set_name = set_name
        self.expansion_name = expansion_name

    def __repr__(self):
        return f'{self.name} {self.number}/{self.set_ct}'


'''------- functions -------'''


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

def get_cards(table_soup, set_name: str) -> dict:
    """
    Accepts a TableSoup object and parses it for the list of card anchor tags

    As referenced below, "title" appears like "<card_name> (<set_name> <card_num>)"
    """
    cards = table_soup.table.find_all('a', title = re.compile(set_name))
    for card in cards:
        try:
            title = card['title']
            title_split = title.split('(')
            card_name = title_split[0].strip()
            set_and_num_clean = title_split[1].replace(')', '').replace(set_name, '')
            card_num = re.search('\d+', set_and_num_clean)[0]
            new_card = Card(
                name=card_name, number=card_num, set_ct=card_ct, set_name=set_.name, expansion_name=set_.expansion
            )
            yield new_card
        # HACK: Handles table elements with both EN and JP table element children. The JP table
        # elements do not have card #s, so the card_num line will fail otherwise.
        except TypeError:
            break


'''------- script -------'''
# homepage_soup = url_to_soup(bulbapedia_sets_url)
# homepage = WebpageSoup(homepage_soup)
# expans_names = homepage.expansion_names()
# sets = {}

# TODO: Pick up here
# for expansion in expans_names:
#     expansion_table = homepage.table_after_h2(span_id=expansion)
#     table_soup = TableSoup(expansion_table)
#     set_names = table_soup.set_names()
#     urls = table_soup.set_urls()
#     names_and_urls = dict(zip(set_names, urls))
#     for set_,url in names_and_urls.items():
#         new_set = Set(name=set_, url=url, expansion=expansion, card_ct=None, cards={})
#         sets[set_] = new_set

# TODO: create expansion class, add Set obj maybe?
# BUG: some card #s are TG## (ex. Brilliant Stars)
# TODO: check all card counts to make sure they're formatted correctly
# TODO: store in csv

# for set_ in sets.values():
#     if set_.expansions == 'Main_expansions':
#         card_ct = card_count(set_)
#         set_.card_ct = card_ct
#         set_name = set_.name
#         set_url = set_.url
#         response = requests.get(set_url, verify=False)
#         # Handle status_code >200
#         if not response.ok:
#             print(f'{response.json} for {set_.name}')
#         else:
#             set_soup = WebpageSoup(url_to_soup(set_url))
#             cards_table = set_soup.table_after_h2(span_id = 'Set_list')
#             cards_soup = TableSoup(cards_table)
#             cards = get_cards(cards_soup, set_.name)
#             for card in cards:
#                 set_.cards[card.name] = card
#             print(f'{set_} card extraction complete.')


# def main():
homepage = web_elements.url_to_soup(bulbapedia_sets_url)
homepage = web_elements.WebpageSoup(homepage)

print(homepage.soup)

for el in homepage.find_all('span', class_='mw-headline'):
    print(el.get('id'))
expansion_names = homepage.expansion_names()
for el in expansion_names:
    print(el)




# if __name__ == '__main__':
#     main()
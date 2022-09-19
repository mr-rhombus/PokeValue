import requests
from lxml import etree

from components.cards import Card, Expansion
import constants


serebii_base_url = 'https://www.serebii.net'


class Soup:
    def __init__(self, url):
        self.url = url
        self.r = requests.get(self.url, verify=False)
        self.html = etree.HTML(self.r.text)


class AllSetsPage(Soup):
    def __init__(self, url):
        super().__init__(url)

    def get_expansion_names_and_urls(self):
        locator = "//tr/td/a"
        matches = self.html.xpath(locator)
        # Only want match to expansion name not expansion logo
        expansions = [a for a in matches if matches.index(a)%2==0]
        names = [a.text for a in expansions]
        urls = [constants.serebii_base_url + a.attrib['href'] for a in expansions]
        return [Expansion(name=name, url=url, card_count=None, cards=None) for name,url in zip(names, urls)]


class SetPage(Soup):
    def __init__(self, url):
        super().__init__(url)
        self.card_row_locator = "//tr/td[contains(text(), '/')]/.."
        self.set_number_locator = "//tr/td[contains(text(), '/')]/text()"  # find "# / # "

    @property
    def set_count(self):
        # Only grab the first match
        set_number = self.html.xpath(self.set_number_locator)[0]
        set_count = set_number.split('/')[-1].strip()
        return set_count

    def get_card_num_and_set_count(self, row):
        set_number = row.xpath(self.set_number_locator)[0]
        (card_num,set_count) = [el.strip() for el in set_number.split('/')]
        return card_num, set_count

    def get_card_name(self, row):
        pokemon_name = row.xpath(".//td[@width='20%']/a/font/text()")[0]
        extra_names = row.xpath(".//td[@width='20%']/a/text()")
        preceding_name,proceeding_name = self.clean_additional_card_names(extra_names)
        return preceding_name + pokemon_name + proceeding_name

    def clean_additional_card_names(self, extra_card_names: list):
        preceding_name = ''
        proceeding_name = ''
        for name in extra_card_names:
            # Blank preceding name - appears as ' ' for cards with no preceding name
            if len(name.strip()) == 0:
                continue
            # Get preceding name - ex. 'Hisuian '
            elif name[-1] == ' ':
                preceding_name = name
            # Get proceeding name - ex. ' VMAX'
            elif name[0] == ' ':
                proceeding_name = name
        return preceding_name, proceeding_name


    def get_cards(self):
        rows = self.html.xpath(self.card_row_locator)
        cards = [Card(self.get_card_name(row), self.get_card_num_and_set_count(row)) for row in rows]
        return cards
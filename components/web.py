import requests
from lxml import etree
from io import StringIO
from bs4 import BeautifulSoup

from components import cards


class Soup:
    def __init__(self, url):
        self.url = url
        self.r = requests.get(self.url, verify=False)
        self.soup = BeautifulSoup(self.r.text, 'html.parser')
        self.tree = etree.parse(StringIO(self.soup.get_text()), etree.HTMLParser())
        self.html = etree.HTML(self.r.text)
        # self.html = etree.HTML(self.soup.get_text())
        self.etree_ = etree.tostring(self.tree.getroot(), pretty_print=True)
        self.etree2 = etree.tostring(self.html, pretty_print=True)


class AllSetsPage(Soup):
    def __init__(self, url):
        super().__init__(url)

    def get_expansion_names_and_urls(self):
        locator = ".//tr/td/a"
        matches = self.soup.findall(locator)
        # Only want match to expansion name not expansion logo
        expansions = [a for a in matches if matches.index(a)%2==0]
        names = [a.text for a in expansions]
        urls = [self.url + a.attrib['href'] for a in expansions]
        return [cards.Expansion(name=name, url=url, card_count=None, cards=None) for name,url in zip(names, urls)]


class SetPage(Soup):
    def __init__(self, url):
        super().__init__(url)
        self.card_row_locator = ".//tr//text() == '/')]/.."
        self.set_number_locator = ".//tr[contains(text(), '/')]"

    @property
    def set_count(self):
        set_number = self.soup.xpath(self.set_number_locator).text
        set_count = set_number.split('/')[-1].strip()
        return set_count

    def get_card_num_and_set_count(self, row):
        set_number = row.xpath(self.set_number_locator)
        (card_num,set_count) = [el.strip() for el in set_number.split('/')]
        return card_num, set_count

    def get_card_name(self, row):
        name = row.find(".//td[@width='20%']/a").text
        return name

    def get_cards(self):
        rows = self.soup.findall(self.card_row_locator)
        cards = [cards.Card(self.get_card_name(row), self.get_card_num_and_set_count(row)) for row in rows]
        return cards
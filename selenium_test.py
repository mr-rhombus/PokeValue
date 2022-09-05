from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree


serebii_base_url = 'https://www.serebii.net'
english_expansions_url = serebii_base_url + '/card/english.shtml'


class Expansion:
    def __init__(self, name, url, card_count, cards):
        self.name = name
        self.url = url
        self.card_count = card_count
        self.cards = cards

    def __str__(self):
        return f'The {self.name} expansion has {self.card_count} cards'


class SetsPage:
    def __init__(self, page_source):
        self.tree = etree.HTML(page_source)

    def get_expansion_names_and_urls(self):
        locator = ".//tr/td/a"
        matches = self.tree.findall(locator)
        # Only want match to expansion name not expansion logo
        expansions = [a for a in matches if matches.index(a)%2==0]
        names = [a.text for a in expansions]
        urls = [serebii_base_url + a.attrib['href'] for a in expansions]
        return [Expansion(name=name, url=url, card_count=None, cards=None) for name,url in zip(names, urls)]


class Card:
    """Represents an individual pokemon card. Comprised of the card name, card number, and total number of cards in the set (excluding "special" types of rare cards)
    """
    def __init__(self, name, card_number, card_count):
        self.name = name
        self.card_number = card_number
        self.card_count = card_count

    def __str__(self):
        return f'{self.name} {self.card_number}/{self.card_count}'


class SetPage:
    def __init__(self, page_source):
        self.etree = etree.HTML(page_source)
        self.card_row_locator = ".//tr[contains(text(), '/')]/.."
        self.set_number_locator = ".//tr[contains(text(), '/')]"

    @property
    def set_count(self):
        set_number = self.etree.xpath(self.set_number_locator).text
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
        rows = self.etree.findall(self.card_row_locator)
        cards = [Card(self.get_card_name(row), self.get_card_num_and_set_count(row)) for row in rows]
        return cards


def main():
    driver = webdriver.Chrome()
    driver.get(english_expansions_url)

    # Test
    english_sets_page = SetsPage(driver.page_source)
    astral_radiance = english_sets_page.get_expansion_names_and_urls()[3]
    driver.get(astral_radiance.url)
    astral_radiance_set = SetPage(driver.page_source)
    astral_radiance.card_count = astral_radiance_set.set_count
    astral_radiance.cards = astral_radiance_set.get_cards()
    print(astral_radiance.cards[-12])
    print(astral_radiance)
    print('done')



if __name__ == '__main__':
    main()
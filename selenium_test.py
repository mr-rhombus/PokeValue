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


def main():
    driver = webdriver.Chrome()
    driver.get(english_expansions_url)

    # Test
    english_sets_page = SetsPage(driver.page_source)
    astral_radiance = english_sets_page.get_expansion_names_and_urls()[3]
    print(astral_radiance)
    print('done')



if __name__ == '__main__':
    main()
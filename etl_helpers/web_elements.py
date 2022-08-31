import re, requests
from bs4 import BeautifulSoup


class WebpageSoup:
    """Represents a bs4.BeautifulSoup object scraped from a webpage

    :param soup: The BeautifulSoup object representing the webpage
    :type soup: bs4.BeautifulSoup
    """

    def __init__(self, soup):
        """Constructor method
        """
        self.soup = soup

    def expansion_names(self) -> list:
        """Returns a list of expansion names from the Bulbapedia expansions home page

        :return: A list of expansion names
        :rtype: list
        """
        expansions_names = []
        for el in self.soup.find_all('span', class_='mw-headline'):
            element_id = el.get('id')
            expansions_names.append(element_id)
        return expansions_names

    def table_after_h2(self, span_id: str) -> BeautifulSoup:
        """Finds the first <table> element after an h2 tag that looks something like <h2 id="span_id">. This lets us find the English set list on any given expansion set bulbapedia page

        :param span_id: "id" value of h2 element
        :type span_id: str
        :return: The BeautifulSoup object representing the table containing information about cards in the English card set of interest
        :rtype: BeautifulSoup
        """
        re_match = f'{span_id}.*?'
        h2_element = self.soup.find('span', id=re.compile(re_match)).parent
        # The <table> containing all sets will appear directly beneath the <h2> tag containing
        # the expansion name
        next_table = h2_element.findNext('table')
        return next_table


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
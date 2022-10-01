import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from components import web
import constants


def main():

    # Base English sets page
    english_sets_page = web.AllSetsPage(constants.english_expansions_url)
    expansion_details = english_sets_page.get_expansion_names_and_urls()

    # Gather expansions
    expansions = {}
    for expansion in expansion_details:
        expansion_page = web.SetPage(expansion.url)
        expansion.set_count = expansion_page.set_count
        expansion.cards = expansion_page.get_cards()
        expansions[expansion.name] = expansion
        print(expansions[expansion.name])
    


if __name__ == '__main__':
    main()
from components import web
import constants



# def main():
english_sets_page = web.AllSetsPage(constants.english_expansions_url)
astral_radiance_expansion = english_sets_page.get_expansion_names_and_urls()[3]
astral_radiance_page = web.SetPage(astral_radiance_expansion.url)
astral_radiance_expansion.card_count = astral_radiance_page.set_count
# print(astral_radiance_page.html.xpath("//tr/td[contains(text(), '/')]/.."))
astral_radiance_expansion.cards = astral_radiance_page.get_cards()
print(astral_radiance_expansion.cards[0])
#     print(astral_radiance.cards[-12])
#     print(astral_radiance)
#     print('done')



# if __name__ == '__main__':
#     main()
from components import web


serebii_base_url = 'https://www.serebii.net'
english_expansions_url = serebii_base_url + '/card/english.shtml'


english_sets_page = web.AllSetsPage(english_expansions_url)
print(english_sets_page.url)
print(english_sets_page.html.xpath("//body/div[@id='wrapper']"))
# print(english_sets_page.r.text)


# def main():
#     english_sets_page = web.AllSetsPage(english_expansions_url)
#     astral_radiance_meta = english_sets_page.get_expansion_names_and_urls()[3]
#     astral_radiance = web.SetPage(astral_radiance_meta.url)
#     astral_radiance.card_count = astral_radiance.set_count
#     astral_radiance.cards = astral_radiance.get_cards()
#     print(astral_radiance.cards[-12])
#     print(astral_radiance)
#     print('done')



# if __name__ == '__main__':
#     main()
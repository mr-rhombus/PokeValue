class Expansion:
    def __init__(self, name, url, card_count, cards):
        self.name = name
        self.url = url
        self.card_count = card_count
        self.cards = cards

    def __str__(self):
        return f'The {self.name} expansion has {self.card_count} cards'


class Card:
    """Represents an individual pokemon card. Comprised of the card name, card number, and total number of cards in the set (excluding "special" types of rare cards)
    """
    def __init__(self, name, card_number, card_count):
        self.name = name
        self.card_number = card_number
        self.card_count = card_count

    def __str__(self):
        return f'{self.name} {self.card_number}/{self.card_count}'
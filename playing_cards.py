from random import shuffle


class PlayingCard:
    def __init__(self, name, value, suit):
        self.name = name
        self.value = value
        self.suit = suit


class Hand:
    def __init__(self):
        self.cards = []
        self.count = 0
        self.score = 0

    def add_card(self, card):
        self.cards.append(card)
        self.count = len(self.cards)
        self.__update_score()

    def reset(self):
        self.cards.clear()
        self.count = 0
        self.score = 0

    def __update_score(self):
        if self.score != -1:
            score = 0
            ace_count = 0
            for card in self.cards:
                score += card.value
                if card.name == "ace":
                    ace_count += 1
            while score > 21 and ace_count > 0:
                score -= 10
                ace_count -= 1
            self.score = score


class Deck(Hand):
    def __init__(self, size=1):
        super().__init__()
        self.score = -1
        self.new_deck(num_of_decks=size)
        # self.shuffle()

    def new_deck(self, num_of_decks):
        total_decks = num_of_decks
        suits = ["hearts", "clubs", "diamonds", "spades"]
        face_cards = ["jack", "queen", "king"]
        for _ in range(total_decks):
            for suit in suits:
                self.add_card(PlayingCard("ace", 11, suit))
                for i in range(2, 11):
                    self.add_card(PlayingCard(str(i), i, suit))
                for name in face_cards:
                    self.add_card(PlayingCard(name, 10, suit))

    def shuffle(self):
        for _ in range(6):
            shuffle(self.cards)

    def deal_card(self):
        """removes and returns first card from deck"""
        return self.cards.pop(0)


if __name__ == "__main__":
    deck = Deck()
    for card in deck.cards:
        print(f"{card.name} of {card.suit}")

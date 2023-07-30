from playing_cards import *

DECK_SIZE = 6  # how many 52 card decks will be in play
RESHUFFLE_AT = 78  # when you get to this many cards left in shoe, reshuffle
STARTING_CASH = 100
MAX_WAGER = 5
MIN_WAGER = 0


class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.dealer_visibility = False
        self.active_index = 0
        self.options = ["wager_up", "deal", "wager_down"]
        self.wallet = STARTING_CASH
        self.wager_memory = 0
        self.wager = 0
        self.message = ""
        self.natural_count = 0

    def new_game(self):
        self.deck = Deck(DECK_SIZE)
        self.deck.shuffle()
        self.options = ["wager_up", "deal", "wager_down"]
        self.wallet = STARTING_CASH
        self.message = "Welcome to BlackJack for peasants."

    def deal(self):
        # Reset per game attributes
        self.active_index = 0
        self.__reshuffle_check()
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.dealer_visibility = False
        self.wallet -= self.wager
        self.message = "banter"

        # Create Initial hands for dealer and player
        self.player_hand.append(Hand())
        self.dealer_hand.append(Hand())
        for _ in range(2):
            self.__deal_card(self.player_hand[0])
            self.__deal_card(self.dealer_hand[0])

        # Check outcomes of deal and update options
        if self.__is_natural():
            self.options = ["wager_up", "deal", "wager_down"]
        else:
            self.options = ["hit", "stand", "double", "surrender"]
            if self.__is_split():
                self.options.append("split")

    def __is_natural(self):
        if self.player_hand[0].score == 21:
            self.natural_count += 1
            self.dealer_visibility = True
            if self.dealer_hand[0].score == 21:
                self.wallet += self.wager
                self.message = "tie"
                self.wager = self.wager_memory
            else:
                self.wallet += self.wager * 1.5
                self.message = "win"
                self.wager = self.wager_memory
            return True

    def __is_split(self):
        # returns true if players initial dealt hand is a "value" pair. ie 3,3  6,6  10,Q
        if self.player_hand[0].cards[0].value == self.player_hand[0].cards[1].value:
            return True

    def split(self):
        #  Create Another Hand Object in player_hand list and move second card from initial hand into new hand
        self.player_hand.append(Hand())
        self.player_hand[1].add_card(self.player_hand[0].cards.pop())
        #  deal a new card to each of the split hands
        self.__deal_card(self.player_hand[0])
        self.__deal_card(self.player_hand[1])
        # remove another instance of wager from wallet, but do not change "wager"
        # as each hand outcome will be evaluated based on original amount
        self.wallet -= self.wager

        # update options first, then check hands for 21. If both hands == 21 skip to dealer
        self.options = ["hit", "stand"]
        if self.player_hand[0].score == 21:
            self.active_index += 1
            if self.player_hand[1].score == 21:
                self.dealer_plays()

    def double_down(self):
        self.__deal_card(self.player_hand[self.active_index])
        self.wallet -= self.wager
        self.wager += self.wager
        self.dealer_plays()

    def surrender(self):
        self.options = ["wager_up", "deal", "wager_down"]
        self.dealer_visibility = True
        self.wallet += self.wager/2
        self.message = "lose"
        self.wager = self.wager_memory

    def hit(self):
        # update options to remove "double down" in the case where player declines doubling down
        self.options = ["hit", "stand"]
        # deal card to whichever hand is active (original or split)
        self.__deal_card(self.player_hand[self.active_index])
        # recurse through hands to check for case where they equal 21 off of the split
        self.__recursive_index_update()

    def __recursive_index_update(self):
        if self.player_hand[self.active_index].score > 20:
            if self.active_index == (len(self.player_hand) - 1):
                self.dealer_plays()
            else:
                self.active_index += 1
                self.__recursive_index_update()

    def stand(self):
        if self.active_index == (len(self.player_hand) - 1):
            self.dealer_plays()
        else:
            self.active_index += 1
            if self.active_index == (len(self.player_hand) - 1):
                if self.player_hand[self.active_index].score > 20:
                    self.dealer_plays()

    def dealer_plays(self):
        self.options = ["wager_up", "deal", "wager_down"]
        self.dealer_visibility = True
        should_play = False
        for i in range(len(self.player_hand)):
            if self.player_hand[i].score < 21:
                should_play = True
        if should_play:
            while self.dealer_hand[0].score < 17 and self.dealer_hand[0].score < 21:
                self.__deal_card(self.dealer_hand[0])
        self.__settle_up()

    def wager_up(self):
        self.wager += 1
        if self.wager > MAX_WAGER:
            self.wager = MAX_WAGER
        self.wager_memory = self.wager

    def wager_down(self):
        self.wager -= 1
        if self.wager < MIN_WAGER:
            self.wager = MIN_WAGER
        self.wager_memory = self.wager

    def __settle_up(self):
        # payout for individual hands whether split or not, but also calculate overall advantage by starting from
        # zero, adding 1 for a win, subtracting 1 for loss and updating message by getting sign of result at end
        result = 0
        for i in range(len(self.player_hand)):
            if self.player_hand[i].score > 21:
                result -= 1
            elif self.dealer_hand[0].score > 21:
                result += 1
                self.wallet += self.wager * 2
            elif self.player_hand[i].score < self.dealer_hand[0].score:
                result -= 1
            elif self.player_hand[i].score > self.dealer_hand[0].score:
                result += 1
                self.wallet += self.wager * 2
            elif self.player_hand[i].score == self.dealer_hand[0].score:
                self.wallet += self.wager

        if result < 0:
            self.message = "lose"
        elif result > 0:
            self.message = "win"
        else:
            self.message = "tie"
        self.wager = self.wager_memory

    def __deal_card(self, hand):
        hand.add_card(self.deck.deal_card())

    def __reshuffle_check(self):
        """For a 6*52 card deck game if deck has less than 78 cards in it a new 6*52 card deck is created and shuffled.
        This means the game has a 4.5 deck penetration. This check is performed on every deal"""
        if len(self.deck.cards) < RESHUFFLE_AT:
            self.deck = Deck(DECK_SIZE)
            self.deck.shuffle()


if __name__ == "__main__":
    pass

from random import choice


class Simulation:
    def __init__(self, game, ui, iterations, sim_algorithm):
        self.game = game
        self.ui = ui
        self.algorithm = sim_algorithm
        self.iterations = iterations
        self.iteration_count = 0
        self.split_count = 0
        self.double_count = 0
        self.surrender_count = 0
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.bank_low = 0
        self.bank_high = 0
        self.starting_cash = self.game.wallet

    def autoplay(self):
        # This is the main loop of the simulation.
        self.game.wager = 1
        self.game.wager_memory = 1
        while self.iteration_count < self.iterations:

            # check for high and low wallet values
            if self.game.wallet < self.bank_low:
                self.bank_low = self.game.wallet
            if self.game.wallet > self.bank_high:
                self.bank_high = self.game.wallet

            # --------------Debug Code- advances on "enter" keypress and shows status in speech bubble ------------
            #
            #             if "deal" in self.game.options:
            #                 self.debug_choice = "deal"
            #             else:
            #                 self.debug_choice = self.get_action()
            #
            #             if self.iteration_count > 0:
            #                 self.ui.update_buttons(self.game.options)
            #                 self.ui.update_player_cards(self.game.player_hand, self.game.active_index)
            #                 self.ui.update_dealer_cards(self.game.dealer_hand[0].cards, self.game.dealer_visibility)
            #                 self.ui.update_scoreboard(self.game.wallet, self.game.wager)
            #                 self.ui.update_message(self.game.message, custom=f"{self.game.message}\n\n{self.debug_choice}")
            #                 self.ui.window.update()
            #                 input("")
            #
            #             self.take_action(self.debug_choice)
            #
            #             # comment out the if else statement below this to use debug code
            # ----------------------------------------------------------------------------------------------------

            # get algorithm dependent action and act upon it.
            if "deal" in self.game.options:
                self.take_action("deal")
            else:
                self.take_action(self.get_action())

            # If round is over, iterate game_count and update w,l,t
            if self.game.message == "win":
                self.iteration_count += 1
                self.wins += 1
            elif self.game.message == "lose":
                self.iteration_count += 1
                self.losses += 1
            elif self.game.message == "tie":
                self.iteration_count += 1
                self.ties += 1
            # update progress on screen
            self.show_autoplay_percent()

        # after while loop complete update message and show results
        self.ui.speech_bubble.itemconfig(self.ui.dealer_dialogue,
                                         text=f"Pray tell. Doest the outcome satisfy the commoner?".upper())
        self.ui.window.update()
        self.show_results()

    def get_action(self):
        if self.algorithm == "random":
            return self.random_action()

        elif self.algorithm == "simple_random":
            return self.simple_random()

        elif self.algorithm == "blackjack_or_bust":
            return self.hit_only()

        elif self.algorithm == "stand_only":
            return self.stand_only()

        elif self.algorithm == "dealer_strategy":
            return self.what_dealer_would_do()

        elif self.algorithm == "advanced":
            return self.advanced_strategy()

        elif self.algorithm == "wizard":
            return self.wizard_of_odds()

        elif self.algorithm == "euro_wizard":
            return self.wizard_of_odds_euro()

    def take_action(self, action):
        if action == "deal":
            self.game.deal()
        elif action == "split":
            self.game.split()
            self.split_count += 1
        elif action == "double":
            self.game.double_down()
            self.double_count += 1
        elif action == "hit":
            self.game.hit()
        elif action == "stand":
            self.game.stand()
        elif action == "surrender":
            self.game.surrender()
            self.surrender_count += 1

    def show_autoplay_percent(self):
        if (self.iteration_count / self.iterations) * 100 % 1 == 0:
            self.ui.speech_bubble.itemconfig(self.ui.dealer_dialogue,
                                             text=f"Could it be true? \n that "
                                                  f"{int((self.iteration_count / self.iterations) * 100)}%"
                                                  f" of the\nsimulation is now complete?".upper())
            self.ui.window.update()

    def show_results(self):
        print(f"games played = {self.iterations}")
        print(f"times split = {self.split_count}")
        print(f"naturals = {self.game.natural_count}")
        print(f"times doubled down = {self.double_count}")
        print(f"times surrendered = {self.surrender_count}")
        print(f"hands won = {self.wins}")
        print(f"hands lost = {self.losses}")
        print(f"hands tied = {self.ties}")
        print(f"highest amount in wallet = {self.bank_high}")
        print(f"lowest amount in wallet = {self.bank_low}")
        print(f"final amount in wallet = {self.game.wallet}")
        # print(
        #     f"RTP = {(self.iterations + self.double_count + self.split_count + self.game.wallet) / (self.iterations + self.double_count + self.split_count) * 100}%")
        # print(
        #     f"house advantage = {self.game.wallet / (self.iterations + self.double_count + self.split_count) * -100}%")
        print(
            f"RTP = {(self.iterations + self.game.wallet - self.starting_cash) / self.iterations * 100}%")
        print(
            f"house advantage = {self.game.wallet - self.starting_cash} / {self.iterations} x 100 = {self.game.wallet / self.iterations * -100}%")

    # ------------------------- Start of Algorithm implementation code ---------------------------------------
    def random_action(self):
        return choice(self.game.options)

    def simple_random(self):
        if "deal" in self.game.options:
            return "deal"
        else:
            return choice(["hit", "stand"])

    def hit_only(self):
        if "deal" in self.game.options:
            return "deal"
        else:
            return "hit"

    def stand_only(self):
        if "deal" in self.game.options:
            return "deal"
        else:
            return "stand"

    def what_dealer_would_do(self):
        if "deal" in self.game.options:
            return "deal"
        elif self.game.player_hand[0].score < 17:
            return "hit"
        else:
            return "stand"

    def advanced_strategy(self):
        # https://sunil-s.github.io/assets/pdfs/AcingBlackJack.pdf
        if "deal" in self.game.options:
            return "deal"
        if "split" in self.game.options:
            if self.game.player_hand[0].cards[0].value == 11:
                return "split"
            if self.game.player_hand[0].cards[0].value == 10:
                return "stand"
            if self.game.player_hand[0].cards[0].value == 9:
                if self.game.dealer_hand[0].cards[0].value == 7 or self.game.dealer_hand[0].cards[0].value > 9:
                    return "stand"
                else:
                    return "split"
            if self.game.player_hand[0].cards[0].value == 8:
                return "split"
            if self.game.player_hand[0].cards[0].value == 7:
                if self.game.dealer_hand[0].cards[0].value < 8:
                    return "split"
                else:
                    return "hit"
            if self.game.player_hand[0].cards[0].value == 6:
                if self.game.dealer_hand[0].cards[0].value < 7:
                    return "split"
                else:
                    return "hit"
            if self.game.player_hand[0].cards[0].value == 5:
                if self.game.dealer_hand[0].cards[0].value < 10:
                    return "double"
                else:
                    return "hit"
            if self.game.player_hand[0].cards[0].value == 4:
                if self.game.dealer_hand[0].cards[0].value == 5 or self.game.dealer_hand[0].cards[0].value == 6:
                    return "split"
                else:
                    return "hit"
            if self.game.player_hand[0].cards[0].value == 3:
                if self.game.dealer_hand[0].cards[0].value < 8:
                    return "split"
                else:
                    return "hit"
            if self.game.player_hand[0].cards[0].value == 2:
                if self.game.dealer_hand[0].cards[0].value < 8:
                    return "split"
                else:
                    return "hit"
        soft = False
        for card in self.game.player_hand[self.game.active_index].cards:
            if card.name == "ace":
                soft = True
        if soft:
            if self.game.player_hand[self.game.active_index].score == 20:
                return "stand"
            if self.game.player_hand[self.game.active_index].score == 19:
                return "stand"
            if self.game.player_hand[self.game.active_index].score == 18:
                if self.game.dealer_hand[0].cards[0].value > 8:
                    return "hit"
                if 2 < self.game.dealer_hand[0].cards[0].value < 7:
                    if "double" in self.game.options:
                        return "double"
                    else:
                        return "hit"
                else:
                    return "stand"
            if self.game.player_hand[self.game.active_index].score == 17:
                if 7 > self.game.dealer_hand[0].cards[0].value > 2:
                    if "double" in self.game.options:
                        return "double"
                    else:
                        return "hit"
                else:
                    return "hit"
            if self.game.player_hand[self.game.active_index].score == 16:
                if 7 > self.game.dealer_hand[0].cards[0].value > 3:
                    if "double" in self.game.options:
                        return "double"
                    else:
                        return "hit"
                else:
                    return "hit"
            if self.game.player_hand[self.game.active_index].score == 15:
                if 7 > self.game.dealer_hand[0].cards[0].value > 3:
                    if "double" in self.game.options:
                        return "double"
                    else:
                        return "hit"
                else:
                    return "hit"
            if self.game.player_hand[self.game.active_index].score == 14:
                if 7 > self.game.dealer_hand[0].cards[0].value > 4:
                    if "double" in self.game.options:
                        return "double"
                    else:
                        return "hit"
                else:
                    return "hit"
            if self.game.player_hand[self.game.active_index].score == 13:
                if 7 > self.game.dealer_hand[0].cards[0].value > 4:
                    if "double" in self.game.options:
                        return "double"
                    else:
                        return "hit"
                else:
                    return "hit"

        if self.game.player_hand[self.game.active_index].score < 9:
            return "hit"
        if self.game.player_hand[self.game.active_index].score == 9:
            if 7 > self.game.dealer_hand[0].cards[0].value > 2:
                if "double" in self.game.options:
                    return "double"
                else:
                    return "hit"
            else:
                return "hit"
        if self.game.player_hand[self.game.active_index].score == 10:
            if self.game.dealer_hand[0].cards[0].value < 10:
                if "double" in self.game.options:
                    return "double"
                else:
                    return "hit"
            else:
                return "hit"

        if self.game.player_hand[self.game.active_index].score == 11:
            if self.game.dealer_hand[0].cards[0].value < 11:
                if "double" in self.game.options:
                    return "double"
                else:
                    return "hit"
            else:
                return "hit"

        if self.game.player_hand[self.game.active_index].score == 12:
            if 3 < self.game.dealer_hand[0].cards[0].value < 7:
                return "stand"
            else:
                return "hit"

        if self.game.player_hand[self.game.active_index].score == 13:
            if self.game.dealer_hand[0].cards[0].value < 7:
                return "stand"
            else:
                return "hit"

        if self.game.player_hand[self.game.active_index].score == 14:
            if self.game.dealer_hand[0].cards[0].value < 7:
                return "stand"
            else:
                return "hit"

        if self.game.player_hand[self.game.active_index].score == 15:
            if self.game.dealer_hand[0].cards[0].value < 7:
                return "stand"
            if self.game.dealer_hand[0].cards[0].value == 10:
                return "surrender"
            else:
                return "hit"

        if self.game.player_hand[self.game.active_index].score == 16:
            if self.game.dealer_hand[0].cards[0].value < 7:
                return "stand"
            if self.game.dealer_hand[0].cards[0].value > 8:
                return "surrender"
            else:
                return "hit"

        if self.game.player_hand[self.game.active_index].score > 16:
            return "stand"

        print("If you see this, something went wrong.")
        print(f"iteration: {self.iteration_count}")
        print("player cards")
        for i in range(self.game.player_hand[self.game.active_index].count):
            print(f"{self.game.player_hand[self.game.active_index].cards[i].name}")
        print(self.game.player_hand[self.game.active_index].score)
        print("dealer cards")
        for i in range(self.game.dealer_hand[0].count):
            print(f"{self.game.dealer_hand[0].cards[i].name}")
        self.ui.window.exit()

    def wizard_of_odds(self):
        # https://wizardofodds.com/games/blackjack/strategy/calculator/
        soft = False
        score = 0
        ace_count = 0
        for card in self.game.player_hand[self.game.active_index].cards:
            score += card.value
            if card.name == "ace":
                ace_count += 1
                soft = True
        while score > 21 and ace_count > 0:
            score -= 10
            ace_count -= 1
            soft = False

        action = ""
        if "split" in self.game.options:
            pair_table = [
                # 2    3    4    5    6    7    8    9    10   A
                ["H", "H", "P", "P", "P", "P", "H", "H", "H", "H"],  # 2,2
                ["H", "H", "P", "P", "P", "P", "H", "H", "H", "H"],  # 3
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H"],  # 4
                ["DH", "DH", "DH", "DH", "DH", "DH", "DH", "DH", "H", "H"],  # 5
                ["H", "P", "P", "P", "P", "H", "H", "H", "H", "H"],  # 6
                ["P", "P", "P", "P", "P", "P", "H", "H", "H", "H"],  # 7
                ["P", "P", "P", "P", "P", "P", "P", "P", "P", "P"],  # 8
                ["P", "P", "P", "P", "P", "S", "P", "P", "S", "S"],  # 9
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 10
                ["P", "P", "P", "P", "P", "P", "P", "P", "P", "P"],  # A
            ]
            action = pair_table[self.game.player_hand[self.game.active_index].cards[0].value - 2][
                self.game.dealer_hand[0].cards[0].value - 2]

        elif soft:
            soft_table = [
                # 2    3    4    5    6    7    8    9    10   A
                ["H", "H", "H", "DH", "DH", "H", "H", "H", "H", "H"],  # 13
                ["H", "H", "H", "DH", "DH", "H", "H", "H", "H", "H"],  # 14
                ["H", "H", "DH", "DH", "DH", "H", "H", "H", "H", "H"],  # 15
                ["H", "H", "DH", "DH", "DH", "H", "H", "H", "H", "H"],  # 16
                ["H", "DH", "DH", "DH", "DH", "H", "H", "H", "H", "H"],  # 17
                ["S", "DS", "DS", "DS", "DS", "S", "S", "H", "H", "H"],  # 18
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 19
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 20
            ]
            action = soft_table[score - 13][self.game.dealer_hand[0].cards[0].value - 2]

        elif not soft:
            hard_table = [
                # 2    3    4    5    6    7    8    9    10   A
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H"],  # 4
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H"],  # 5
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H"],  # 6
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H"],  # 7
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H"],  # 8
                ["H", "DH", "DH", "DH", "DH", "H", "H", "H", "H", "H"],  # 9
                ["DH", "DH", "DH", "DH", "DH", "DH", "DH", "DH", "H", "H"],  # 10
                ["DH", "DH", "DH", "DH", "DH", "DH", "DH", "DH", "DH", "H"],  # 11
                ["H", "H", "S", "S", "S", "H", "H", "H", "H", "H"],  # 12
                ["S", "S", "S", "S", "S", "H", "H", "H", "H", "H"],  # 13
                ["S", "S", "S", "S", "S", "H", "H", "H", "H", "H"],  # 14
                ["S", "S", "S", "S", "S", "H", "H", "H", "RH", "H"],  # 15
                ["S", "S", "S", "S", "S", "H", "H", "RH", "RH", "RH"],  # 16
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 17
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 18
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 19
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 20
            ]
            action = hard_table[score - 4][self.game.dealer_hand[0].cards[0].value - 2]

        if action == "H":
            return "hit"
        elif action == "S":
            return "stand"
        elif action == "P":
            return "split"
        elif action == "DH":
            if "double" in self.game.options:
                return "double"
            else:
                return "hit"
        elif action == "DS":
            if "double" in self.game.options:
                return "double"
            else:
                return "stand"
        elif action == "RH":
            if "surrender" in self.game.options:
                return "surrender"
            else:
                return "hit"

    def wizard_of_odds_euro(self):
        # https://wizardofodds.com/games/blackjack/strategy/calculator/
        soft = False
        score = 0
        ace_count = 0
        for card in self.game.player_hand[self.game.active_index].cards:
            score += card.value
            if card.name == "ace":
                ace_count += 1
                soft = True
        while score > 21 and ace_count > 0:
            score -= 10
            ace_count -= 1
            soft = False

        action = ""
        if "split" in self.game.options:
            pair_table = [
                # 2    3    4    5    6    7    8    9    10   A
                ["H", "H", "P", "P", "P", "P", "H", "H", "H", "H"],  # 2,2
                ["H", "H", "P", "P", "P", "P", "H", "H", "H", "RH"],  # 3
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H"],  # 4
                ["DH", "DH", "DH", "DH", "DH", "DH", "DH", "DH", "H", "H"],  # 5
                ["H", "P", "P", "P", "P", "H", "H", "H", "H", "RH"],  # 6
                ["P", "P", "P", "P", "P", "P", "H", "H", "RH", "RH"],  # 7
                ["P", "P", "P", "P", "P", "P", "P", "P", "RH", "RH"],  # 8
                ["P", "P", "P", "P", "P", "S", "P", "P", "S", "S"],  # 9
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 10
                ["P", "P", "P", "P", "P", "P", "P", "P", "P", "H"],  # A
            ]
            action = pair_table[self.game.player_hand[self.game.active_index].cards[0].value - 2][
                self.game.dealer_hand[0].cards[0].value - 2]

        elif soft:
            soft_table = [
                # 2    3    4    5    6    7    8    9    10   A
                ["H", "H", "H", "DH", "DH", "H", "H", "H", "H", "H"],  # 13
                ["H", "H", "H", "DH", "DH", "H", "H", "H", "H", "H"],  # 14
                ["H", "H", "DH", "DH", "DH", "H", "H", "H", "H", "H"],  # 15
                ["H", "H", "DH", "DH", "DH", "H", "H", "H", "H", "H"],  # 16
                ["H", "DH", "DH", "DH", "DH", "H", "H", "H", "H", "H"],  # 17
                ["S", "DS", "DS", "DS", "DS", "S", "S", "H", "H", "H"],  # 18
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 19
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 20
            ]
            action = soft_table[score - 13][self.game.dealer_hand[0].cards[0].value - 2]

        elif not soft:
            hard_table = [
                # 2    3    4    5    6    7    8    9    10   A
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "RH"],  # 4
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "RH"],  # 5
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "RH"],  # 6
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "RH"],  # 7
                ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H"],  # 8
                ["H", "DH", "DH", "DH", "DH", "H", "H", "H", "H", "H"],  # 9
                ["DH", "DH", "DH", "DH", "DH", "DH", "DH", "DH", "H", "H"],  # 10
                ["DH", "DH", "DH", "DH", "DH", "DH", "DH", "DH", "H", "H"],  # 11
                ["H", "H", "S", "S", "S", "H", "H", "H", "H", "RH"],  # 12
                ["S", "S", "S", "S", "S", "H", "H", "H", "H", "RH"],  # 13
                ["S", "S", "S", "S", "S", "H", "H", "H", "RH", "RH"],  # 14
                ["S", "S", "S", "S", "S", "H", "H", "H", "RH", "RH"],  # 15
                ["S", "S", "S", "S", "S", "H", "H", "RH", "RH", "RH"],  # 16
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "RS"],  # 17
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 18
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 19
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 20
            ]
            action = hard_table[score - 4][self.game.dealer_hand[0].cards[0].value - 2]

        if action == "H":
            return "hit"
        elif action == "S":
            return "stand"
        elif action == "P":
            return "split"
        elif action == "DH":
            if "double" in self.game.options:
                return "double"
            else:
                return "hit"
        elif action == "DS":
            if "double" in self.game.options:
                return "double"
            else:
                return "stand"
        elif action == "RH":
            if "surrender" in self.game.options:
                return "surrender"
            else:
                return "hit"
        elif action == "RS":
            if "surrender" in self.game.options:
                return "surrender"
            else:
                return "stand"
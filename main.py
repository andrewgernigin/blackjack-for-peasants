import sim_model
import blackjack_model
import blackjack_ui


def update_ui():
    ui.update_buttons(game.options)
    ui.update_player_cards(game.player_hand, game.active_index)
    ui.update_dealer_cards(game.dealer_hand[0].cards, game.dealer_visibility)
    ui.update_scoreboard(game.wallet, game.wager)
    ui.update_message(game.message)


def reset_game():
    game.new_game()
    ui.load_title()
    ui.update_scoreboard(game.wallet, game.wager)
    ui.update_buttons(game.options)
    ui.update_message(game.message, "EVERYONE LOVES A FRESH START.")


def deal():
    game.deal()
    update_ui()


def split():
    game.split()
    update_ui()


def hit():
    game.hit()
    update_ui()


def stand():
    game.stand()
    update_ui()


def surrender():
    game.surrender()
    update_ui()


def double():
    game.double_down()
    update_ui()


def wager_up():
    game.wager_up()
    ui.update_scoreboard(game.wallet, game.wager)


def wager_down():
    game.wager_down()
    ui.update_scoreboard(game.wallet, game.wager)


def autoplay(iterations, algorithm):
    sim = sim_model.Simulation(game, ui, iterations, algorithm)
    sim.autoplay()
    del sim


# ---------------------------- Start of main -------------------------------
# Create instances of View and Model
game = blackjack_model.Blackjack()
ui = blackjack_ui.BlackjackInterface(game.deck.cards)
# initialize game (probably a button in the future)
game.new_game()
ui.update_scoreboard(game.wallet, game.wager)
ui.update_buttons(game.options)

# Connect UI buttons to Model through controller functions
ui.deal_button.config(command=deal)
ui.hit_me_button.config(command=hit)
ui.stand_button.config(command=stand)
ui.double_button.config(command=double)
ui.surrender_button.config(command=surrender)
ui.split_button.config(command=split)
ui.wager_up_btn.config(command=wager_up)
ui.wager_down_btn.config(command=wager_down)
ui.file_menu.add_command(label="Reset", command=reset_game)
ui.file_menu.add_command(label="Exit", command=exit)

# ------------------------ Simulation Code ---------------------------
# Implementation through menus to be implemented at a later date. If you want to test it you can uncomment
# Doing so will cause simulation to run when program starts and output data to console when complete


# # optional algorithms for autoplay temporarily listed here
# # dealer_strategy
# # blackjack_or_bust
# # random
# # simple_random
# # advanced
# # wizard
# # euro_wizard
# # stand_only
#
# # actual code for simulation.
# try:
#     autoplay(100000, "wizard")
# except tkinter.TclError:
#     # if user closes root window while autoplay still running
#     exit()

ui.window.mainloop()

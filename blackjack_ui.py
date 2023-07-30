from tkinter import *
from PIL import Image, ImageTk
from playing_cards import PlayingCard
import json
from random import choice
from functools import partial

GREEN = "green"
# GREEN = "#239063"
BLACK = "#0b0b0b"
FONT = ("small fonts", 16, "bold")


class BlackjackInterface:
    def __init__(self, deck):
        # create root window
        self.window = Tk()
        # define class attributes
        self.card_images = {}
        self.small_card_images = {}
        self.__load_card_images_from_file(deck)
        self.dealer_image = None
        self.observer_image = None
        self.dialogue_options = {}
        self.__load_dialogue_options_from_file()
        self.scoreboard = [0, 0, 0]
        self.buttons = []
        self.clicked_button = ""
        self.current_dealer = "dealer"
        # ------------------------Create Screen elements that should be changed with CAUTION----------------------------

        # configure root window
        self.window.config(bg="black")
        self.window.title("Blackjack For Peasants")
        self.window.minsize(1024, 768)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # create and configure menu bar
        self.menu_bar = Menu(self.window)

        self.file_menu = Menu(self.menu_bar, tearoff=0)

        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.dealer_options = Menu(self.options_menu, tearoff=0)

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_cascade(label="New Dealer", menu=self.dealer_options)

        self.window.config(menu=self.menu_bar)
        self.dealer_options.add_command(label="Innocent X", command=partial(self.change_dealer, "dealer"))
        self.dealer_options.add_command(label="A Bear", command=partial(self.change_dealer, "dealer-bear"))

        # create padding frame used to keep aspect ratio when window size adjusted by user
        self.pad_frame = Frame(borderwidth=0, bg="black", width=1024, height=768)
        self.pad_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # create frame to hold all visual content that works with padding frame
        self.view_frame = Frame(self.window, bg=BLACK)
        self.view_frame.rowconfigure(0, weight=1)
        self.view_frame.rowconfigure(1, weight=2)
        self.view_frame.rowconfigure(2, weight=1)
        self.view_frame.rowconfigure(3, weight=2)
        self.view_frame.columnconfigure(0, weight=1)
        self.view_frame.config(bg=GREEN, pady=0, padx=0)
        # call set aspect function to pack view frame with proper aspect ratio
        self.__set_aspect(self.view_frame, self.pad_frame, aspect_ratio=4.0 / 3.0)

        # Create a frame(dealer_frame) inside a frame(top_frame) to play nice with adjustments to aspect ratio
        # do not change unless changing aspect ratio. For adjustments to LAYOUT of top frame like image position,
        # buffers, or speech bubble position go to next section
        self.top_frame = Frame(self.view_frame, bg=BLACK, highlightthickness=0, borderwidth=0)
        self.top_frame.grid(row=0, column=0, sticky=NSEW)
        self.dealer_frame = Frame(self.top_frame, bg=BLACK, borderwidth=0, highlightthickness=0)
        self.dealer_frame.pack(anchor="center", side="bottom")
        # --------------------------------------------------------------------------------------------------------------

        # ----------------------- LAYOUT of top third of screen starts here --------------------------------------------
        self.top_left_canvas = Canvas(self.dealer_frame, bg=BLACK, highlightthickness=0, width=90)
        self.speech_bubble = Canvas(self.dealer_frame, bg="white", highlightthickness=0, height=190, width=260, )
        self.speech_bubble.config()
        self.dealer_dialogue = self.speech_bubble.create_text(
            130, 95, font=FONT, justify="center",
        )
        self.speech_bubble.itemconfig(
            self.dealer_dialogue, fill="black", width=240, text="WELCOME TO BLACKJACK FOR PEASANTS."
        )
        self.top_right_canvas = Canvas(self.dealer_frame, bg=BLACK, highlightthickness=0, width=50)

        # call function to pack widgets and load dealer and observer
        self.__load_dealer_image()

        # ---------------------------------------------------------------------------------------------------------------------

        self.dealer_card_frame = Frame(self.view_frame, borderwidth=0, bg=GREEN)
        self.dealer_card_frame.grid(row=1, pady=(10, 0))

        self.player_card_frame = Frame(self.view_frame, borderwidth=0, bg=GREEN)
        self.player_card_frame.grid(row=3)

        self.button_frame = Frame(self.view_frame, borderwidth=0, bg=GREEN)
        self.button_frame.grid(row=2)

        self.hit_me_button = Button(
            self.button_frame, text="HIT", width=7, borderwidth=0, font=FONT,
            command=lambda: self.button_clicked("hit")
        )
        self.stand_button = Button(
            self.button_frame, text="STAND", width=7, borderwidth=0, font=FONT,
            command=lambda: self.button_clicked("stand")
        )
        self.surrender_button = Button(
            self.button_frame, text="YIELD", width=7, borderwidth=0, font=FONT,
            command=lambda: self.button_clicked("surrender")
        )
        self.split_button = Button(
            self.button_frame, text="SPLIT", width=7, borderwidth=0, font=FONT,
            command=lambda: self.button_clicked("split")
        )
        self.deal_button = Button(
            self.button_frame, text="DEAL", width=7, borderwidth=0, font=FONT,
            command=lambda: self.button_clicked("deal")
        )
        self.double_button = Button(
            self.button_frame, text="DOUBLE", width=7, borderwidth=0, font=FONT,
            command=lambda: self.button_clicked("double")
        )
        self.wager_up_btn = Button(
            self.button_frame, text="WAGER+", width=7, borderwidth=0, font=FONT,
            command=lambda: self.button_clicked("wager_up")
        )
        self.wager_down_btn = Button(
            self.button_frame, text="WAGER-", width=7, borderwidth=0, font=FONT,
            command=lambda: self.button_clicked("wager_down")
        )

        self.buttons.append(self.stand_button)
        self.buttons.append(self.hit_me_button)
        self.buttons.append(self.surrender_button)
        self.buttons.append(self.split_button)
        self.buttons.append(self.deal_button)
        self.buttons.append(self.double_button)
        self.buttons.append(self.wager_up_btn)
        self.buttons.append(self.wager_down_btn)

        self.button_spacer_00 = Label(
            self.button_frame, highlightthickness=0, height=2, borderwidth=0, bg=GREEN, text="    "
        )
        self.button_spacer_01 = Label(
            self.button_frame, highlightthickness=0, height=2, borderwidth=0, bg=GREEN, text="    "
        )
        self.button_spacer_02 = Label(
            self.button_frame, highlightthickness=0, height=2, borderwidth=0, bg=GREEN, text="    "
        )
        self.button_spacer_03 = Label(
            self.button_frame, highlightthickness=0, height=2, borderwidth=0, bg=GREEN, text="    "
        )
        self.button_spacer_04 = Label(
            self.button_frame, highlightthickness=0, height=2, borderwidth=0, bg=GREEN, text="    "
        )
        self.button_spacer_05 = Label(
            self.button_frame, highlightthickness=0, height=2, borderwidth=0, bg=GREEN, text="    "
        )
        self.button_spacer_06 = Label(
            self.button_frame, highlightthickness=0, height=2, borderwidth=0, bg=GREEN, text="    "
        )

        self.buttons.append(self.button_spacer_00)
        self.buttons.append(self.button_spacer_01)
        self.buttons.append(self.button_spacer_02)
        self.buttons.append(self.button_spacer_03)
        self.buttons.append(self.button_spacer_04)
        self.buttons.append(self.button_spacer_05)
        self.buttons.append(self.button_spacer_06)

        self.info_Label = Label(self.view_frame, bg=GREEN, borderwidth=0, highlightthickness=0, font=FONT,
                                fg="white")
        self.info_Label.grid(row=4, pady=(0, 5), padx=(0, 10), sticky=NE)

        self.deal_button.pack(fill="x", side="left")
        self.load_title()

    def update_player_cards(self, cards, active_index=0):
        self.__update_player_card_frame(self.player_card_frame, cards=cards, active_index=active_index)

    def update_dealer_cards(self, cards, visible):
        hand = cards
        if not visible:
            hand = [hand[0], PlayingCard('back', 0, 'card')]
        self.__update_card_frame(self.dealer_card_frame, hand)

    def update_buttons(self, options: list):

        for widgets in self.button_frame.winfo_children():
            widgets.pack_forget()
        self.button_spacer_00.pack(fill="x", side="left")
        if "wager_down" in options:
            self.wager_down_btn.pack(fill="x", side="left")
            self.button_spacer_02.pack(fill="x", side="left")
        if "deal" in options:
            self.deal_button.pack(fill="x", side="left")
            self.button_spacer_01.pack(fill="x", side="left")
        if "wager_up" in options:
            self.wager_up_btn.pack(fill="x", side="left")
            self.button_spacer_03.pack(fill="x", side="left")
        if "double" in options:
            self.double_button.pack(fill="x", side="left")
            self.button_spacer_04.pack(fill="x", side="left")
        if "hit" in options:
            self.hit_me_button.pack(fill="x", side="left")
            self.button_spacer_02.pack(fill="x", side="left")
        if "stand" in options:
            self.stand_button.pack(fill="x", side="left")
            self.button_spacer_03.pack(fill="x", side="left")
        if "surrender" in options:
            self.surrender_button.pack(fill="x", side="left")
            self.button_spacer_05.pack(fill="x", side="left")
        if "split" in options:
            self.split_button.pack(fill="x", side="left")
            self.button_spacer_06.pack(fill="x", side="left")

    def button_clicked(self, name):
        self.clicked_button = name
        print(name)

    def update_message(self, status, custom=""):
        if custom == "":
            dialogue_list = self.dialogue_options[self.current_dealer][status]
            message = choice(dialogue_list)
        else:
            # if kwarg custom is used, any string can be put into message box. Mainly used for debugging
            message = custom
        self.speech_bubble.itemconfig(self.dealer_dialogue, text=message.upper())

    def update_scoreboard(self, wallet, wager):

        self.info_Label.config(
            text=f"WAGER:  ${wager}           WALLET:  ${wallet}")

    def __update_player_card_frame(self, frame: Frame, cards: list, active_index):
        for widgets in frame.winfo_children():
            widgets.destroy()

        for hand in cards:
            if cards.index(hand) == 1 and len(cards) > 1:
                Canvas(self.player_card_frame, bg=GREEN, borderwidth=0, highlightthickness=0, height=1, width=50).pack(
                    fill="x", side="left")
            for card in hand.cards:
                if cards.index(hand) == active_index:
                    image = self.card_images[f"cards/{card.suit}_{card.name}.png"]
                    Label(frame, image=image, bg=GREEN).pack(fill="x", side="left", padx=2)
                else:
                    image = self.small_card_images[f"cards/{card.suit}_{card.name}.png"]
                    Label(frame, image=image, bg=GREEN).pack(fill="x", side="left", padx=2)

    def __update_card_frame(self, frame: Frame, hand: list):
        for widgets in frame.winfo_children():
            widgets.destroy()

        for card in hand:
            image = self.card_images[f"cards/{card.suit}_{card.name}.png"]
            Label(frame, image=image, bg=GREEN).pack(fill="x", side="left", padx=2)

    def __load_card_images_from_file(self, deck):

        # load regular sized card images
        for card in deck[0:52]:
            file_name = f"cards/{card.suit}_{card.name}.png"
            card_image = self.__load_image(file_name, 100)
            self.card_images[file_name] = card_image

        # load smaller images for split hands
        for card in deck[0:52]:
            file_name = f"cards/{card.suit}_{card.name}.png"
            card_image = self.__load_image(file_name, 60)
            self.small_card_images[file_name] = card_image

        card_image = self.__load_image("cards/card_back.png", 100)
        self.card_images["cards/card_back.png"] = card_image

    def change_dealer(self, dealer_name):
        self.__load_dealer_image(dealer_name)
        self.current_dealer = dealer_name
        self.update_message("greeting")

    def __load_dealer_image(self, dealer_name="dealer"):
        for widgets in self.dealer_frame.winfo_children():
            widgets.pack_forget()

        self.top_left_canvas.pack(fill="x", side="left")

        self.observer_image = self.__load_image("images/swissguard.png", 240)
        # print(f"w{self.observer_image.width()} x h{self.observer_image.height()}")
        Label(self.dealer_frame, image=self.observer_image, bg=BLACK, borderwidth=0,
              highlightthickness=0).pack(fill="x", side="left", anchor="s")

        self.dealer_image = self.__load_image(f"images/{dealer_name}.png", 400)
        # print(f"w{self.dealer_image.width()} x h{self.dealer_image.height()}")
        Label(self.dealer_frame, image=self.dealer_image, bg=BLACK, borderwidth=0,
              highlightthickness=0).pack(fill="x", side="left", anchor="s")

        self.speech_bubble.pack(side="left", pady=30, anchor="n")
        self.top_right_canvas.pack(fill="x", side="left")

    @staticmethod
    def __load_image(file_path, h_size):
        image = Image.open(file_path)
        width_percent = (h_size / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(width_percent)))
        image = image.resize((h_size, hsize), Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def __load_dialogue_options_from_file(self):
        with open("data/dialogue.json") as json_file:
            self.dialogue_options = json.load(json_file)

    def load_title(self):
        for widgets in self.player_card_frame.winfo_children():
            widgets.destroy()
        for widgets in self.dealer_card_frame.winfo_children():
            widgets.destroy()
        image = self.card_images["cards/card_back.png"]
        Label(self.dealer_card_frame, image=image, bg=GREEN).pack(fill="x", side="left", padx=2)
        Label(self.dealer_card_frame, image=image, bg=GREEN).pack(fill="x", side="left", padx=2)
        Label(self.player_card_frame, image=image, bg=GREEN).pack(fill="x", side="left", padx=2)
        Label(self.player_card_frame, image=image, bg=GREEN).pack(fill="x", side="left", padx=2)

    def __set_aspect(self, content_frame, pad_frame, aspect_ratio):
        # a function which places a frame within a containing frame, and
        # then forces the inner frame to keep a specific aspect ratio

        def enforce_aspect_ratio(event):
            # when the pad window resizes, fit the content into it,
            # either by fixing the width or the height and then
            # adjusting the height or width based on the aspect ratio.

            # start by using the width as the controlling dimension
            desired_width = event.width
            desired_height = int(event.width / aspect_ratio)

            # if the window is too tall to fit, use the height as
            # the controlling dimension
            if desired_height > event.height:
                desired_height = event.height
                desired_width = int(event.height * aspect_ratio)

            # place the window, giving it an explicit size
            content_frame.place(in_=pad_frame, x=((self.pad_frame.winfo_width() - desired_width) / 2),
                                y=((self.pad_frame.winfo_height() - desired_height) / 2),
                                width=desired_width, height=desired_height)

        pad_frame.bind("<Configure>", enforce_aspect_ratio)

# blackjack-for-peasants

Blackjack for Peasants is a blackjack GUI made using tkinter. There are two dealer options along with chat gpt created dialogue for either dealer. The interpreter used during creation was Python 3.11

There is additional simulation code inside of main.py. It is currently commented out but is functional if you're Python savvy. The sim_model.py and code in main.py was left available in case anyone wants to play with it, and I intend to implement it into the GUI in a future version.

As a quick note, even though I understood the basic rules of BlackJack there were a lot of edege case rules I was unaware existed. As of this version here are the rules used:

* The game uses 6 standard 52 card decks for the shoe with a penetration of approximately 4.5 decks
* Natural Black Jack pays out at 1.5
* Early Surrender is available
* You can only Split once but can split aces and any combination of face cards
* Double Down is available but you can not double after splitting(for now)
* The Max wager is $5 with a minimum wager of $0 (this is in case you want to play without worrying about betting). 


<img src="https://github.com/andrewgernigin/blackjack-for-peasants/assets/135146706/8e2529c4-b621-439e-ab0c-2186b27fcbe5" width="830" height="662">

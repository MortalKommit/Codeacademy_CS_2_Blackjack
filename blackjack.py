import random
import requests
from urllib3.util import Retry
import logging

suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = [i for i in range(2,10)] + ['Jack', 'Queen', 'King', 'Ace']
card_values = {}
for rank in ranks:
    for suit in suits:
        if isinstance(rank, int):
            card_values[str(rank) + ' of ' + suit] = rank
        elif rank == 'Ace':
            card_values[rank + ' of ' + suit] = 11
        else:
            card_values[rank + ' of ' + suit] = 10

#logging object configuration (root logger)
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

#Tries to shuffle deck using random.org's True Randomness API
def shuffle_deck(cards):
    payload = {'min':0, 'max': len(cards) - 1, 'col':1, 'base':10, 'format':'plain', 'rnd':'new'}
    try:
        response = requests.get('https://random.org/sequences', params = payload)
        errored = False
    except requests.exceptions.RequestException as e:
        logging.error(f'Request Exception (Connection Error)\nDetails:{e.__context__}')
        errored = True
    if errored:
        random.shuffle(cards)
    elif getattr(response, 'status_code', None) == 200:
        order = response.text.splitlines()
        for index, card in enumerate(cards[:]):
            cards[int(order[index])] = card

class Player:
    def __init__(self):
        self.cards = []
        self.current_hand_value = 0
        self.name = 'Player'
    def play_game(self, deck):
        self.game_end = False
        print('Player turn!')
        choice = None
        while not self.check_current_hand() and choice != 2:
            try:
                choice = int(input('\nChoose an option\n1.Hit\n2.Stand : '))
                if choice == 1:
                    self.deal_cards(deck, 1)
            except ValueError:
                print('Invalid choice! Enter 1 or 2 as options')
    def deal_cards(self, deck, number_of_cards):
        for _ in range(0, number_of_cards):
            self.cards.append(deck.pop())
        self.update_value()
        self.show_cards()   
    #Shows dealer's cards if game_end = True
    def show_cards(self):
        print('Player hand:',self.cards, self.current_hand_value)
    def update_value(self):
        self.current_hand_value = 0
        #1st pass counts non-Ace values
        for card in self.cards:
            if 'Ace' not in card:   
                self.current_hand_value += card_values[card]
        #2nd pass adds Ace values
        for card in self.cards:
            if 'Ace' in card:   
                #Ace value is 1 if current_hand + card_value exceeds limit
                if self.current_hand_value + card_values[card] > 21:
                    self.current_hand_value += 1
                else:
                    self.current_hand_value += card_values[card]
    
    #Returns True if game is over (hand >= 21)
    def check_current_hand(self):
        if self.current_hand_value == 21:
            print('Blackjack!', self.name + ' wins!')
            self.game_end = True
            return True
        elif self.current_hand_value > 21:
            self.game_end = True
            print(self.name + ' Bust!')
            return True
        return False



class Dealer(Player):
    def __init__(self):
        self.cards = []
        self.current_hand_value = 0
        self.name = 'Dealer'
    #Override dealer's show cards to hide remaining card unless game end
    def show_cards(self, game_end = False):
        if not game_end:
            print('Dealer hand:', '[\'' + self.cards[0] + '\'', end = '')
            for _ in range(1, len(self.cards)):
                print(", Hidden Card", end = '')
            print(']')
        else:
            print('Dealer hand:',self.cards, self.current_hand_value)

    #Returns True if drawing card is safe else False
    def dealer_algorithm(self, cards, player, simple = True):
        if simple:
            if self.current_hand_value < 17:
                return True
            else:
                return False
        else:
            no_of_cards_that_bust = 0
            no_of_safe_cards = 0

            for card in cards:
                if 'Ace' not in card:
                    if card_values[card] + self.current_hand_value > 21:
                        no_of_cards_that_bust += 1
                    elif card_values[card] + self.current_hand_value > player.current_hand_value:
                        no_of_safe_cards += 1
                else:
                    #Ace only counts as bust if it's value as 1 also counts as bust
                    if 1 + self.current_hand_value > 21:
                        no_of_cards_that_bust += 1
                    elif card_values[card] + self.current_hand_value > player.current_hand_value:
                        no_of_safe_cards += 1
                    elif 1 + self.current_hand_value > player.current_hand_value:
                        no_of_safe_cards += 1
            prob_safe_hand = 1.0 * no_of_safe_cards / len(cards)
            prob_unsafe_hand = 1.0 * no_of_cards_that_bust / len(cards)
            if prob_safe_hand > prob_unsafe_hand:
                return True
            else:
                return False
             
    def play_game(self, deck, player):
        self.bust = False
        print('Dealer turn!')
        while not self.check_current_hand() and self.dealer_algorithm(deck, player):
            print('Dealer hits!')
            self.deal_cards(deck, 1)
        print('Dealer stands!')
        self.show_cards(game_end = True)
        self.compare_hands(player)

    def compare_hands(self, player):
        if player.current_hand_value == self.current_hand_value:
            print("Push!")
        elif player.current_hand_value > self.current_hand_value:
            print("Player wins!")
        else:
            print("House wins!")

def play_blackjack():
    play_again = True
    while play_again:

        #New deck of cards every
        cards = list(card_values.keys())
        print('::::::::     Blackjack     ::::::::\n\n')
        player = Player()
        dealer = Dealer()
        
        #Set cards to None at start of round to overwrite previous values
        player.cards = list()
        dealer.cards = list()
        shuffle_deck(cards)

        player.deal_cards(cards, 2)
        dealer.deal_cards(cards, 2)
        player.play_game(cards)
        if not player.game_end:
            dealer.play_game(cards, player)
        choice = input('Play again?(y/n):')
        if choice.upper() == 'Y':
            play_again = True
        else:
            play_again = False
play_blackjack()
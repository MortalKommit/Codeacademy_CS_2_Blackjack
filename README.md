# Codeacademy Counter Science Project : Blackjack 2

## Goal

Build a console application that allows the user to play blackjack versus a computer dealer.  

## User Stories/Features as described by the challenge

Basic

User Story: As a user I want to clearly see the cards dealt to me and to the dealer.

User Story: As a user I want to be able to choose to stay.

User Story: As a user I want to be able to choose to hit until I choose to stay or until I bust.

User Story: As a user I want to clearly see the sequence of moves made by the dealer.

User Story: As a user I want to clearly see who won and why.

User Story: As a user I want to be able to quit the game or go again after each cycle.

Intermediate Challenge

User Story: As a user I want the game to incorporate a virtual chip/currency system to simulate real-life  staking mechanics.

User Story: As a user I want to clearly see my chip stack, as well as that of the dealer.

User Story: As a user I want to be able to vary my bet according to the min/max betting rules.

Advanced Challenge

User Story: As a user I want to be able to choose to split my hand whenever possible.

User Story: As a user I want to be able to choose to double down whenever possible.

### Installation instructions  

Installed via pipenv (pipenv install)  
OR  
pip install -r requirements.txt

### Features that the project implements  

1. View cards dealt to dealer and player  
2. Deck shuffled via random.org API or if unavailable, python's random.shuffle()  
3. Player prompted for staked game at the start of program (for betting)  
4. Prompted to play again until player does not enter 'y' or if player runs out of money  
5. Choice of varying bet amount between rounds (10/25/50/100)  
6. Dealer's cards hidden until player stands  
7. Player allowed to hit or stand until blackjack/bust  
8. A probability-based dealer algorithm can be used by setting simple = False in the call to dealer_algorithm()  

### Planned features/difficulties
- Dealer (The House) typically does not have a fund limit
- Splitting needs to be implemented, but would require changing cards from a 1-dimensional list
to a list of lists and iterating over them in turn
- Not all variants allow for doubling down whenever possible (Some allow if  
the player's total face value is between 9 and 11, inclusive)

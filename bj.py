'''
card_game (21)
11-27-14
'''

import random


def opening_message():
    print("Welcome to 21! Here are the game rules.")
    print("- The goal of each round is to get the value of your hand to 21.")
    print("- You start off with 100 points for the game.")
    print("- Each round, an amount of points equal to 21 - your hand's value \n\
will be subtracted from your game points.")
    print("- Your goal is to have the greatest amount of points\
after 5 rounds.")
    print("Good luck!")
    print()


def create_deck():
    deck = []
    suit_list = ['clubs', 'diamonds', 'hearts', 'spades']
    card_list = ['ace', '2', '3', '4', '5', '6', '7',
                 '8', '9', '10', 'jack', 'queen', 'king']
    for suit in suit_list:
        for card in card_list:
            card_dict = {}
            card_dict['name'] = card
            card_dict['suit'] = suit
            if card_list.index(card) < 10:
                card_dict['value'] = (card_list.index(card)+1)
            else:
                card_dict['value'] = 10
            card_dict['display'] = (card + ' of ' + suit)
            deck.append(card_dict)
    return deck


def pick_card(deck):
    random.shuffle(deck)
    card = deck.pop()
    return card


def find_card_value(card_list):
    value = 0
    for card in card_list:
        value += card['value']
    return value


def hit_me(picked_cards, deck):
    pick_another = input("Do you want to draw another card? ")
    pick_another = pick_another.strip().lower()

    value = find_card_value(picked_cards)
    while pick_another.startswith('y') and value < 21:
        card = pick_card(deck)
        print("You drew the", card['display'])
        picked_cards.append(card)

        value = find_card_value(picked_cards)
        print("Your", len(picked_cards), "cards add up to", value)
        print()
        if value < 21:
            pick_another = input("Do you want to draw another card? ")
            print()
        else:
            return value
    return value


def get_rank(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def main():
    score = 100
    counter = 1
    opening_message()
    while counter <= 5:
        print("Round ", counter, "\n")

        deck = create_deck()
        picked_cards = []

        first_card = pick_card(deck)
        print("First card:", first_card['display'])
        picked_cards.append(first_card)

        second_card = pick_card(deck)
        print("Second card:", second_card['display'])
        picked_cards.append(second_card)

        value = find_card_value(picked_cards)
        print("Those 2 cards add up to a value of", value)
        print()

        if value < 21:
            value = hit_me(picked_cards, deck)

        if value > 21:
            print("Whoops! You went bust!")
            score = score - 21
        else:
            print("You ended this round with a hand valued at",
                  value, "points.")
            score = score - (21-value)

        if counter < 5:
            print("Your score is now", score)
        print()
        counter += 1
    print("Your score on this game was", score, "out of 100")
    print("Your rank on this game was:", get_rank(score))


main()
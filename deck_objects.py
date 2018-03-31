import random

class Deck(object):
    """
        Object that keeps track of the total deck, the cards in play and the used cards
    """
    full_deck = [['3', '♦', [3]], ['J', '♦', [10]], ['8', '♦', [8]], ['9', '♦', [9]], ['5', '♦', [5]], ['2', '♦', [2]],
                 ['A', '♦', [1, 11]], ['K', '♦', [10]], ['4', '♦', [4]], ['7', '♦', [7]], ['T', '♦', [10]],
                 ['Q', '♦', [10]], ['6', '♦', [6]], ['3', '♠', [3]], ['J', '♠', [10]], ['8', '♠', [8]], ['9', '♠', [9]],
                 ['5', '♠', [5]], ['2', '♠', [2]], ['A', '♠', [1, 11]], ['K', '♠', [10]], ['4', '♠', [4]],
                 ['7', '♠', [7]], ['T', '♠', [10]], ['Q', '♠', [10]], ['6', '♠', [6]], ['3', '♥', [3]],
                 ['J', '♥', [10]], ['8', '♥', [8]], ['9', '♥', [9]], ['5', '♥', [5]], ['2', '♥', [2]],
                 ['A', '♥', [1, 11]], ['K', '♥', [10]], ['4', '♥', [4]], ['7', '♥', [7]], ['T', '♥', [10]],
                 ['Q', '♥', [10]], ['6', '♥', [6]], ['3', '♣', [3]], ['J', '♣', [10]], ['8', '♣', [8]], ['9', '♣', [9]],
                 ['5', '♣', [5]], ['2', '♣', [2]], ['A', '♣', [1, 11]], ['K', '♣', [10]], ['4', '♣', [4]],
                 ['7', '♣', [7]], ['T', '♣', [10]], ['Q', '♣', [10]], ['6', '♣', [6]]]

    def __init__(self, decks=1, deck_penetration=0):
        self.available_cards = []
        combined_decks = Deck.full_deck * decks
        for c in combined_decks:
            self.available_cards.append(Card(c))
        self.deck_size = len(self.available_cards)
        self.used_cards = []
        self.in_play_cards = []
        self.target_deck_penetration = deck_penetration
        self.shuffle()

    @property
    def penetraion(self):
        """
        :return: Percent of the deck that is currently being used
        """
        return round(((len(self.in_play_cards) + len(self.used_cards)) / (self.deck_size)) * 100, 2)

    def __repr__(self):
        return "Decks {} | Cards {} | Status: {}/{}/{} {}%".format(self.deck_size / 52, self.deck_size,
                                                                   len(self.available_cards), len(self.in_play_cards),
                                                                   len(self.used_cards), self.penetraion)

    def deal(self):
        """
            Deal a new hand of 2 cards
        :return: list of two cards
        """
        return [self.draw(), self.draw()]

    def draw(self):
        """
            Draw one more card into a hand
        :return: a single card object
        """
        if self.check_card_availability():
            current_card = self.available_cards.pop()
            self.in_play_cards.append(current_card)
            return current_card
        else:
            print("ERROR: All cards in play")
            return None

    def return_cards(self, cards):
        """
            Take cards from the list and move them to the used_cards list
        :param cards: any number of cards in a list
        :return:
        """
        for c in cards:
            if c in self.in_play_cards:
                self.in_play_cards.remove(c)
                self.used_cards.append(c)
            else:
                print("ERROR = {} was not in play?".format(c))

    def check_card_availability(self):
        if len(self.available_cards) == 0 and len(self.used_cards) == 0:
            return False
        elif (len(self.available_cards) == 0 or self.penetraion >= self.target_deck_penetration) and len(
                self.used_cards) > 0:
            self.shuffle()
            return True
        else:
            return True

    def shuffle(self):
        for c in range(len(self.used_cards)):
            self.available_cards.append(self.used_cards.pop())
        random.shuffle(self.available_cards)

    @property
    def num_decks(self):
        return self.deck_size / 52


class Card(object):
    def __init__(self, card_list):
        """
        :param card_list: in format ['value name','suit name','card value']
        :return:
        """
        self.suit = card_list[1]
        self.name = card_list[0]
        self.values = card_list[2]

    def __repr__(self):
        return "{}{}".format(self.name, self.suit)


class Hand(object):
    """
        Current hand of play
    """

    def __init__(self, cards, player, bet=0, is_split=False):
        self.cards = cards
        self.player = player
        self.bet = bet
        self.is_stand = False
        self.is_split = is_split
        self.actions_taken = []

    @property
    def values(self):
        """

        :return: List of all possible values for a hand
        """
        values = []
        for c in self.cards:
            if values == []:
                values = c.values
            else:
                values = [sum([x, y]) for x in c.values for y in values]
        return values

    @property
    def max_value(self):
        """
        :return: The highest value of a hand 21 or below. Or if no value below 21, return highest value
        """
        max_val = max(self.values)
        if max_val > 21 and len(self.values) > 1:
            max_val = max(v for v in self.values if v <= 21)
        return max_val

    @property
    def min_value(self):
        """
        :return: Lowest value a hand has
        """
        return min(self.values)

    @property
    def blackjack(self):
        """
        :return: True if hand is a blackjack
        """
        if len(self.cards) == 2:
            if self.max_value == 21:
                return True
        else:
            return False

    @property
    def bust(self):
        """
        :return: True if all values are above 21
        """
        if self.min_value > 21:
            return True
        else:
            return False

    @property
    def soft(self):
        """
        :return: True if one of the cards is an Ace (and therefore has multiple possible values
        """
        if len(self.values) > 1:
            return True
        else:
            return False

    @property
    def showing_ace(self):
        """
        For insurance
        :return: True if first card is an ACE - For insurance purposes
        """
        if self.cards[0].name == "A":
            return True
        else:
            return False

    @property
    def can_split(self):
        """
        :return: True if the hand can be split (2 of the same card, ignoreing suits)
        """
        if self.is_split and self.player.game.rules["multi_split"] is False:
            print("Already Split")
            return False
        elif len(self.cards) == 2 and self.cards[0].name == self.cards[1].name:
            return True
        else:
            return False

    @property
    def can_double(self):
        if self.player.game.rules["double_after_split"] is False and self.is_split is True:
            return False
        if len(self.cards) == 2:
            return True
        else:
            return False

    ##
    ##  Showing the hand
    ##
    def __repr__(self):
        """
        :return: Text sting with no spaces between card names
        """
        name = ""
        for c in self.cards:
            name += "{}".format(str(c))
        return name

    def __str__(self):
        """
        :return: Text sting with spaces between card names
        """
        name = ""
        for c in self.cards:
            name += "{} ".format(str(c))
        return name

    def card_names(self):
        """
        :return: Text sting with no suits
        """
        name = ""
        for c in self.cards:
            name += "{}".format(c.name)
        return name

    def show_player_hand(self):
        """
        :return: The text string for the hand
        """
        return self.__str__()

    def show_player_value(self):
        """
        :return: All possible values for the hand or blackjack
        """
        if self.blackjack: return "Blackjack"
        return self.values

    def show_dealer_hand(self):
        """
        :return: If blackjack, show the hand. Otherwise just show the first card
        """
        name = ""
        if self.blackjack: return self.show_player_hand()
        for c in self.cards:
            name += "{} ".format(str(c))
            break
        return name + "##"

    def show_dealer_value(self):
        """
        :return: If blackjack, show blackjacj. Otherwise just show the value of the first card
        """
        value = ""
        if self.blackjack: return "Blackjack"
        for c in self.cards:
            value = c.values
            break
        return value

    ##
    ##  Playing the hand
    ##
    def draw(self):
        """
        :return: Add a card to the hand
        """
        assert (self.player.game.deck is not None)
        self.cards.append(self.player.draw())
        return 0

    def stand(self):
        self.is_stand = True
        return 1

    def split(self):
        if self.can_split:
            new_hands = [Hand([self.cards[0], self.player.draw()], self.player, self.bet),
                         Hand([self.cards[1], self.player.draw()], self.player, self.bet)]
            return new_hands




class HandMatchup(object):
    def __init__(self, player_hand, dealer_hand):
        self.name = HandMatchup.matchup_string(player_hand, dealer_hand)
        # if "'" in self.name: print(self.name)
        self.db_id = None
        self.action_record = {"hit": {"played": 0, "won": 0, "lost": 0, "mwon": 0, "mlost": 0},
                              "stand": {"played": 0, "won": 0, "lost": 0, "mwon": 0, "mlost": 0},
                              "split": {"played": 0, "won": 0, "lost": 0, "mwon": 0, "mlost": 0},
                              "doub": {"played": 0, "won": 0, "lost": 0, "mwon": 0, "mlost": 0},
                              "lost_to_blackjack": {"played": 0, "won": 0, "lost": 0, "mwon": 0, "mlost": 0},
                              "push": {"played": 0, "won": 0, "lost": 0, "mwon": 0, "mlost": 0},
                              "bust": {"played": 0, "won": 0, "lost": 0, "mwon": 0, "mlost": 0}
                              }

    CARD_VALUES = {"A": [1, 11], "2": [2], "3": [3], "4": [4], "5": [5], "6": [6], "7": [7], "8": [8], "9": [9],
                   "T": [10], "J": [10], "Q": [10], "K": [10]}



    @staticmethod
    def build_matchup_from_array(m_array):
        if len(m_array) != 29:
            print(len(m_array), "LEN ERROR")
            return None
        else:
            new_matchup = HandMatchup(m_array[2], m_array[3])
            new_matchup.db_id = m_array[0]
            new_matchup.action_record = {
                "stand": {"played": m_array[4], "won": m_array[5], "lost": m_array[6], "mwon": m_array[7],
                          "mlost": m_array[8]},
                "hit": {"played": m_array[9], "won": m_array[10], "lost": m_array[11], "mwon": m_array[12],
                        "mlost": m_array[13]},
                "doub": {"played": m_array[14], "won": m_array[15], "lost": m_array[16], "mwon": m_array[17],
                         "mlost": m_array[18]},
                "split": {"played": m_array[19], "won": m_array[20], "lost": m_array[21], "mwon": m_array[22],
                          "mlost": m_array[23]},
                "lost_to_blackjack": {"played": m_array[25], "won": 0, "lost": m_array[25], "mwon": 0,
                                      "mlost": m_array[26]},
                "push": {"played": m_array[24], "won": 0, "lost": 0, "mwon": 0, "mlost": 0},
                "bust": {"played": m_array[27], "won": 0, "lost": m_array[27], "mwon": 0, "mlost": m_array[28]}
            }
            return {new_matchup.name: new_matchup}

    @staticmethod
    def values(hand):
        values = []
        for c in hand:
            if values == []:
                values = HandMatchup.CARD_VALUES[c]
            else:
                values = [sum([x, y]) for x in HandMatchup.CARD_VALUES[c] for y in values]
        return values

    @property
    def player_hand(self):
        return self.name.split("+")[0]

    @property
    def num_cards(self):
        return len(self.player_hand)

    @property
    def dealer_hand(self):
        return self.name.split("+")[1]

    @property
    def player_hand_max_value(self):
        value_list = HandMatchup.values(self.player_hand)
        max_val = max(value_list)
        min_val = min(value_list)
        #if max value is greater than 21 find other possible max values
        if max_val > 21 and min_val < 21 and len(value_list) > 1:
            max_val = max(v for v in value_list if v <= 21)
        return max_val

    @property
    def player_hand_min_value(self):
        return min(HandMatchup.values(self.player_hand))

    @property
    def played(self):
        return max((self.action_record["hit"]["played"] + \
                    self.action_record["stand"]["played"] + \
                    self.action_record["split"]["played"] + \
                    self.action_record["doub"]["played"] + \
                    self.action_record["lost_to_blackjack"]["lost"]), 1)

    @property
    def won(self):
        return self.action_record["hit"]["won"] + \
               self.action_record["stand"]["won"] + \
               self.action_record["split"]["won"] + \
               self.action_record["doub"]["won"]

    @property
    def lost(self):
        return self.action_record["hit"]["lost"] + \
               self.action_record["stand"]["lost"] + \
               self.action_record["split"]["lost"] + \
               self.action_record["doub"]["lost"] + \
               self.action_record["lost_to_blackjack"]["lost"]

    @property
    def can_split(self):
        self_string = self.name
        if len(self_string) == 4:
            if self_string[0] == self_string[1]:
                return True
        return False

    @property
    def hit_prob(self):
        if self.action_record["hit"]["played"] != 0:
            return round(((self.action_record["hit"]["mwon"] - self.action_record["hit"]["mlost"]) /
                          self.action_record["hit"]["played"]), 2) * 100
            # return round(self.action_record["hit"]["won"]/self.action_record["hit"]["played"]*100,2)
        else:
            return "UNKN"

    @property
    def hit_report(self):
        return "HIT {}/{} {}% @ {}%".format(self.action_record["hit"]["played"], self.played,
                                            round(self.action_record["hit"]["played"] / self.played * 100, 2),
                                            self.hit_prob)

    @property
    def split_prob(self):
        if self.action_record["split"]["played"] != 0:
            return round(((self.action_record["split"]["mwon"] - self.action_record["split"]["mlost"]) /
                          self.action_record["split"]["played"]), 2) * 100
        else:
            if self.can_split:
                return "UNKN"
            return None

    @property
    def split_report(self):
        return "Split {}/{} {}% @ {}%".format(self.action_record["split"]["played"], self.played,
                                              round(self.action_record["split"]["played"] / self.played * 100, 2),
                                              self.split_prob)

    @property
    def stand_prob(self):
        if self.action_record["stand"]["played"] != 0:
            return round(((self.action_record["stand"]["mwon"] - self.action_record["stand"]["mlost"]) /
                          self.action_record["stand"]["played"]), 2) * 100
        else:
            return "UNKN"

    @property
    def stand_report(self):
        return "STAND {}/{} {}% @ {}%".format(self.action_record["stand"]["played"], self.played,
                                              round(self.action_record["stand"]["played"] / self.played * 100, 2),
                                              self.stand_prob)

    @property
    def doub_prob(self):
        if self.action_record["doub"]["played"] != 0:
            return round(((self.action_record["doub"]["mwon"] - self.action_record["doub"]["mlost"]) /
                          self.action_record["doub"]["played"]), 2) * 100
        else:
            return "UNKN"

    @property
    def doub_report(self):
        return "DOUB {}/{} {}% @ {}%".format(self.action_record["doub"]["played"], self.played,
                                             round(self.action_record["doub"]["played"] / self.played * 100, 2),
                                             self.doub_prob)

    @property
    def bust_report(self):
        return "BUST {}/{} {}%".format(self.action_record["bust"]["played"], self.played,
                                       round(self.action_record["bust"]["played"] / self.played * 100, 2))

    @property
    def push_report(self):
        return "PUSH {}/{} {}%".format(self.action_record["push"]["played"], self.played,
                                       round(self.action_record["push"]["played"] / self.played * 100, 2))

    @property
    def l2bj_report(self):
        return "L2BJ {}/{} {}%".format(self.action_record["lost_to_blackjack"]["played"], self.played,
                                       round(self.action_record["lost_to_blackjack"]["played"] / self.played * 100, 2))

    def filtered_probabilities(self, play_options):
        probs = self.probabilities
        fprobs = {}
        for k in probs.keys():
            if k in play_options:
                fprobs[k] = probs[k]
        return fprobs

    @property
    def probabilities(self):
        probs = {"hit": self.hit_prob, "stand": self.stand_prob, "doub": self.doub_prob}
        if self.can_split:
            probs["split"] = self.split_prob
        for p in probs:
            if probs[p] == "UNKN":
                probs[p] = -201
        return probs

    def update_action(self, action, won, mwon):
        self.action_record[action]["played"] += 1
        if won > 0:
            # print("won",action,won,mwon)
            self.action_record[action]["won"] += won
            self.action_record[action]["mwon"] += mwon
        elif won < 0:
            # print("lost",action,won,mwon)
            self.action_record[action]["lost"] -= won  # minus negative == addition
            self.action_record[action]["mlost"] += mwon
        else:
            pass
            # print(action)
            # print("PUSH--")
            # self.action_record["push"]["played"] += 1

            # print(self.__repr__())

    def pick_random_action(self, play_options):
        return random.choice(list(self.filtered_probabilities(play_options).keys()))

    def pick_action(self, play_options, delay=0):
        MIN_RAND = delay
        choice = None
        if self.played > MIN_RAND:
            choice = weighted_choice(self.filtered_probabilities(play_options))
            # return choice
            # if choice and self.action_record[choice]["played"] > MIN_RAND / 3:
            #     return choice
        else:
            choice = self.pick_random_action(play_options)
        return choice

    @property
    def clear_top_choice(self):
        if -201 in self.probabilities.values():
            return False # Un-used options go to random
        action_1, action_2 = sorted(self.probabilities, key=self.probabilities.get, reverse=True)[:2]
        if abs(self.probabilities[action_1]-self.probabilities[action_2])<25:
            return False
        return True

    def get_top_choice(self, play_options):
        top_action = max(self.filtered_probabilities(play_options), key=self.filtered_probabilities(play_options).get)
        return top_action#, self.filtered_probabilities(play_options)[top_action]

    @property
    def top_choice(self):
        top_action = max(self.probabilities, key=self.probabilities.get)
        return top_action#, self.probabilities[top_action]

    @property
    def top_choiceP(self):
        top_action = max(self.probabilities, key=self.probabilities.get)
        return top_action , self.probabilities[top_action]

    # @property
    # def top_2_choices(self):
    #     top_choices = sorted(self.probabilities, key=self.probabilities.get, reverse=True)[:2]
    #     #top_probabilities = [self.probabilities[top_choices[0]], self.probabilities[top_choices[1]]]
    #     return top_choices#, top_probabilities

    def __repr__(self):
        if self.can_split:
            return "{} = TOP: {} | TOTAL WON: {}% | {} | {} | {} | {} | {} | {} | {}".format(self.name, self.top_choice,
                                                                                             round(
                                                                                                 self.won / self.played * 100,
                                                                                                 2), self.stand_report,
                                                                                             self.hit_report,
                                                                                             self.doub_report,
                                                                                             self.split_report,
                                                                                             self.push_report,
                                                                                             self.bust_report,
                                                                                             self.l2bj_report)
        else:
            return "{} = TOP: {} | TOTAL WON: {}% | {} | {} | {} | {} | {} | {}".format(self.name, self.top_choice,
                                                                                        round(
                                                                                            self.won / self.played * 100,
                                                                                            2), self.stand_report,
                                                                                        self.hit_report,
                                                                                        self.doub_report,
                                                                                        self.push_report,
                                                                                        self.bust_report,
                                                                                        self.l2bj_report)

    def __str__(self):
        return self.__repr__()

    @property
    def _matchup_array(self):
        """
        :return: Array used to save and load matchups
        """
        return (self.name,
                self.player_hand,
                self.dealer_hand,
                self.player_hand_max_value,
                self.player_hand_min_value,
                self.action_record["stand"]["played"],
                self.action_record["stand"]["won"],
                self.action_record["stand"]["lost"],
                self.action_record["stand"]["mwon"],
                self.action_record["stand"]["mlost"],
                self.action_record["hit"]["played"],
                self.action_record["hit"]["won"],
                self.action_record["hit"]["lost"],
                self.action_record["hit"]["mwon"],
                self.action_record["hit"]["mlost"],
                self.action_record["doub"]["played"],
                self.action_record["doub"]["won"],
                self.action_record["doub"]["lost"],
                self.action_record["doub"]["mwon"],
                self.action_record["doub"]["mlost"],
                self.action_record["split"]["played"],
                self.action_record["split"]["won"],
                self.action_record["split"]["lost"],
                self.action_record["split"]["mwon"],
                self.action_record["split"]["mlost"],
                self.action_record["push"]["played"],
                self.action_record["lost_to_blackjack"]["played"],
                self.action_record["lost_to_blackjack"]["mlost"],
                self.action_record["bust"]["played"],
                self.action_record["bust"]["mlost"],
                self.stand_prob,
                self.hit_prob,
                self.doub_prob,
                self.split_prob,
                self.top_choice[0],
                self.top_choice[1],
                "{}+{}".format(self.player_hand_max_value, self.dealer_hand),
                self.num_cards)


    @staticmethod
    def matchup_string(player_hand, dealer_hand):
        if type(player_hand) == Hand:
            return HandMatchup.sort_string(player_hand.card_names()) + "+" + repr(dealer_hand)[0]
        else:
            player_hand = player_hand.translate({ord(i): None for i in "♣♠♥♦"})
            if type(dealer_hand) == Hand:
                return HandMatchup.sort_string(player_hand) + "+" + repr(dealer_hand)[0]
            else:
                return HandMatchup.sort_string(player_hand) + "+" + dealer_hand[0]

    @staticmethod
    def sort_string(cards):
        sorted_cards = ''.join(sorted(cards[:2]))
        return sorted_cards + cards[2:]


def weighted_choice(choices):
    adjust_min = abs(min(choices.values()))
    if adjust_min==201: return None # This means one of the options hasn't been choosen yet so percentages may not be accurate
    sub_choices = {(c, w+adjust_min) for c, w in choices.items()}# if w>=0}
    total = sum(w for c, w in sub_choices)
    r = random.uniform(0, total)
    if total == 0:
        return None
    upto = 0
    for c, w in sub_choices:
        wa = w
        if upto + wa > r:
            return c
        upto += wa
    assert False, "Shouldn't get here"





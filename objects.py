import random
import database as db
import os
from basic_strategy_dicts import basic


class deck(object):
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
        combined_decks = deck.full_deck * decks
        for c in combined_decks:
            self.available_cards.append(card(c))
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


class card(object):
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


class hand(object):
    """
        Current hand of play
    """

    def __init__(self, cards, player, bet=0, is_split=False):
        self.cards = cards
        self.player = player
        self.bet = bet
        # self.winlose = 0 # 1 for won, 0 for lost
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
            new_hands = [hand([self.cards[0], self.player.draw()], self.player, self.bet),
                         hand([self.cards[1], self.player.draw()], self.player, self.bet)]
            return new_hands


class player(object):
    MANUAL_PLAY = 1
    RULES_PLAY = 2
    RANDOM_PLAY = 3
    WEIGHTED_PLAY = 4
    TOP_CHOICE = 5
    BASIC_STRATEGY = 6

    def __init__(self, dealer=False, name="", current_game=None, play_type=4, hands=None, play_type_delay=1000):
        self.hands = []  # Plural because of split possibilities
        self.db_id = None
        self.dealer = dealer  # True if player is dealer
        self.default_bet = 1
        self.money = 0
        self.hands_played = 0
        self.hands_won = 0
        self.hands_lost = 0
        self.hands_push = 0
        self.money_won = 0
        self.money_lost = 0
        self.recent_record = []
        if hands is not None:
            self.money = hands["money"]
            self.hands_played = hands["hands_played"]
            self.hands_won = hands["hands_won"]
            self.hands_lost = hands["hands_lost"]
            self.hands_push = hands["hands_push"]
            self.money_won = hands["money_won"]
            self.money_lost = hands["money_lost"]

        if self.dealer:
            self.play_type = player.RULES_PLAY
        else:
            self.play_type = play_type

        self.play_type_delay = play_type_delay

        if dealer:
            self.name = "Dealer"
        else:
            self.name = name

        self.game = current_game
        print(self.name, self.hands_played)

    @property
    def all_hands_stand(self):
        if len(self.hands) == 0: return False
        for h in self.hands:
            if h.is_stand is False:
                return False
        return True

    @property
    def has_blackjack(self):
        if len(self.hands) == 0: return False
        for h in self.hands:
            if h.blackjack is True:
                return True
        return False

    @property
    def current_bet(self):
        """
        :return: Sum of all the best on the players hands
        """
        cbet = 0
        for h in self.hands:
            cbet += h.bet
        return cbet

    @property
    def all_hands_bust(self):
        if len(self.hands) == 0: return False
        for h in self.hands:
            if h.bust is False:
                return False
        return True

    def deal_hand(self):
        self.hands.append(hand(self.game.deck.deal(), player=self))
        for h in self.hands:
            self.bet(h)

    def show_deal(self):
        hands = "{} playing: ".format(self.name)
        for i, h in enumerate(self.hands):
            if self.dealer:
                hands += "{}: {} | ".format(h.show_dealer_hand(), h.show_dealer_value())
            else:
                hands += "{}: {} ${} | ".format(h.show_player_hand(), h.show_player_value(), h.bet)
        return print(hands)

    def show_hand(self, hand, action):
        if self.game.verbose: print(
            "  {} | Cards {} | Value {} | Bet ${}".format(action, hand.show_player_hand(), hand.show_player_value(),
                                                          hand.bet))

    def draw(self):
        return self.game.deck.draw()

    def play_options(self, hand):
        if hand is None: return
        options = {}
        options["stand"] = self.stand
        if hand.min_value < 21:
            options["hit"] = self.hit
            if self.dealer is False and hand.can_double is True:
                options["doub"] = self.doubledown
        if hand.can_split and self.dealer is False:
            options["split"] = self.split
        return options

    def play_hands(self):
        while self.all_hands_stand is False:
            for h in self.hands:
                if self.game.verbose:
                    if self.dealer:
                        print("Dealer playing hand {} {}".format(h, h.values))
                    else:
                        print("{} playing hand {} {}".format(self.name, h, h.values))
                if h.is_stand: continue
                if self.play_type == player.MANUAL_PLAY:
                    self.manual_play_hand(h)
                if self.play_type == player.RULES_PLAY:
                    self.auto_play_hand_rules(h)
                if self.play_type == player.RANDOM_PLAY:
                    self.auto_play_hand_random(h)
                if self.play_type == player.WEIGHTED_PLAY:
                    self.auto_play_hand_weighted(h)
                if self.play_type == player.TOP_CHOICE:
                    self.auto_play_hand_top(h)
                if self.play_type == player.BASIC_STRATEGY:
                    self.auto_play_hand_basic_strategy(h)

    def bet(self, hand):
        if self.game.verbose: print("Betting {}".format(self.default_bet))
        self.money -= self.default_bet
        hand.bet += self.default_bet

    def hit(self, hand):
        hand.actions_taken.append(["hit", repr(hand)])
        hand.draw()
        if self.game.verbose: self.show_hand(hand, "Hit")

    def stand(self, hand):
        hand.actions_taken.append(["stand", repr(hand)])
        hand.stand()
        if self.game.verbose: print("  Stand")

    def split(self, hand):
        chand = hand
        self.hands.remove(hand)
        self.money -= chand.bet
        shands = chand.split()
        shands[0].actions_taken.append(["split", repr(chand)])
        shands[1].actions_taken.append(["split", repr(chand)])

        self.hands.extend(shands)
        if self.game.verbose: print("  Split: {} | {}".format(shands[0], shands[1]))

    def doubledown(self, hand):
        hand.actions_taken.append(["doub", repr(hand)])
        self.bet(hand)
        hand.draw()
        if hand.bust:
            self.bust(hand)
        else:
            self.stand(hand)
        self.show_hand(hand, "DDn")

    def bust(self, hand):
        hand.stand()
        hand.actions_taken.append(["bust", repr(hand)])
        if self.game.verbose: print("  Busted")

    def lost_to_blackjack(self, hand):
        hand.stand()
        hand.actions_taken.append(["lost_to_blackjack", repr(hand)])

    def push(self, hand):
        hand.stand()
        hand.actions_taken.append(["push", repr(hand)])

    def manual_play_hand(self, chand):
        pass

    def auto_play_hand_random(self, chand):
        while not chand.is_stand:
            if chand.bust:
                self.bust(chand)
                break
            if not chand.bust and not chand.blackjack:
                play_options = self.play_options(chand)
                play_choice = play_options[random.choice(play_options.keys())]
                play_choice(chand)
                if play_choice == self.split:
                    break
            else:
                self.stand(chand)

    def auto_play_hand_rules(self, chand):
        while not chand.is_stand:
            if chand.bust:
                self.bust(chand)
                break
            if not chand.bust and not chand.blackjack:
                if chand.max_value == 17 and chand.min_value < 17 and chand.soft:
                    # If it is a hard 17 don't follow these rules
                    # A+6 = True
                    # A+T+5 = False
                    if self.game.rules["soft_17_hit"]:
                        self.stand(chand)
                    else:
                        self.hit(chand)
                elif chand.max_value <= 16:
                    # Hit if hand is 16 or less. Max value gives largest value 21 or below so this doesn't
                    #  need any more qualifiers
                    self.hit(chand)
                else:
                    self.stand(chand)

    def auto_play_hand_weighted(self, chand):
        while not chand.is_stand:
            if chand.bust:
                self.bust(chand)
                break
            if not chand.bust and not chand.blackjack:
                choice = self.game.get_matchup_choice(chand, delay=self.play_type_delay)
                play_options = self.play_options(chand)
                if not choice or choice not in play_options:
                    play_choice = play_options[random.choice(list(play_options.keys()))]
                else:
                    play_choice = play_options[choice]
                play_choice(chand)
                if play_choice == self.split:
                    break
            elif chand.blackjack:
                self.stand(chand)

            else:
                print("NO ACTION {}".format(chand))
                self.stand(chand)

    def auto_play_hand_basic_strategy(self, chand):
        bs_db = basic[self.game.bs_name]
        play_options = self.play_options(chand)
        while not chand.is_stand:
            if chand.bust:
                self.bust(chand)
                break

            def make_bs_matchup(chand):
                dealer_card = repr(self.game.current_dealer_hand)[0]
                c_hand = chand.card_names()
                # print(c_hand)
                if chand.can_split:
                    c_hand = c_hand.replace("J", "T").replace("Q", "T").replace("K", "T")
                    return "{},{}X{}".format(c_hand[0], c_hand[1], dealer_card)
                elif chand.soft and chand.max_value >= 13 and chand.max_value <= 21:
                    return "{}SX{}".format(chand.max_value, dealer_card)
                else:
                    return "{}X{}".format(chand.max_value, dealer_card)

            play_choice = None
            lu_string = make_bs_matchup(chand)
            if bs_db[lu_string] and bs_db[lu_string]:
                if bs_db[lu_string][0] in play_options:
                    play_choice = play_options[bs_db[lu_string][0]]
                elif len(bs_db[lu_string]) == 2 and bs_db[lu_string][1] in play_options:
                    play_choice = play_options[bs_db[lu_string][1]]
                else:
                    print("Random Pick")
                    play_choice = play_options[random.choice(list(play_options.keys()))]
            play_choice(chand)
            if play_choice == self.split:
                break

    def auto_play_hand_top(self, chand):
        while not chand.is_stand:
            if chand.bust:
                self.bust(chand)
                break
            if not chand.bust and not chand.blackjack:
                choice = self.game.get_top_choice(chand, delay=self.play_type_delay)
                play_options = self.play_options(chand)
                if not choice or choice not in play_options:
                    play_choice = play_options[random.choice(list(play_options.keys()))]
                else:
                    play_choice = play_options[choice]
                play_choice(chand)
                if play_choice == self.split:
                    break
            elif chand.blackjack:
                self.stand(chand)

            else:
                print("NO ACTION {}".format(chand))
                self.stand(chand)

    def clear_hands(self):
        for h in self.hands:
            self.game.deck.return_cards(h.cards)
        self.hands = []
        self.has_insurance = False

    def lost_hand(self, money_lost, hand):
        if self.game.verbose:
            print("LOST HAND {} to {}".format(repr(hand), repr(self.game.current_dealer_hand)))
            self.hand_result(hand)
        self.hands_lost += 1
        self.hands_played += 1
        self.money_lost += money_lost
        self.game.update_matchups(hand, -1, money_lost)
        if len(self.recent_record) >= game.RECENT_HANDS_LEN:
            self.recent_record.pop(0)
        self.recent_record.append(-money_lost)
        # print(hand.actions_taken)

    def won_hand(self, money_won, hand):
        if self.game.verbose:
            print("WON HAND {} to {}".format(repr(hand), repr(self.game.current_dealer_hand)))
            self.hand_result(hand)
        self.hands_won += 1
        self.hands_played += 1
        self.money_won += money_won
        self.money += money_won
        self.game.update_matchups(hand, 1, money_won)
        if len(self.recent_record) >= game.RECENT_HANDS_LEN:
            self.recent_record.pop(0)
        self.recent_record.append(money_won)
        # print(hand.actions_taken)

    def push_hand(self, money_push, hand):
        if self.game.verbose:
            print("PUSH HAND {} to {}".format(repr(hand), repr(self.game.current_dealer_hand)))
            self.hand_result(hand)
        self.hands_played += 1
        self.hands_push += 1
        self.money += money_push
        self.game.update_matchups(hand, 0, money_push)
        if len(self.recent_record) >= game.RECENT_HANDS_LEN:
            self.recent_record.pop(0)
        self.recent_record.append(0)
        # print(hand.actions_taken)

    def hand_result(self, hand):
        for action in hand.actions_taken:
            if action[0].upper() in ["PUSH","BUST"]: continue
            if action[0].upper() == "LOST_TO_BLACKJACK":
                print("      LOST TO BLACKJACK")
                continue
            matchup = self.game.get_matchup(action[1])
            result = "    matchup {} played {} times. won {}%\n".format(matchup.name,
                                                                     matchup.played,
                                                                     round((matchup.won / matchup.played)*100, 2))
            if action[0].upper() == matchup.top_choice[0].upper():
                result += "      played: {} wins {}%".format(
                                                                         action[0].upper(),
                                                                         round(((matchup.action_record[action[0]]["mwon"] -
                                                                                 matchup.action_record[action[0]][
                                                                                     "mlost"]) /
                                                                                max(matchup.action_record[action[0]]["played"],0.01)),
                                                                               2) * 100,
                                                                         matchup.top_choice[0].upper(),matchup.top_choice[1])
            else:
                result += "      !!played: {} wins {}% !! top action {} wins {}%".format(
                                                                         action[0].upper(),
                                                                         round(((matchup.action_record[action[0]]["mwon"] -
                                                                                 matchup.action_record[action[0]][
                                                                                     "mlost"]) /
                                                                                max(matchup.action_record[action[0]]["played"],0.01)),
                                                                               2) * 100,
                                                                         matchup.top_choice[0].upper(),matchup.top_choice[1])
            print(result)

    @property
    def moving_avg_played(self):
        return len(self.recent_record)

    @property
    def moving_avg_won(self):
        return sum([m for m in self.recent_record if m > 0])

    @property
    def moving_avg_lost(self):
        return -sum([m for m in self.recent_record if m < 0])

    @property
    def moving_avg_push(self):
        return len([m for m in self.recent_record if m == 0])

    @property
    def moving_avg(self):
        if self.moving_avg_played > 0:
            return round((self.moving_avg_won - self.moving_avg_lost) / (self.moving_avg_played-self.moving_avg_push), 4) * 100
        return 0

    def standings(self):
        print(
            "{} | Win/Loss/Push/Total {}/{}/{}|{} ({}%)  MA: {}/{}/{}|{} {}% | Win/Loss ${}/${} | Current Money ${}".format(
                self.name,
                self.hands_won,
                self.hands_lost,
                self.hands_push,
                self.hands_played,
                round(self.hands_won / (self.hands_played - self.hands_push), 4) * 100,
                self.moving_avg_won,
                self.moving_avg_lost,
                self.moving_avg_push,
                self.moving_avg_played,
                self.moving_avg,
                round(self.money_won, 2),
                round(self.money_lost, 2),
                round(self.money, 2)))

    def _player_array(self):
        return (self.game.db_id,
                self.name,
                self.hands_played,
                self.hands_won,
                self.hands_lost,
                self.hands_push,
                self.money_won,
                self.money_lost,
                self.money,
                self.play_type,
                self.moving_avg_won,
                self.moving_avg_lost,
                self.moving_avg_push,
                self.moving_avg_played
                )

    def save_player_standings(self):
        print("Saved Player")
        sql = "INSERT INTO hands(game_id, player_name, hands_played, hands_won, hands_lost, hands_push, money_won,money_lost, money, play_type, moving_avg_won, moving_avg_lost, moving_avg_push, moving_avg_played) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        db.lte_run_sql(sql, self._player_array(), db=self.game.game_database)


class game(object):
    """
    http://wizardofvegas.com/guides/blackjack-survey/
    """
    RECENT_HANDS_LEN = 100000

    def __init__(self, players=1, num_decks=1, deck_penetration=0, backjack_payout=1.2, soft_17_hit=True,
                 multi_split=False, double_after_split=True, verbose=False, play_type=4, play_type_delay=1000):
        self.deck = deck(decks=num_decks, deck_penetration=deck_penetration)
        self.db_id = None
        self.players = []
        self.dealer = None
        self.num_players = players
        self.verbose = verbose
        self.matchups = {}
        self.play_type = play_type
        self.play_type_delay = play_type_delay
        self.value_matchups = {}
        self.rules = {"soft_17_hit": soft_17_hit, "hit_until": 16, "multi_split": multi_split,
                      "blackjack_payout": backjack_payout, "double_after_split": double_after_split}

    def start_game(self, hands):
        self.load_game()
        if len(self.players) != self.num_players:
            for i, p in enumerate(range(self.num_players)):
                self.players.append(player(name="Player " + str(i), current_game=self, play_type=self.play_type,
                                           play_type_delay=self.play_type_delay))
        self.dealer = player(dealer=True, current_game=self)
        self.game_cycle(hands)

    def game_cycle(self, hands=1000):
        for i in range(hands):
            self.deal_hands()
            if not self.peek():
                self.play_hands()
            self.payout()
            self.clear_table()
            if i % 500000 == 0 and i > 10:
                self.save_matchups()
            if i > 10 and i % 10000 == 0:
                print("HAND {}".format(i))
            if i > 10 and i % game.RECENT_HANDS_LEN == 0:
                self.save_player_standings()
        for p in self.players:
            p.standings()
        self.save_matchups()

        print("Done")

    def deal_hands(self):
        for p in self.players:
            p.deal_hand()
            if self.verbose: p.show_deal()
        self.dealer.deal_hand()
        if self.verbose: self.dealer.show_deal()
        self.create_matchups()

    def create_matchups(self):
        dealer_hand = self.current_dealer_hand
        for p in self.players:
            for h in p.hands:
                matchup = hand_matchup.matchup_string(h, dealer_hand)
                if matchup in self.matchups:
                    continue
                else:
                    self.matchups[matchup] = hand_matchup(h, dealer_hand)

    def get_matchup(self, player_hand_text):
        matchup = hand_matchup.matchup_string(player_hand_text, self.current_dealer_hand)
        if matchup not in self.matchups:
            self.matchups[matchup] = hand_matchup(player_hand_text, self.current_dealer_hand)
        return self.matchups[matchup]

    def get_matchup_choice(self, hand, delay=0):
        matchup = self.get_matchup(hand)
        if matchup.played == 1:
            try:
                return self.value_matchups["{}+{}".format(matchup.player_hand_max_value, matchup.dealer_hand)]
            except:
                None
        return matchup.pick_action(delay)

    def get_top_choice(self, hand, delay=0):
        matchup = self.get_matchup(hand)
        if matchup.played < delay:
            return matchup.pick_action(delay)
        else:
            return matchup.top_choice

    def update_matchups(self, player_hand_text, won, mwon):
        for action, hand_text in player_hand_text.actions_taken:
            cmatchup = self.get_matchup(hand_text)
            cmatchup.update_action(action, won, mwon)

    def play_hands(self):
        for p in self.players:
            p.play_hands()
        self.dealer.play_hands()

    def peek(self):
        if self.dealer.has_blackjack: return True
        return False

    def payout(self):
        dealer_hand = None
        for h in self.dealer.hands:
            dealer_hand = h
            break
        for p in self.players:
            for h in p.hands:
                # print("{}:{} X {}:{}".format(repr(h),h.values, repr(dealer_hand),dealer_hand.values))
                if h.min_value > 21:
                    p.lost_hand(h.bet, h)
                    # print(1)
                elif h.blackjack and not dealer_hand.blackjack:
                    p.won_hand(h.bet + h.bet * self.rules["blackjack_payout"], h)
                    # print(2)
                elif dealer_hand.blackjack and not h.blackjack:
                    p.lost_to_blackjack(h)
                    p.lost_hand(h.bet, h)
                    # print(3)
                elif dealer_hand.bust and not h.bust:
                    p.won_hand(h.bet * 2, h)
                    # print(4)
                elif not dealer_hand.bust and h.bust:
                    p.lost_hand(h.bet, h)
                    # print(5)
                elif not h.blackjack and not dealer_hand.blackjack:
                    if h.max_value > dealer_hand.max_value:
                        p.won_hand(h.bet * 2, h)
                        # print(6)
                    elif h.max_value < dealer_hand.max_value:
                        p.lost_hand(h.bet, h)
                        # print(7)
                    else:
                        p.push(h)
                        p.push_hand(h.bet, h)
                else:
                    p.push(h)
                    p.push_hand(h.bet, h)

    def clear_table(self):
        for p in self.players:
            p.clear_hands()
            # p.standings()
            # print("")
        self.dealer.clear_hands()

    @property
    def current_dealer_hand(self):
        if self.dealer.hands != []:
            return self.dealer.hands[0]
        return None

    @property
    def hands_played(self):
        return 0

    @property
    def game_database(self):
        # Eventually the last false wil be true or false for surrender
        return db.make_project_path(
            "database/BJDB{}-{}-{}-{}-{}-{}-{}-False.sqlite".format(self.num_players, self.deck.deck_size,
                                                                    self.deck.target_deck_penetration,
                                                                    self.rules["blackjack_payout"],
                                                                    self.rules["soft_17_hit"],
                                                                    self.rules["multi_split"],
                                                                    self.rules["double_after_split"]))

    @property
    def bs_name(self):
        """
        game name lookup for basic strategy dicts
        :return:
        """
        numdecks = 4
        if self.deck.num_decks < 3:
            numdecks = self.deck.num_decks
        return "{}-{}-{}-{}".format(int(numdecks), self.rules["soft_17_hit"], self.rules["double_after_split"], "False")

    # Database stuff
    def load_game(self):
        if not os.path.isfile(self.game_database):
            db.create_database(self.game_database)
        sql = "SELECT id FROM games WHERE decks={} AND penetration={} AND players={} AND soft_17_hit={} AND hit_until={} AND multi_split={} AND blackjack_payout={} AND play_style={} AND play_style_delay={} AND doub_after_split={}".format(
            *self._game_array)
        game_id = db.lte_run_sql(sql, one=True, db=self.game_database)
        if game_id is None:
            db.lte_run_sql(
                "INSERT INTO games(decks, penetration, players, soft_17_hit, hit_until, multi_split, blackjack_payout, play_style, play_style_delay, doub_after_split) VALUES (?,?,?,?,?,?,?,?,?,?)",
                insert_list=self._game_array, one=True, db=self.game_database)
            game_id = db.lte_run_sql(sql, one=True, db=self.game_database)
        self.db_id = game_id
        self.load_player_standings()
        self.load_matchups()
        self.load_value_matchups()

    def save_game(self):
        self.save_matchups()

    def load_value_matchups(self):
        print("Loading Value Matchups")
        sql = "SELECT value_name, count(value_name), (SUM(stand_mwon)-SUM(stand_mlost))/SUM(stand_played)*100, (SUM(hit_mwon)-SUM(hit_mlost))/SUM(hit_played)*100, (SUM(doub_mwon)-SUM(doub_mlost))/SUM(doub_played)*100, (SUM(split_mwon)-SUM(split_mlost))/SUM(split_played)*100 FROM matchups GROUP BY value_name;"
        v_matchups = db.lte_run_sql(sql, db=self.game_database)
        action_lookup = {0: None, 2: "stand", 3: "hit", 4: "doub", 5: "split"}
        for m in v_matchups:
            try:
                top_return = m.index(max(value for value in m[2:] if value is not None))
            except:
                top_return = 0
            self.value_matchups[m[0]] = action_lookup[top_return]

    def load_matchups(self):
        print("Loading Matchups")
        sql = "SELECT id, " \
              "matchup_name," \
              "player_hand, " \
              "dealer_card, " \
              "stand_played," \
              "stand_won," \
              "stand_lost," \
              "stand_mwon," \
              "stand_mlost," \
              "hit_played," \
              "hit_won," \
              "hit_lost," \
              "hit_mwon," \
              "hit_mlost," \
              "doub_played," \
              "doub_won," \
              "doub_lost," \
              "doub_mwon," \
              "doub_mlost," \
              "split_played," \
              "split_won," \
              "split_lost," \
              "split_mwon," \
              "split_mlost," \
              "push_played, " \
              "lost_to_blackjack_played, " \
              "lost_to_blackjack_mlost, " \
              "bust_played, " \
              "bust_mlost " \
              "FROM matchups WHERE game_id={}".format(self.db_id)
        matchups = db.lte_run_sql(sql, db=self.game_database)
        if matchups:
            for m in matchups:
                self.build_matchup_from_array(m)
        print("{} Matchups Loaded".format(len(self.matchups)))

    def build_matchup_from_array(self, m_array):
        if len(m_array) != 29:
            print(len(m_array), "LEN ERROR")
        else:
            new_matchup = hand_matchup(m_array[2], m_array[3])
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
            self.matchups[new_matchup.name] = new_matchup

    def save_matchups(self):
        print("Saving Matchups")
        matchup_lists = []
        for m in self.matchups:
            matchup_lists.append((self.db_id,) + self.matchups[m]._matchup_array)
        sql = "DELETE FROM matchups WHERE game_id={}".format(self.db_id)
        db.lte_run_sql(sql, db=self.game_database)
        sql2 = 'INSERT INTO matchups(game_id, ' \
               'matchup_name, ' \
               'player_hand, ' \
               'dealer_card, ' \
               'player_max_value, ' \
               'player_min_value,' \
               'stand_played,' \
               'stand_won,' \
               'stand_lost,' \
               'stand_mwon,' \
               'stand_mlost,' \
               'hit_played,' \
               'hit_won,' \
               'hit_lost,' \
               'hit_mwon,' \
               'hit_mlost,' \
               'doub_played,' \
               'doub_won,' \
               'doub_lost,' \
               'doub_mwon,' \
               'doub_mlost,' \
               'split_played,' \
               'split_won,' \
               'split_lost,' \
               'split_mwon,' \
               'split_mlost,' \
               'push_played, ' \
               'lost_to_blackjack_played, ' \
               'lost_to_blackjack_mlost, ' \
               'bust_played, ' \
               'bust_mlost,' \
               'stand_prob,' \
               'hit_prob,' \
               'doub_prob,' \
               'split_prob,' \
               'top_action,' \
               'top_action_prob, ' \
               'value_name) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        db.lte_batch_update(sql2, matchup_lists, db=self.game_database)
        print("{} Matchups Saved".format(len(matchup_lists)))

    def save_player_standings(self):
        for p in self.players:
            p.standings()
            p.save_player_standings()

    def load_player_standings(self):
        sql = "select player_name, play_type, money, hands_played, hands_won, hands_lost, hands_push, money_won, money_lost from hands where hands_played = (select max(hands_played) from hands as f where game_id={} and f.player_name = hands.player_name);".format(
            self.db_id)
        players = db.lte_run_sql(sql, db=self.game_database)
        for p in players:
            self.build_players(p)

    def build_players(self, p):
        hands_dict = {"money": p[2], "hands_played": p[3], "hands_won": p[4], "hands_lost": p[5], "hands_push": p[6],
                      "money_won": p[7], "money_lost": p[8]}
        new_player = player(name=p[0], play_type=p[1], current_game=self, hands=hands_dict,
                            play_type_delay=self.play_type_delay)
        self.players.append(new_player)
        new_player.standings()

    @property
    def _game_array(self):
        """
        :return: Array used to save and load the game
        """
        return (int(self.deck.deck_size / 52), self.deck.target_deck_penetration, self.num_players,
                int(self.rules["soft_17_hit"]), self.rules["hit_until"], int(self.rules["multi_split"]),
                self.rules["blackjack_payout"], self.play_type, self.play_type_delay,
                int(self.rules["double_after_split"]))


class hand_matchup(object):
    def __init__(self, player_hand, dealer_hand):
        self.name = hand_matchup.matchup_string(player_hand, dealer_hand)
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
    def values(hand):
        values = []
        for c in hand:
            if values == []:
                values = hand_matchup.CARD_VALUES[c]
            else:
                values = [sum([x, y]) for x in hand_matchup.CARD_VALUES[c] for y in values]
        return values

    @property
    def player_hand(self):
        return self.name.split("+")[0]

    @property
    def dealer_hand(self):
        return self.name.split("+")[1]

    @property
    def player_hand_max_value(self):
        value_list = hand_matchup.values(self.player_hand)
        max_val = max(value_list)
        min_val = min(value_list)
        if max_val > 21 and min_val < 21 and len(value_list) > 1:
            max_val = max(v for v in value_list if v <= 21)
        return max_val

    @property
    def player_hand_min_value(self):
        return min(hand_matchup.values(self.player_hand))

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

    @property
    def probabilities(self):
        if self.can_split:
            probs = {"hit": self.hit_prob, "stand": self.stand_prob, "doub": self.doub_prob, "split": self.split_prob}
        else:
            probs = {"hit": self.hit_prob, "stand": self.stand_prob, "doub": self.doub_prob}
        for p in probs:
            if probs[p] == "UNKN":
                probs[p] = 0
            # if probs[p] < 0:
            #     probs[p] = 0
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

    def pick_action(self, delay=0):
        MIN_RAND = delay
        choice = None
        if self.played > MIN_RAND:
            choice = weighted_choice(self.probabilities)
            if choice and self.action_record[choice]["played"] > MIN_RAND / 3:
                # if (choice != self.top_choice[0]):
                #     print("PLAY: {} @ {}%----{}".format(choice, round(((self.action_record[choice]["mwon"] -
                #                                                         self.action_record[choice]["mlost"]) /
                #                                                        self.action_record[choice]["played"]), 2) * 100,
                #                                         self.__repr__()))
                # else: print("@@Best Bet: {} {}".format(*self.top_choice))
                return choice
        choice = random.choice(list(self.probabilities.keys()))
        # print("{} RANDOM".format(choice))
        return choice

    @property
    def top_choice(self):
        top_action = max(self.probabilities, key=self.probabilities.get)
        return top_action, self.probabilities[top_action]

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
                "{}+{}".format(self.player_hand_max_value, self.dealer_hand))

    @staticmethod
    def matchup_string(player_hand, dealer_hand):
        if type(player_hand) == hand:
            return hand_matchup.sort_string(player_hand.card_names()) + "+" + repr(dealer_hand)[0]
        else:
            player_hand = player_hand.translate({ord(i): None for i in "♣♠♥♦"})
            if type(dealer_hand) == hand:
                return hand_matchup.sort_string(player_hand) + "+" + repr(dealer_hand)[0]
            else:
                return hand_matchup.sort_string(player_hand) + "+" + dealer_hand[0]

    @staticmethod
    def sort_string(cards):
        sorted_cards = ''.join(sorted(cards[:2]))
        return sorted_cards + cards[2:]


def weighted_choice(choices):
    sub_choices = {(c, w) for c, w in choices.items() if w>=0}
    total = sum(w for c, w in sub_choices)
    r = random.uniform(0, total)
    if total == 0: return None
    upto = 0
    for c, w in sub_choices:
        wa = w
        if upto + wa > r:
            return c
        upto += wa
    assert False, "Shouldn't get here"


def main():
    new_game = game(play_type_delay=0, deck_penetration=99, num_decks=1, play_type=player.WEIGHTED_PLAY,
                    soft_17_hit=False, backjack_payout=1.5, multi_split=True, double_after_split=True)
    new_game.start_game(100000000)


main()

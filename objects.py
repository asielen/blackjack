import random
import system as syt

class deck(object):
    full_deck = [['3', '♦', [3]], ['J', '♦', [10]], ['8', '♦', [8]], ['9', '♦', [9]], ['5', '♦', [5]], ['2', '♦', [2]], ['A', '♦', [1, 11]], ['K', '♦', [10]], ['4', '♦', [4]], ['7', '♦', [7]], ['T', '♦', [10]], ['Q', '♦', [10]], ['6', '♦', [6]], ['3', '♠', [3]], ['J', '♠', [10]], ['8', '♠', [8]], ['9', '♠', [9]], ['5', '♠', [5]], ['2', '♠', [2]], ['A', '♠', [1, 11]], ['K', '♠', [10]], ['4', '♠', [4]], ['7', '♠', [7]], ['T', '♠', [10]], ['Q', '♠', [10]], ['6', '♠', [6]], ['3', '♥', [3]], ['J', '♥', [10]], ['8', '♥', [8]], ['9', '♥', [9]], ['5', '♥', [5]], ['2', '♥', [2]], ['A', '♥', [1, 11]], ['K', '♥', [10]], ['4', '♥', [4]], ['7', '♥', [7]], ['T', '♥', [10]], ['Q', '♥', [10]], ['6', '♥', [6]], ['3', '♣', [3]], ['J', '♣', [10]], ['8', '♣', [8]], ['9', '♣', [9]], ['5', '♣', [5]], ['2', '♣', [2]], ['A', '♣', [1, 11]], ['K', '♣', [10]], ['4', '♣', [4]], ['7', '♣', [7]], ['T', '♣', [10]], ['Q', '♣', [10]], ['6', '♣', [6]]]
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

    def deal(self):
        return [self.draw(), self.draw()]

    def draw(self):
        if self.check_card_availability():
            current_card = self.available_cards.pop()
            self.in_play_cards.append(current_card)
            return current_card
        else:
            print("ERROR: All cards in play")
            return None

    def close_play_field(self):
        for c in range(len(self.in_play_cards)):
            self.used_cards.append(self.in_play_cards.pop())

    def return_cards_from_hand(self, cards):
        for c in cards:
            if c in self.in_play_cards:
                self.in_play_cards.remove(c)
                self.used_cards.append(c)
            else:
                print("ERROR = {} was not in play?".format(c))


    @property
    def penetraion(self):
        return ((len(self.in_play_cards)+len(self.used_cards))/(self.deck_size))*100

    def check_penetration(self):
        print("{}% through the deck (of {}%)".format(round(self.penetraion,2), self.target_deck_penetration))
        if self.penetraion >= self.target_deck_penetration:
            self.shuffle()

    def check_card_availability(self):
        if len(self.available_cards) == 0 and len(self.used_cards) ==  0:
            return False
        elif len(self.available_cards) == 0 and len(self.used_cards) > 0:
            self.shuffle()
            return True
        else: return True

    def shuffle(self):
        print("Shuffling Deck")
        for c in range(len(self.used_cards)):
            self.available_cards.append(self.used_cards.pop())
        random.shuffle(self.available_cards)



class card(object):
    def __init__(self, card_list):
        """
        :param card_list: in format ['value name','suit name','card value']
        :return:
        """
        self.suit = card_list[1]
        self.name = card_list[0]
        self.value = card_list[2]


    def __repr__(self):
        return "{}{}".format(self.name,self.suit)

class hand(object):
    def __init__(self, cards, player):
        self.cards = cards
        self.player = player
        self.standed = False
        self.current_matchups = []
        self.actions_taken = []

    @property
    def value(self):
        values = []
        for c in self.cards:
            if values == []:
                values = c.value
            else:
                values = [sum([x,y]) for x in c.value for y in values]
        return values

    @property
    def max_value(self):
        max_val = max(self.value)
        if max_val > 21 and len(self.value) > 1:
            max_val = max(v for v in self.value if v <= 21)
        return max_val

    @property
    def min_value(self):
        return min(self.value)

    @property
    def black_jack(self):
        if len(self.cards) == 2:
            if self.max_value == 21:
                return True
        else:
            return False

    @property
    def soft(self):
        """

        :return: True if one of the cards is an Ace
        """
        if len(self.value) > 1:
            return True
        else:
            return False

    @property
    def has_ace(self):
        """
        For insurance
        :return: True if first card is an ACE
        """
        if self.cards[0].name == "A": return True
        else: return False

    @property
    def has_double_ace(self):
        if self.cards[0].name == "A" and self.cards[0].name == "A": return True
        else: return False

    @property
    def bust(self):
        if self.min_value > 21:
            return True
        else: return False

    def __repr__(self):
        name = ""
        for c in self.cards:
            name += "{}".format(str(c))
        return name

    def __str__(self):
        name = ""
        for c in self.cards:
            name += "{} ".format(str(c))
        return name

    def card_names(self):
        name = ""
        for c in self.cards:
            name += "{}".format(c.name)
        return name

    def show_player_hand(self):
        return self.__repr__()

    def show_player_value(self):
        if self.black_jack: return "Blackjack"
        return self.value

    def show_dealer_hand(self):
        name = ""
        if self.black_jack: return self.show_player_hand()
        for c in self.cards:
            name += "{} ".format(str(c))
            break
        return name + "##"

    def show_dealer_value(self):
        value = ""
        if self.black_jack: return "Blackjack"
        for c in self.cards:
            value = c.value
            break
        return value


    def draw(self):
        assert(deck is not None)
        self.cards.append(self.player.draw())
        return 0

    def stand(self):
        self.standed = True
        return 1

    @property
    def can_split(self):
        if len(self.cards)==2 and self.cards[0].name == self.cards[1].name:
            return True
        else: return False

    def split(self):
        if self.can_split:
            new_hands = [hand([self.cards[0], self.player.draw()],self.player),hand([self.cards[1], self.player.draw()],self.player)]

            return new_hands

class player(object):

    MANUAL_PLAY = 1
    RULES_PLAY = 2
    RANDOM_PLAY = 3
    WEIGHTED_PLAY = 4

    def __init__(self, dealer=False, name="", current_game=None, play_type=4):
        self.hands = [] # Plural because of split possibilities
        self.dealer = dealer
        self.default_bet = 10
        self.current_bet = 0
        self.money = 0
        self.hands_played = 0
        self.hands_won = 0
        self.hands_lost = 0
        self.money_won = 0
        self.money_lost = 0
        self.has_insurance = False

        if self.dealer: self.play_type = player.RULES_PLAY
        else: self.play_type=play_type

        if dealer: self.name = "Dealer"
        else: self.name = name

        self.game = current_game

    def deal_hand(self):
        self.hands.append(hand(self.game.deck.deal(), player=self))

    def show_deal(self):
        hands = "{} playing: ".format(self.name)
        for i, h in enumerate(self.hands):
            if self.dealer:
                hands += "{}: {} | ".format(h.show_dealer_hand(), h.show_dealer_value())
            else:
                hands += "{}: {} | ".format(h.show_player_hand(), h.show_player_value())
        return print(hands)

    def show_hand(self, hand, action):
        if self.game.verbose: print("  {} | Cards {} | Value {}".format(action, hand.show_player_hand(), hand.show_player_value()))

    @property
    def has_ace(self):
        if self.hands[0].has_ace:
            return True
        else: return False

    @property
    def all_standed(self):
        if len(self.hands) == 0: return False
        for h in self.hands:
            if h.standed is False:
                return False
        return True

    @property
    def has_blackjack(self):
        if len(self.hands) == 0: return False
        for h in self.hands:
            if h.black_jack is True:
                return True
        return False

    def draw(self):
        return self.game.deck.draw()

    def play_options(self, hand):
        if hand is None: return
        options = {}
        options["stand"]=self.stand
        if hand.min_value < 21:
            options["hit"]=self.hit
            if self.dealer is False:
                options["doub"]=self.doubledown
        if hand.can_split and self.dealer is False:
            options["split"]=self.split
        # if self.dealer is False and self.game.dealer.has_ace and self.has_insurance is False:
        #     options.append(("Buy Insurance", self.insurance))
        return options

    def play_hands(self):
        while self.all_standed is False:
            for h in self.hands:
                if self.dealer:
                    print("Dealer playing hand {} {}".format(h, h.value))
                else:
                    print("{} playing hand {} {}".format(self.name, h, h.value))
                if h.standed: continue
                if self.play_type == player.MANUAL_PLAY:
                    self.manual_play_hand(h)
                if self.play_type == player.RULES_PLAY:
                    self.auto_play_hand_rules(h)
                if self.play_type == player.RANDOM_PLAY:
                    self.auto_play_hand_random(h)
                if self.play_type == player.WEIGHTED_PLAY:
                    self.auto_play_hand_weighted(h)
        self.hands_played += len(self.hands)

    def bet(self):
        if self.game.verbose: print("Betting {}".format(self.default_bet))
        self.money -= self.default_bet
        self.current_bet += self.default_bet

    def hit(self, hand):
        hand.actions_taken.append(["hit",repr(hand)])
        hand.draw()
        if self.game.verbose: self.show_hand(hand, "Hit")

    def stand(self, hand):
        hand.actions_taken.append(["stand",repr(hand)])
        hand.stand()
        if self.game.verbose: print("  Stand")

    def split(self, hand):
        self.bet()
        # hand.actions_taken.append(["split",repr(hand)])
        chand = hand
        self.hands.remove(hand)
        shands = chand.split()
        shands[0].actions_taken.append(["split",repr(chand)])
        shands[1].actions_taken.append(["split",repr(chand)])
        self.hands.extend(shands)
        if self.game.verbose: print("  Split: {} | {}".format(shands[0],shands[1]))


    def doubledown(self, hand):
        self.bet()
        hand.actions_taken.append(["doub",repr(hand)])
        hand.draw()
        hand.stand()
        self.show_hand(hand, "DDn")
        hand.actions_taken.append(["stand",repr(hand)])

    def insurance(self,hand):
        if self.game.verbose: print("  Bought Insurance")
        self.has_insurance = True
        self.bet()

    def surrender(self):
        pass


    def manual_play_hand(self, chand):
        pass

    def auto_play_hand_random(self, chand):
        while not chand.standed:
            if chand.bust:
                self.bust(chand)
                break
            if not chand.bust and not chand.black_jack:
                play_options = self.play_options(chand)
                play_choice = play_options[random.choice(play_options.keys())]
                play_choice(chand)
                if play_choice == self.split:
                    break
                # else:
                    # self.show_hand(chand, action)
            else:
                self.stand(chand)

    def auto_play_hand_rules(self, chand):
        while not chand.standed:
            if chand.bust:
                self.bust(chand)
            if not chand.bust and not chand.black_jack:
                if chand.has_double_ace and chand.min_value <= 16:
                    self.hit(chand)
                elif chand.max_value <= 16:
                    self.hit(chand)
                elif chand.max_value == 17 and chand.soft:
                    if self.game.rules["soft_17_hit"]:
                        self.stand(chand)
                    else:
                        self.hit(chand)
                else:
                    self.stand(chand)

    def bust(self, hand):
        hand.standed = True
        print("Bust")
        hand.actions_taken.append(["bust",repr(hand)])
        if self.game.verbose: print("  Busted")

    @property
    def all_hands_bust(self):
        if len(self.hands) == 0: return False
        for h in self.hands:
            if h.bust is False:
                return False
        return True

    def auto_play_hand_weighted(self, chand):
        while not chand.standed:
            if chand.bust:
                self.bust(chand)
                break
            if not chand.bust and not chand.black_jack:
                choice = self.game.get_matchup_choice(chand)
                play_options = self.play_options(chand)
                if not choice or choice not in play_options:
                    play_choice = play_options[random.choice(list(play_options.keys()))]
                else:
                    play_choice = play_options[choice]
                play_choice(chand)
                if play_choice == self.split:
                    break
                # else:
                    # self.show_hand(chand, action)
            else:
                self.stand(chand)

    def clear_hands(self):
        for h in self.hands:
            self.game.deck.return_cards_from_hand(h.cards)
        self.hands = []
        self.has_insurance = False

    def lost_hand(self, money_lost,hand):
        if self.game.verbose: print("\nPlayer: {} lost the hand".format(self.name))
        self.hands_lost += 1
        self.money_lost += money_lost
        self.game.update_matchups(hand,-1,money_lost)
        print(hand.actions_taken)

    def won_hand(self, money_won,hand):
        if self.game.verbose: print("\nPlayer: {} won the hand".format(self.name))
        self.hands_won += 1
        self.money_won += money_won
        self.money += money_won
        self.game.update_matchups(hand,1,money_won)
        print(hand.actions_taken)

    def standings(self):
        print("{} | Win/Loss {}/{} ({}%) | Win/Loss ${}/${} ({}%) | Current Money ${}".format(self.name,self.hands_won,self.hands_lost,round(self.hands_won/(self.hands_won+self.hands_lost),4)*100,round(self.money_won,2),round(self.money_lost,2),round(self.money_won/(self.money_won+self.money_lost),4)*100, self.money))

class game(object):
    def __init__(self, players=1, num_decks=1, deck_penetration=50, backjack_payout=1.2, soft_17_hit=False, multi_split=False, allow_insurance=False, allow_surrender=False, verbose=False):
        self.deck = deck(decks=num_decks, deck_penetration=deck_penetration)
        self.players = []
        self.dealer = None
        self.num_players = players
        self.verbose = verbose
        self.matchups = {}
        self.rules = {"soft_17_hit":soft_17_hit,"hit_until":16,"multi_split":multi_split,"allow_insurance":allow_insurance,"blackjack_payout":backjack_payout}

    def start_game(self):
        for i,p in enumerate(range(self.num_players)):
            self.players.append(player(name="Player "+str(i), current_game=self))
        self.dealer = player(dealer=True, current_game=self)
        self.game_cycle()

    def game_cycle(self):
        for i in range(100000):
            self.deal_hands()
            if not self.peek():
                self.play_hands()
            self.payout()
            self.clear_table()
        for m in self.matchups:
            if self.matchups[m].played >= 10:
                print(self.matchups[m])
        print("Done")


    def deal_hands(self):
        for p in self.players:
            p.bet()
            p.deal_hand()
            p.show_deal()
        self.dealer.deal_hand()
        self.dealer.show_deal()
        self.create_matchups()

    def create_matchups(self):
        dealer_hand = self.current_dealer_hand
        for p in self.players:
            for h in p.hands:
                matchup = hand_matchup.matchup_string(h,dealer_hand)
                if matchup in self.matchups:
                    continue
                else:
                    self.matchups[matchup] = hand_matchup(h,dealer_hand)

    def get_matchup(self, player_hand_text):
        matchup = hand_matchup.matchup_string(player_hand_text, self.current_dealer_hand)
        if matchup not in self.matchups:
            self.matchups[matchup] = hand_matchup(player_hand_text, self.current_dealer_hand)
        return self.matchups[matchup]

    def get_matchup_choice(self, hand):
        matchup = self.get_matchup(hand)
        return matchup.pick_action()

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
                if h.min_value > 21:
                    p.lost_hand(p.current_bet / len(p.hands),h)
                    # print(1)
                elif h.black_jack and not dealer_hand.black_jack:
                    p.won_hand((p.current_bet / len(p.hands))*2*self.rules["blackjack_payout"],h)
                    # print(2)
                elif dealer_hand.black_jack and not h.black_jack:
                    p.lost_hand(p.current_bet / len(p.hands),h)
                    # print(3)
                elif dealer_hand.bust and not h.bust:
                    p.won_hand((p.current_bet / len(p.hands))*2,h)
                    # print(4)
                elif not dealer_hand.bust and h.bust:
                    p.lost_hand(p.current_bet / len(p.hands),h)
                    # print(5)
                elif not h.black_jack and not dealer_hand.black_jack:
                    if h.max_value > dealer_hand.max_value:
                        p.won_hand((p.current_bet / len(p.hands))*2,h)
                        # print(6)
                    elif h.max_value < dealer_hand.max_value:
                        p.lost_hand(p.current_bet / len(p.hands),h)
                        # print(7)
                else:
                    # print(8)
                    pass
            p.current_bet = 0


    def clear_table(self):
        for p in self.players:
            p.clear_hands()
            p.standings()
            print("")
        self.dealer.clear_hands()

    @property
    def current_dealer_hand(self):
        if self.dealer.hands != []:
            return self.dealer.hands[0]
        return None


class hand_matchup(object):
    def __init__(self, player_hand, dealer_hand):
        self.name = hand_matchup.matchup_string(player_hand,dealer_hand)
        self.action_record = {"hit":{"played":0,"won":0,"lost":0,"mwon":0,"mlost":0},"stand":{"played":0,"won":0,"lost":0,"mwon":0,"mlost":0},"split":{"played":0,"won":0,"lost":0,"mwon":0,"mlost":0},"doub":{"played":0,"won":0,"lost":0,"mwon":0,"mlost":0}}

    @property
    def played(self):
        return self.action_record["hit"]["played"]+self.action_record["stand"]["played"]+self.action_record["split"]["played"]+self.action_record["doub"]["played"]

    def update_action(self, action, won, mwon):
        if action == "bust":
            action = "stand"
        self.action_record[action]["played"] += 1
        if won > 0:
            self.action_record[action]["won"] += won
            self.action_record[action]["mwon"] += mwon
        elif won > 0:
            self.action_record[action]["lost"] -= won #minus negative = addition
            self.action_record[action]["mlost"] += mwon
        # print(self.__repr__())

    @property
    def can_split(self):
        self_string = self.name
        if len(self_string)==4:
            if self_string[0] == self_string[1]:
                return True
        return False

    @property
    def hit_prob(self):
        if self.action_record["hit"]["played"] > 0:
            return round(self.action_record["hit"]["won"]/self.action_record["hit"]["played"]*100,2)
        else:
            return "Unknown"

    @property
    def split_prob(self):
        if self.action_record["split"]["played"] > 0:
            return round(self.action_record["split"]["won"]/self.action_record["split"]["played"]*100,2)
        else:
            if self.can_split:
                return "Unknown"
            return None

    @property
    def stand_prob(self):
        if self.action_record["stand"]["played"] > 0:
            return round(self.action_record["stand"]["won"]/self.action_record["stand"]["played"]*100,2)
        else:
           return "Unknown"

    @property
    def doub_prob(self):
        if self.action_record["doub"]["played"] > 0:
            return round(self.action_record["doub"]["won"]/self.action_record["doub"]["played"]*100,2)
        else:
           return "Unknown"

    @property
    def probabilities(self):
        if self.can_split:
            probs = {"hit":self.hit_prob,"stand":self.stand_prob,"doub":self.stand_prob,"split":self.stand_prob}
        else:
            probs = {"hit":self.hit_prob,"stand":self.stand_prob,"doub":self.stand_prob}
        for p in probs:
            if probs[p] == "Unknown":
                probs[p] = 50
        return probs

    def pick_action(self):
        choice = None
        if self.played > 5:
            choice = weighted_choice(self.probabilities)
            if choice and self.action_record[choice]["played"] > 1:
                print("{} wins {}% of the time".format(choice,self.action_record[choice]["won"]/self.action_record[choice]["played"]*100))
                return choice
        choice = random.choice(list(self.probabilities.keys()))
        print("{} RANDOM".format(choice))
        return choice

    def __repr__(self):
        if self.can_split:
            return "{} = PLAYED: {} | HIT: {}% | DOU: {}% | STD: {}% | SPT: {}%".format(self.name, self.played, self.hit_prob, self.doub_prob, self.stand_prob, self.split_prob)
        else:
            return "{} = PLAYED: {} | HIT: {}% | DOU: {}% | STD: {}%".format(self.name,self.played,self.hit_prob,self.doub_prob,self.stand_prob)


    def __str__(self):
        return self.__repr__()

    @staticmethod
    def matchup_string(player_hand, dealer_hand):
        if type(player_hand) == hand:
            return player_hand.card_names()+"+"+repr(dealer_hand)[0]
        else:
            player_hand = player_hand.translate({ord(i):None for i in "♣♠♥♦"})
            return player_hand+"+"+repr(dealer_hand)[0]

def weighted_choice(choices):
    total = sum(w for c, w in choices.items())
    r = random.uniform(0, total)
    if total == 0: return None
    upto = 0
    for c, w in choices.items():
        if upto + w > r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def main():
    new_game = game()
    new_game.start_game()

main()










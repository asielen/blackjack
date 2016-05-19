import random
import database as db

class deck(object):
    """
        Object that keeps track of the total deck, the cards in play and the used cards
    """
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

    @property
    def penetraion(self):
        """
        :return: Percent of the deck that is currently being used
        """
        return round(((len(self.in_play_cards)+len(self.used_cards))/(self.deck_size))*100,2)

    def __repr__(self):
        return "Decks {} | Cards {} | Status: {}/{}/{} {}%".format(self.deck_size/52,self.deck_size,len(self.available_cards),len(self.in_play_cards),len(self.used_cards),self.penetraion)

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
        elif (len(self.available_cards) == 0 or self.penetraion >= self.target_deck_penetration) and len(self.used_cards) > 0:
            self.shuffle()
            return True
        else:
            return True

    def shuffle(self):
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
        self.values = card_list[2]

    def __repr__(self):
        return "{}{}".format(self.name,self.suit)

class hand(object):
    """
        Current hand of play
    """
    def __init__(self, cards, player, bet=0):
        self.cards = cards
        self.player = player
        self.bet = bet
        self.winlose = 0 # 1 for won, 0 for lost
        self.is_stand = False
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
                values = [sum([x,y]) for x in c.values for y in values]
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
        else: return False

    @property
    def soft(self):
        """
        :return: True if one of the cards is an Ace (and therefore has multiple possible values
        """
        if len(self.values) > 1: return True
        else: return False

    @property
    def showing_ace(self):
        """
        For insurance
        :return: True if first card is an ACE - For insurance purposes
        """
        if self.cards[0].name == "A": return True
        else: return False

    @property
    def can_split(self):
        """
        :return: True if the hand can be split (2 of the same card, ignoreing suits)
        """
        if len(self.cards)==2 and self.cards[0].name == self.cards[1].name:
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
        assert(self.player.game.deck is not None)
        self.cards.append(self.player.draw())
        return 0

    def stand(self):
        self.is_stand = True
        return 1

    def split(self):
        if self.can_split:
            new_hands = [hand([self.cards[0], self.player.draw()],self.player,self.bet),hand([self.cards[1], self.player.draw()],self.player,self.bet)]
            return new_hands

class player(object):

    MANUAL_PLAY = 1
    RULES_PLAY = 2
    RANDOM_PLAY = 3
    WEIGHTED_PLAY = 4

    def __init__(self, dealer=False, name="", current_game=None, play_type=4):
        self.hands = [] # Plural because of split possibilities
        self.db_id = None
        self.dealer = dealer # True if player is dealer
        self.default_bet = 1
        self.money = 0
        self.hands_played = 0
        self.hands_won = 0
        self.hands_lost = 0
        self.hands_push = 0
        self.money_won = 0
        self.money_lost = 0

        if self.dealer: self.play_type = player.RULES_PLAY
        else: self.play_type=play_type

        if dealer: self.name = "Dealer"
        else: self.name = name

        self.game = current_game

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
                hands += "{}: {} ${} | ".format(h.show_player_hand(), h.show_player_value(),h.bet)
        return print(hands)

    def show_hand(self, hand, action):
        if self.game.verbose: print("  {} | Cards {} | Value {} | Bet ${}".format(action, hand.show_player_hand(), hand.show_player_value(),hand.bet))

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


    def bet(self, hand):
        if self.game.verbose: print("Betting {}".format(self.default_bet))
        self.money -= self.default_bet
        hand.bet += self.default_bet

    def hit(self, hand):
        hand.actions_taken.append(["hit",repr(hand)])
        hand.draw()
        if self.game.verbose: self.show_hand(hand, "Hit")

    def stand(self, hand):
        hand.actions_taken.append(["stand",repr(hand)])
        hand.stand()
        if self.game.verbose: print("  Stand")

    def split(self, hand):
        chand = hand
        self.hands.remove(hand)
        shands = chand.split()
        self.money -= self.default_bet
        shands[0].actions_taken.append(["split",repr(chand)])
        shands[1].actions_taken.append(["split",repr(chand)])

        self.hands.extend(shands)
        if self.game.verbose: print("  Split: {} | {}".format(shands[0],shands[1]))

    def doubledown(self, hand):
        hand.actions_taken.append(["doub",repr(hand)])
        self.bet(hand)
        hand.draw()
        if hand.bust:
            self.bust(hand)
        else:
            self.stand(hand)
        self.show_hand(hand, "DDn")

    def bust(self, hand):
        hand.stand()
        hand.actions_taken.append(["bust",repr(hand)])
        if self.game.verbose: print("  Busted")

    def lost_to_blackjack(self, hand):
        hand.stand()
        hand.actions_taken.append(["lost_to_blackjack",repr(hand)])

    def push(self, hand):
        hand.stand()
        hand.actions_taken.append(["push",repr(hand)])

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
            if not chand.bust and not chand.blackjack:
                if chand.max_value == 17 and chand.min_value < 17 and chand.soft:
                    #If it is a hard 17 don't follow these rules
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
                choice = self.game.get_matchup_choice(chand)
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
        if self.game.verbose: print("\n{} lost the hand".format(self.name))
        self.hands_lost += 1
        self.hands_played += 1
        self.money_lost += money_lost
        self.game.update_matchups(hand,-1,money_lost)

        # print(hand.actions_taken)

    def won_hand(self, money_won, hand):
        if self.game.verbose: print("\n{} won the hand".format(self.name))
        self.hands_won += 1
        self.hands_played += 1
        self.money_won += money_won
        self.money += money_won
        self.game.update_matchups(hand,1,money_won)
        # print(hand.actions_taken)

    def push_hand(self, money_push, hand):
        if self.game.verbose: print("\nP{} push the hand".format(self.name))
        self.hands_played += 1
        self.hands_push += 1
        self.money += money_push
        self.game.update_matchups(hand,0,money_push)
        # print(hand.actions_taken)


    def standings(self):
        print("{} | Win/Loss/Push/Total {}/{}/{}/{} ({}%) | Win/Loss ${}/${} | Current Money ${}".format(self.name,self.hands_won,self.hands_lost,self.hands_push,self.hands_played,round(self.hands_won/(self.hands_played),4)*100,round(self.money_won,2),round(self.money_lost,2), self.money))

    def _player_array(self):
        return (self.game.db_id,
                self.name,
                self.hands_played,
                self.hands_won,
                self.hands_lost,
                self.money_won,
                self.money_lost,
                self.money)

class game(object):
    def __init__(self, players=1, num_decks=1, deck_penetration=0, backjack_payout=1.2, soft_17_hit=False, multi_split=False, verbose=False):
        self.deck = deck(decks=num_decks, deck_penetration=deck_penetration)
        self.db_id = None
        self.players = []
        self.dealer = None
        self.num_players = players
        self.verbose = verbose
        self.matchups = {}
        self.rules = {"soft_17_hit":soft_17_hit,"hit_until":16,"multi_split":multi_split,"blackjack_payout":backjack_payout}

    def start_game(self):
        for i,p in enumerate(range(self.num_players)):
            self.players.append(player(name="Player "+str(i), current_game=self))
        self.dealer = player(dealer=True, current_game=self)
        self.game_cycle()

    def game_cycle(self):
        self.load_game()
        for i in range(100000):
            print("HAND {}".format(i))
            self.deal_hands()
            if not self.peek():
                self.play_hands()
            self.payout()
            self.clear_table()
        # for m in self.matchups:
        #     if self.matchups[m].played >= 1:
        #         print(self.matchups[m])
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
                    p.lost_hand(h.bet,h)
                    # print(1)
                elif h.blackjack and not dealer_hand.blackjack:
                    p.won_hand(h.bet*2*self.rules["blackjack_payout"],h)
                    # print(2)
                elif dealer_hand.blackjack and not h.blackjack:
                    p.lost_to_blackjack(h)
                    p.lost_hand(h.bet,h)
                    # print(3)
                elif dealer_hand.bust and not h.bust:
                    p.won_hand(h.bet*2,h)
                    # print(4)
                elif not dealer_hand.bust and h.bust:
                    p.lost_hand(h.bet,h)
                    # print(5)
                elif not h.blackjack and not dealer_hand.blackjack:
                    if h.max_value > dealer_hand.max_value:
                        p.won_hand(h.bet*2,h)
                        # print(6)
                    elif h.max_value < dealer_hand.max_value:
                        p.lost_hand(h.bet,h)
                        # print(7)
                    else:
                        p.push(h)
                        p.push_hand(h.bet,h)
                else:
                    p.push(h)
                    p.push_hand(h.bet,h)


    def clear_table(self):
        for p in self.players:
            p.clear_hands()
            p.standings()
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

    # Database stuff
    def load_game(self):
        sql = "SELECT id FROM games WHERE decks={} AND penetration={} AND players={} AND soft_17_hit={} AND hit_until={} AND multi_split={} AND blackjack_payout={}".format(*self._game_array)
        game_id = db.lte_run_sql(sql, one=True)
        if game_id is None:
            db.lte_run_sql("INSERT INTO games(decks, penetration, players, soft_17_hit, hit_until, multi_split, blackjack_payout) VALUES (?,?,?,?,?,?,?)",insert_list=self._game_array,one=True)
            game_id = db.lte_run_sql(sql, one=True)
        self.db_id = game_id
        self.load_matchups()

    def save_game(self):
        self.save_matchups()

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
        matchups = db.lte_run_sql(sql)
        if matchups:
            for m in matchups:
                self.build_matchup_from_array(m)
        print("{} Matchups Loaded".format(len(self.matchups)))

    def build_matchup_from_array(self, m_array):
        if len(m_array) != 29: print(len(m_array),"LEN ERROR")
        else:
            new_matchup = hand_matchup(m_array[2],m_array[3])
            new_matchup.db_id = m_array[0]
            new_matchup.action_record = {
                "stand":{"played":m_array[4],"won":m_array[5],"lost":m_array[6],"mwon":m_array[7],"mlost":m_array[8]},
                "hit":{"played":m_array[9],"won":m_array[10],"lost":m_array[11],"mwon":m_array[12],"mlost":m_array[13]},
                "doub":{"played":m_array[14],"won":m_array[15],"lost":m_array[16],"mwon":m_array[17],"mlost":m_array[18]},
                "split":{"played":m_array[19],"won":m_array[20],"lost":m_array[21],"mwon":m_array[22],"mlost":m_array[23]},
                "lost_to_blackjack":{"played":m_array[25],"won":0,"lost":m_array[25],"mwon":0,"mlost":m_array[26]},
                "push":{"played":m_array[24],"won":0,"lost":0,"mwon":0,"mlost":0},
                "bust":{"played":m_array[27],"won":0,"lost":m_array[27],"mwon":0,"mlost":m_array[28]}
                }
            self.matchups[new_matchup.name] = new_matchup


    def save_matchups(self):
        print("Saving Matchups")
        matchup_lists = []
        for m in self.matchups:
            matchup_lists.append((self.db_id,)+self.matchups[m]._matchup_array)
        sql = "DELETE FROM matchups WHERE game_id={}".format(self.db_id)
        db.lte_run_sql(sql)
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
              'bust_mlost) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        print(db.lte_batch_update(sql2,matchup_lists))
        print("{} Matchups Saved".format(len(matchup_lists)))

    @property
    def _game_array(self):
        """
        :return: Array used to save and load the game
        """
        return (int(self.deck.deck_size/52),self.deck.target_deck_penetration,self.num_players,int(self.rules["soft_17_hit"]),self.rules["hit_until"],int(self.rules["multi_split"]),self.rules["blackjack_payout"])

class hand_matchup(object):

    def __init__(self, player_hand, dealer_hand):
        self.name = hand_matchup.matchup_string(player_hand,dealer_hand)
        if "'" in self.name: print(self.name)
        self.db_id = None
        self.action_record = {"hit":{"played":0,"won":0,"lost":0,"mwon":0,"mlost":0},
                              "stand":{"played":0,"won":0,"lost":0,"mwon":0,"mlost":0},
                              "split":{"played":0,"won":0,"lost":0,"mwon":0,"mlost":0},
                              "doub":{"played":0,"won":0,"lost":0,"mwon":0,"mlost":0},
                              "lost_to_blackjack":{"played":0,"won":0,"lost":0,"mwon":0,"mlost":0},
                              "push":{"played":0,"won":0,"lost":0,"mwon":0,"mlost":0},
                              "bust":{"played":0,"won":0,"lost":0,"mwon":0,"mlost":0}
                              }

    CARD_VALUES = {"A":[1,11],"2":[2],"3":[3],"4":[4],"5":[5],"6":[6],"7":[7],"8":[8],"9":[9],"T":[10],"J":[10],"Q":[10],"K":[10]}
    
    @staticmethod
    def values(hand):
        values = []
        for c in hand:
            if values == []:
                values = hand_matchup.CARD_VALUES[c]
            else:
                values = [sum([x,y]) for x in hand_matchup.CARD_VALUES[c] for y in values]
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
        return max(self.action_record["hit"]["played"]+\
               self.action_record["stand"]["played"]+\
               self.action_record["split"]["played"]+\
               self.action_record["doub"]["played"]+\
               self.action_record["lost_to_blackjack"]["lost"],1)

    @property
    def won(self):
        return self.action_record["hit"]["won"]+\
               self.action_record["stand"]["won"]+\
               self.action_record["split"]["won"]+\
               self.action_record["doub"]["won"]

    @property
    def lost(self):
        return self.action_record["hit"]["lost"]+\
               self.action_record["stand"]["lost"]+\
               self.action_record["split"]["lost"]+\
               self.action_record["doub"]["lost"]+\
               self.action_record["lost_to_blackjack"]["lost"]
    @property
    def can_split(self):
        self_string = self.name
        if len(self_string)==4:
            if self_string[0] == self_string[1]:
                return True
        return False

    @property
    def hit_prob(self):
        if self.action_record["hit"]["played"] != 0:
            return round(((self.action_record["hit"]["mwon"]-self.action_record["hit"]["mlost"])/self.action_record["hit"]["played"]),2)*100
            # return round(self.action_record["hit"]["won"]/self.action_record["hit"]["played"]*100,2)
        else:
            return "UNKN"

    @property
    def hit_report(self):
        return "HIT {}/{} {}% @ {}% {}|{}".format(self.action_record["hit"]["played"],self.played,round(self.action_record["hit"]["played"]/self.played*100,2),self.hit_prob,self.action_record["hit"]["mwon"],self.action_record["hit"]["mlost"])

    @property
    def split_prob(self):
        if self.action_record["split"]["played"] != 0:
            return round(((self.action_record["split"]["mwon"]-self.action_record["split"]["mlost"])/self.action_record["split"]["played"]),2)*100
        else:
            if self.can_split:
                return "UNKN"
            return None
    
    @property
    def split_report(self):
        return "Split {}/{} {}% @ {}%".format(self.action_record["split"]["played"],self.played,round(self.action_record["split"]["played"]/self.played*100,2),self.split_prob)

    @property
    def stand_prob(self):
        if self.action_record["stand"]["played"] != 0:
            return round(((self.action_record["stand"]["mwon"]-self.action_record["stand"]["mlost"])/self.action_record["stand"]["played"]),2)*100
        else:
           return "UNKN"
    
    @property
    def stand_report(self):
        return "STAND {}/{} {}% @ {}%".format(self.action_record["stand"]["played"],self.played,round(self.action_record["stand"]["played"]/self.played*100,2),self.stand_prob)
    
    @property
    def doub_prob(self):
        if self.action_record["doub"]["played"] != 0:
            return round(((self.action_record["doub"]["mwon"]-self.action_record["doub"]["mlost"])/self.action_record["doub"]["played"]),2)*100
        else:
           return "UNKN"
    
    @property
    def doub_report(self):
        return "DOUB {}/{} {}% @ {}%".format(self.action_record["doub"]["played"],self.played,round(self.action_record["doub"]["played"]/self.played*100,2),self.doub_prob)

    @property
    def bust_report(self):
        return "BUST {}/{} {}%".format(self.action_record["bust"]["played"],self.played,round(self.action_record["bust"]["played"]/self.played*100,2))

    @property
    def push_report(self):
        return "PUSH {}/{} {}%".format(self.action_record["push"]["played"],self.played,round(self.action_record["push"]["played"]/self.played*100,2))

    @property
    def l2bj_report(self):
        return "L2BJ {}/{} {}%".format(self.action_record["lost_to_blackjack"]["played"],self.played,round(self.action_record["lost_to_blackjack"]["played"]/self.played*100,2))

    @property
    def probabilities(self):
        if self.can_split:
            probs = {"hit":self.hit_prob,"stand":self.stand_prob,"doub":self.stand_prob,"split":self.stand_prob}
        else:
            probs = {"hit":self.hit_prob,"stand":self.stand_prob,"doub":self.stand_prob}
        for p in probs:
            if probs[p] == "UNKN":
                probs[p] = 50
        return probs

    def update_action(self, action, won, mwon):
        self.action_record[action]["played"] += 1
        if won > 0:
            # print("won",action,won,mwon)
            self.action_record[action]["won"] += won
            self.action_record[action]["mwon"] += mwon
        elif won < 0:
            # print("lost",action,won,mwon)
            self.action_record[action]["lost"] -= won #minus negative == addition
            self.action_record[action]["mlost"] += mwon
        else:
            pass
            # print(action)
            #print("PUSH--")
            #self.action_record["push"]["played"] += 1

        # print(self.__repr__())

    def pick_action(self):
        MIN_RAND = 100
        choice = None
        if self.played > MIN_RAND*10:
            choice = weighted_choice(self.probabilities)
            if choice and self.action_record[choice]["played"] > MIN_RAND:
                # print("{} wins {}% of the time ({})".format(choice,round(self.action_record[choice]["won"]/self.action_record[choice]["played"]*100,2),self.action_record[choice]["won"]))
                return choice
        choice = random.choice(list(self.probabilities.keys()))
        # print("{} RANDOM".format(choice))
        return choice

    def __repr__(self):
        if self.can_split:
            return "{} = PLAYED: {} {}% | {} | {} | {} | {} | {} | {} | {}".format(self.name, self.played, round(self.won/self.played*100,2), self.stand_report, self.hit_report, self.doub_report, self.split_report, self.push_report, self.bust_report, self.l2bj_report)
        else:
            return "{} = PLAYED: {} {}% | {} | {} | {} | {} | {} | {}".format(self.name, self.played, round(self.won/self.played*100,2), self.stand_report, self.hit_report, self.doub_report, self.push_report, self.bust_report, self.l2bj_report)


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
                self.action_record["bust"]["mlost"])

    @staticmethod
    def matchup_string(player_hand, dealer_hand):
        if type(player_hand) == hand:
            return hand_matchup.sort_string(player_hand.card_names())+"+"+repr(dealer_hand)[0]
        else:
            player_hand = player_hand.translate({ord(i):None for i in "♣♠♥♦"})
            if type(dealer_hand) == hand:
                return hand_matchup.sort_string(player_hand)+"+"+repr(dealer_hand)[0]
            else:
                return hand_matchup.sort_string(player_hand)+"+"+dealer_hand[0]

    @staticmethod
    def sort_string(cards):
        sorted_cards = ''.join(sorted(cards[:2]))
        return sorted_cards+cards[2:]

def weighted_choice(choices):
    min_v = min(w for c, w in choices.items())
    adj = 0
    if min_v < 0: adj = abs(min_v)
    total = sum(w+adj for c, w in choices.items())
    r = random.uniform(0, total)
    if total == 0: return None
    upto = 0
    for c, w in choices.items():
        wa = w + adj
        if upto + wa > r:
            return c
        upto += wa
    assert False, "Shouldn't get here"


def main():
    new_game = game()
    new_game.start_game()

main()










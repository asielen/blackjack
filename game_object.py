import system as syt
from deck_objects import Deck, HandMatchup
from player_object import Player
import database as db
import os


class Game(object):
    """
    http://wizardofvegas.com/guides/blackjack-survey/
    """

    def __init__(self, play_string='', players=1, num_decks=1,
                 deck_penetration=90, backjack_payout=1.2,
                 multi_split=0, double_after_split=1, soft_17_hit=1, hit_until=16):

        self.settings = {'players': players, 'decks': num_decks, 'deck_penetration': deck_penetration}
        self.rules = {"multi_split": multi_split, "blackjack_payout": backjack_payout,
                      "double_after_split": double_after_split}
        self.dealer_rules = {'soft_17_hit': soft_17_hit, 'hit_until':hit_until}

        self.db_id = None
        self.players = []
        self.min_hands_played = 0
        self.dealer = None
        self.deck = None
        self.verbose = False #VERBOSE
        self.build_game()
        self.deck = self.build_deck()

    def build_game(self):

        def title():
            return "Game String: {}".format(self.game_string)

        def load_game_string():
            self.load_game_string(input('Please insert the new Game String: '))

        def set_players():
            nonlocal self
            try:
                nplayers = int(input('Choose number of players 1-8: '))
                if 1 <= nplayers <= 8:
                    self.settings['players'] = nplayers
                else:
                    raise 'Not a valid number of players'
            except:
                print('Not a vaild number of players')

        def set_decks():
            nonlocal self
            try:
                ndecks = int(input('Choose number of decks 1-100: '))
                if 1 <= ndecks <= 100 :
                    self.settings['decks'] = ndecks
                else:
                    raise 'Not a valid number of decks'
            except:
                print('Not a vaild number of decks')

        def set_penetration():
            nonlocal self
            try:
                npen = int(input('Choose decks penetration 0-100%: '))
                if 0 <= npen <= 100:
                    self.settings['deck_penetration'] = npen
                else:
                    raise 'Not a valid deck penetration'
            except:
                print('Not a valid deck penetration')

        def set_blackjack_payout():
            nonlocal self
            try:
                v = float(input('Choose blackjack payout 1-3: '))
                if 1 <= v <= 3:
                    self.rules['blackjack_payout'] = v
                else:
                    raise 'Not a valid blackjack payout rate'
            except:
                print('Not a valid blackjack payout rate')

        def set_multi_split():
            nonlocal self
            try:
                v = input('Allow Multi-Split? T/F: ')
                if v.lower() == 't':
                    self.rules['multi_split'] = 1
                elif v.lower() == 'f':
                    self.rules['multi_split'] = 0
                else:
                    raise 'Must enter T or F'
            except:
                print('Must enter T or F')

        def set_double_after_split():
            nonlocal self
            try:
                v = input('Allow Double after Split? T/F: ')
                if v.lower() == 't':
                    self.rules['double_after_split'] = 1
                elif v.lower() == 'f':
                    self.rules['double_after_split'] = 0
                else:
                    raise 'Must enter T or F'
            except:
                print('Must enter T or F')

        options = (
            ("Change Game String", load_game_string),
            ("Players", set_players),
            ("Number of Decks", set_decks),
            ("Deck Penetration", set_penetration),
            ("Blackjack Payout", set_blackjack_payout),
            ("Multi Split?", set_multi_split),
            ("Double After Split?", set_double_after_split)
        )
        syt.Menu(name=title, choices=options, quit_tag='Done').run()

    def load_game_string(self, game_string):
        game_string_list = game_string.split('-')
        if(len(game_string_list)!=self.game_string_len):
            print('ERROR Game string Malformed')
            return
        else:
            self.settings = {'players': game_string_list[0],
                             'decks': game_string_list[1],
                             'deck_penetration': game_string_list[2]}
            self.dealer_rules = {'soft_17_hit':game_string_list[5][0],'hit_until':game_string_list[4]}
            self.rules = {"multi_split": game_string_list[5][1],
                          "blackjack_payout": game_string_list[3],
                          "double_after_split": game_string_list[5][2]}

    def build_deck(self):
        return Deck(decks=self.settings['decks'], deck_penetration=self.settings['deck_penetration'])

    @property
    def game_string_len(self):
        return len(self.game_string.split('-'))

    @property
    def strat_string(self):
        '''
        The 111 is:
            [0] double on anything = 1 or only double on certain conditions
                this isn't built out so 1 by default
            [1] surrender - not built yet
            [2] peek - always yes
        :return:
        '''
        return "{}-{}{}101".format(self.settings['decks'],
                                              self.dealer_rules['soft_17_hit'],
                                              self.rules['double_after_split'])

    @property
    def game_string(self):
        '''
            String rep of game format
            AA-BB-CC-DD-EE-FGH
            0AA = Number of players (not including dealer)
            1BB = Number of decks
            2CC = Deck penetration 0-100
            3DD = Blackjack payout 1-2 (decimals allowed)
            4EE = Dealer hit until (default 16)
            50F = 1/0 = T/F Dealer hit on soft 17
            51G = 1/0 = T/F Multi Split Allowed
            52H = 1/0 = T/F Double after Split
        :return:
        '''
        return "{}-{}-{}-{}-{}-{}{}{}".format(self.settings['players'], self.settings['decks'],
                                         self.settings['deck_penetration'], self.rules['blackjack_payout'],
                                         self.dealer_rules['hit_until'], self.dealer_rules['soft_17_hit'],
                                         self.rules['multi_split'], self.rules['double_after_split'])


    def start_game(self, hands=None):
        '''
        :param hands:
        :return:
        '''
        if not hands:
            hands = int(input('How many hands to play?: '))
        self.make_db()
        for i in range(self.settings['players']):
            print(i)
            self.players.append(Player.build_player(game=self))
        self.dealer = Player.build_player(dealer=1, game=self)
        Player.save_players(players=self.players+[self.dealer], game=self)
        self.min_hands_played = min(p.hands_played for p in self.players)
        self.game_cycle(hands)

    def game_cycle(self, hands=1000):
        print("\n--Starting Game--\n")
        SCALE = 10
        HANDS_ADJUST = self.min_hands_played
        for i in range(hands):
            self.deal_hands()
            if not self.peek():
                self.play_hands()
            self.payout()
            self.clear_table()
            if i > 10 and (i % 1000 == 0 or (self.verbose and i % 100 == 0)):
                print("# {} Hands Played".format(i))
            hai = HANDS_ADJUST + i
            if i > 10 and hai % SCALE == 0: #Does this 10 times for every save
                Player.store_all_player_standings(self)
            if i > 10 and hai % (SCALE*100) == 0:
                Player.save_all_player_matchups(self)
                Player.save_all_player_standings(self)
                Player.load_all_value_matchups(self)
            #Hard Coded Scale for speed Factor based on exponential logging increase
            if SCALE != 10000 and ((hai > 10000 and SCALE == 10) or (hai > 1000000 and SCALE == 100) or (hai > 100000000 and SCALE == 1000)):
                SCALE = SCALE*10

        for p in self.players:
            p.standings()
        Player.save_all_player_matchups(self)
        Player.save_all_player_standings(self)
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
                matchup = HandMatchup.matchup_string(h, dealer_hand)
                if matchup not in p.matchups:
                    p.matchups[matchup] = HandMatchup(h, dealer_hand)


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
                    p.won_hand(h.bet, (h.bet * self.rules["blackjack_payout"]), h)
                    # print(2)
                elif dealer_hand.blackjack and not h.blackjack:
                    p.lost_to_blackjack(h)
                    p.lost_hand(h.bet, h)
                    # print(3)
                elif dealer_hand.bust and not h.bust:
                    p.won_hand(h.bet,h.bet, h)
                    # print(4)
                elif not dealer_hand.bust and h.bust:
                    p.lost_hand(h.bet, h)
                    # print(5)
                elif not h.blackjack and not dealer_hand.blackjack:
                    if h.max_value > dealer_hand.max_value:
                        p.won_hand(h.bet, h.bet, h)
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
        # Eventually the last false will be true or false for surrender
        return db.make_project_path("database/BJDB.sqlite")

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
    def make_db(self):
        if not os.path.isfile(self.game_database):
            db.create_database(self.game_database)

    # def save_game(self):
    #     self.save_matchups()

    @property
    def game_array(self):
        """
        :return: Array used to save and load the game
        """
        return [self.settings['decks'],
                self.settings['deck_penetration'],
                self.settings['players'],
                self.dealer_rules['soft_17_hit'],
                self.dealer_rules['hit_until'],
                self.rules['multi_split'],
                self.rules['double_after_split'],
                self.rules['blackjack_payout'],
                self.game_string]


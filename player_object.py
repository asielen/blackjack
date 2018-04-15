from deck_objects import Hand, HandMatchup
import database as db
from basicStrategybuilder import get_strategy_map

import system as syt

import random
import numpy as np
from datetime import datetime

class Player(object):
    MANUAL_PLAY = 1
    RULES_PLAY = 2
    RANDOM_PLAY = 3
    WEIGHTED_PLAY = 4
    BASIC_STRATEGY = 5
    # TOP_CHOICE = 6

    #How often to save standings. Used in player object
    RECENT_HANDS_LEN = 1000

    def __init__(self, dealer=0, name="", current_game=None, standings=None, id=None, matchups = None):

        self.db_id = id
        self.name = name
        if dealer:
            self.name = 'Dealer_{}'.format(datetime.now().strftime('%j%H%M%S'))
        self.dealer = dealer  # True if player is dealer
        self.default_bet = 1
        self.money = 0
        self.hands = []
        self.hands_played = 0
        self.hands_won = 0
        self.hands_lost = 0
        self.hands_push = 0
        self.money_won = 0
        self.money_lost = 0
        self.recent_record = [] # The money result of the last XXX hands. len defined by the game object
        self.value_matchups = {}
        self.matchups = {}
        self.standings2save = {}
        if matchups != None:
            self.matchups = matchups
        if standings is not None:
            self.money = standings["money"]
            self.hands_played = standings["hands_played"]
            self.hands_won = standings["hands_won"]
            self.hands_lost = standings["hands_lost"]
            self.hands_push = standings["hands_push"]
            self.money_won = standings["money_won"]
            self.money_lost = standings["money_lost"]

        self.play_style = 0
        self.random_play_duration = 0
        self.weighted_play_duration = 0
        self.top = 0
        self.value_assist = 0
        self.game = current_game


    @staticmethod
    def build_player(dealer=0, game=None):

        def title():
            if dealer:
                return "Setup Dealer"
            return "Setup Player"

        def load_player():
            return Player.load_players(game)

        def default_player():
            if dealer:
                return PlayerRules(name='Dealer_{}'.format(datetime.now().strftime('%j%H%M%S')), dealer=dealer, current_game=game)
            else:
                return PlayerLearning(name='Default_{}'.format(datetime.now().strftime('%j%H%M%S')), dealer=dealer, current_game=game)

        def new_learning_player():
            return PlayerLearning.build_player(dealer=dealer, current_game=game)

        def new_strategy_player():
            return PlayerBasicStrategy.build_player(dealer=dealer, current_game=game)

        def new_random_player():
            return PlayerRandom.build_player(dealer=dealer, current_game=game)

        def new_rules_player():
            return PlayerRules.build_player(dealer=dealer, current_game=game)

        def new_manual_player():
            return PlayerManual.build_player(current_game=game)

        options = (
            ("Default Player", default_player),
            ("Load Player", load_player),
            ("New Strategy Player", new_strategy_player),
            ("New Rules (dealer style) Player", new_rules_player),
            ("New Learning Player", new_learning_player),
            ("New Random Player", new_random_player),
        )
        if not dealer:
            options = options + (("New Manual Player", new_manual_player),)

        player = None
        while not player:
            player = syt.Menu(name=title, choices=options, quit_tag='Done', drop_down=True).run()
        return player



    # If every current hand of a player is stand (done)
    @property
    def all_hands_stand(self):
        if len(self.hands) == 0: return False
        for h in self.hands:
            if h.is_stand is False:
                return False
        return True

    @property
    def all_hands_bust(self):
        if len(self.hands) == 0: return False
        for h in self.hands:
            if h.bust is False:
                return False
        return True

    # If the player has at least one blackjack
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


    def deal_hand(self):
        self.hands.append(Hand(self.game.deck.deal(), player=self))
        for h in self.hands:
            self.bet(h)

    def show_deal(self):
        hands = "{} playing: ".format(self.name)
        for i, h in enumerate(self.hands):
            if self.dealer:
                hands += "{}: {} | ".format(h.show_dealer_hand(), h.show_dealer_value())
            else:
                hands += "{}: {} ${} | ".format(h.show_player_hand(), h.show_player_value(), h.bet)
                hands = "\n"+hands
        return print(hands)

    def show_hand(self, hand, action):
        if self.game.verbose: print(
            "  {} | Cards {} | Value {} | Bet ${}".format(action, hand.show_player_hand(), hand.show_player_value(),
                                                          hand.bet))
    def draw(self):
        return self.game.deck.draw()

    def play_options(self, hand):
        """

        :param hand: The current hand
        :return: list of possible play options
        """
        if hand is None: return
        options = {}
        options["stand"] = self.stand
        if hand.min_value < 21:
            options["hit"] = self.hit
            if not self.dealer and hand.can_double is True:
                options["doub"] = self.doubledown
        if hand.can_split and not self.dealer:
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
                self.auto_play_hand(h)

    def bet(self, hand):
        # if self.game.verbose: print("Betting {}".format(self.default_bet))
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


    def auto_play_hand(self,chand):
        '''
        Defined in children
        :param chand:
        :return:
        '''
        pass

    def get_matchup(self, player_hand_text):
        """
            Take the hand string and return the matchup object
        """
        matchup = HandMatchup.matchup_string(player_hand_text, self.game.current_dealer_hand)
        if matchup not in self.matchups:
            self.matchups[matchup] = HandMatchup(player_hand_text, self.game.current_dealer_hand)
        return self.matchups[matchup]

    def update_matchups(self, player_hand_text, won, mwon):
        for action, hand_text in player_hand_text.actions_taken:
            cmatchup = self.get_matchup(hand_text)
            cmatchup.update_action(action, won, mwon)

    def clear_hands(self):
        for h in self.hands:
            self.game.deck.return_cards(h.cards)
        self.hands = []
        self.has_insurance = False

    def lost_hand(self, bet, hand):
        self.update_matchups(hand, -1, bet)
        if self.game.verbose:
            print("LOST HAND {} to {}".format(repr(hand), repr(self.game.current_dealer_hand)))
            self.hand_result(hand)
        self.hands_lost += 1
        self.hands_played += 1
        self.money_lost += bet
        if len(self.recent_record) >= Player.RECENT_HANDS_LEN:
            self.recent_record.pop(0)
        self.recent_record.append(-bet)
        # print(hand.actions_taken)

    def won_hand(self, bet, winnings, hand):
        self.update_matchups(hand, 1, winnings+bet)
        if self.game.verbose:
            print("WON HAND {} to {}".format(repr(hand), repr(self.game.current_dealer_hand)))
            self.hand_result(hand)
        self.hands_won += 1
        self.hands_played += 1
        self.money_won += winnings
        self.money += winnings+bet
        if len(self.recent_record) >= Player.RECENT_HANDS_LEN:
            self.recent_record.pop(0)
        self.recent_record.append(winnings)
        # print(hand.actions_taken)

    def push_hand(self, bet, hand):
        self.update_matchups(hand, 0, bet)
        if self.game.verbose:
            print("PUSH HAND {} to {}".format(repr(hand), repr(self.game.current_dealer_hand)))
            self.hand_result(hand)
        self.hands_played += 1
        self.hands_push += 1
        self.money += bet
        if len(self.recent_record) >= Player.RECENT_HANDS_LEN:
            self.recent_record.pop(0)
        self.recent_record.append(0)
        # print(hand.actions_taken)

    def hand_result(self, hand):
        for action in hand.actions_taken:
            if action[0].upper() in ["PUSH","BUST"]: continue
            if action[0].upper() == "LOST_TO_BLACKJACK":
                print("      LOST TO BLACKJACK")
                continue
            matchup = self.get_matchup(action[1])
            result = "    matchup {} played {} times. won {:+.2f}%\n".format(matchup.name,
                                                                     matchup.played,
                                                                     (matchup.won / matchup.played)*100)
            if action[0].upper() == matchup.top_choiceP[0].upper():
                result += "      played: {} returns {:+.2f}%".format(
                                                                         action[0].upper(),
                                                                         round(((matchup.action_record[action[0]]["mwon"] -
                                                                                 matchup.action_record[action[0]][
                                                                                     "mlost"]) /
                                                                                max(matchup.action_record[action[0]]["played"],0.01)),
                                                                               2) * 100,
                                                                         matchup.top_choice[0].upper(),matchup.top_choice[1])
            else:
                result += "      !!played: {} returns {:+.2f}% !! top action {} returns {:+.2f}%".format(
                                                                         action[0].upper(),
                                                                         round(((matchup.action_record[action[0]]["mwon"] -
                                                                                 matchup.action_record[action[0]][
                                                                                     "mlost"]) /
                                                                                max(matchup.action_record[action[0]]["played"],0.01)),
                                                                               2) * 100,
                                                                         matchup.top_choiceP[0].upper(),matchup.top_choiceP[1])
                result += " ## {}".format(matchup.probabilities)
            print(result)
            if "##" in result:
                print("", end="")

    @property
    def moving_avg_won(self):
        return sum([m for m in self.recent_record if m > 0])

    @property
    def moving_avg_lost(self):
        return -sum([m for m in self.recent_record if m < 0])

    @property
    def moving_avg_push(self):
        return sum([m for m in self.recent_record if m == 0]) \

    @ property
    def moving_avg_money(self):
        return (self.moving_avg_won+self.moving_avg_lost+self.moving_avg_push)

    @property
    def count_recent_played(self):
        return len(self.recent_record)

    @property
    def count_recent_won(self):
        return len([m for m in self.recent_record if m > 0])

    @property
    def count_recent_lost(self):
        return len([m for m in self.recent_record if m < 0])

    @property
    def count_recent_push(self):
        return len([m for m in self.recent_record if m == 0])

    @property
    def moving_avg_winnings(self):
        if self.count_recent_played > 0:
            # return round((self.moving_avg_won) / (self.moving_avg_won+self.moving_avg_lost), 4) * 100
            return ((self.moving_avg_won + 0.5*self.moving_avg_push) / (self.moving_avg_won+self.moving_avg_lost+self.moving_avg_push)) * 100
        return 0

    @property
    def count_recent_win_percent(self):
        if self.count_recent_played > 0:
            return ((self.count_recent_won+0.5*self.count_recent_push) / (self.count_recent_played)) * 100
        return 0

    def standings(self):
        print(
            "{} | Win/Loss/Push/Total {}/{}/{}|{} ({:+.2f}% | {:+.2f}% +Pushes)  $MA: {}/{}/{}|{} {:+.2f}% | #MA: {}/{}/{}|{} {:+.2f}% | Win/Loss ${:+.2f}/${:+.2f} | Current Money ${:+.2f} | {:+.2f}%".format(
                self.name,
                self.hands_won,
                self.hands_lost,
                self.hands_push,
                self.hands_played,
                (self.hands_won / (self.hands_played - self.hands_push)) * 100,
                ((self.hands_won+(0.5*self.hands_push)) / self.hands_played) * 100,
                self.moving_avg_won,
                self.moving_avg_lost,
                self.moving_avg_push,
                self.moving_avg_money,
                self.moving_avg_winnings,
                self.count_recent_won,
                self.count_recent_lost,
                self.count_recent_push,
                self.count_recent_played,
                self.count_recent_win_percent,
                self.money_won,
                self.money_lost,
                self.money,
                self.money_won/(self.money_won+self.money_lost)))

    @property
    def player_standings_array(self):
        return (
            self.db_id,
            self.hands_won,
            self.hands_lost,
            self.hands_push,
            self.hands_played,
            self.money_won,
            self.money_lost,
            self.money,
            self.moving_avg_won,
            self.moving_avg_lost,
            self.moving_avg_push,
            self.count_recent_played
        )

    @property
    def player_game_array(self):
        return tuple([self.name, self.dealer, self.play_style, self.random_play_duration, self.weighted_play_duration, self.top, self.value_assist] + self.game.game_array)


    @staticmethod
    def save_players(players, game):
        save_array = [p.player_game_array for p in players if p.db_id is None and p.dealer==0]
        db.lte_run_batch_sql(
            "INSERT INTO players(name, dealer, play_style, random_play_duration, weighted_play_duration, top, value_assist, decks, penetration, players,  soft_17_hit, hit_until, multi_split, doub_after_split, blackjack_payout, game_string) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            values=save_array, db=game.game_database)
        # Get player ids
        namesql = 'SELECT name, id FROM players WHERE name IN (%s)' % ','.join('?'*len(players))
        playerlist = db.lte_run_sql(namesql, insert_list=[p.name for p in players], db=game.game_database)
        playerdict = syt.list_to_dict(playerlist)
        for p in players:
            if not p.dealer:
                p.db_id = playerdict[p.name]

    # Database stuff
    @staticmethod
    def load_players(game, dealer=0):
        '''
            Find all players that match the current game string
        :return:
        '''
        sql = "SELECT id, name, play_style, random_play_duration, weighted_play_duration, top, value_assist FROM players WHERE game_string = '{}';".format(game.game_string)
        player_query = db.lte_run_sql(sql, db=game.game_database)
        player_map = {p[1]:p for p in player_query}

        if not len(player_query):
            return None
        if dealer:
            # Dealer can't be manual
            options = [p[1] for p in player_query if p[2] != Player.MANUAL_PLAY]
        else:
            options = [p[1] for p in player_query]
        def get_player_string(player_name):
            return player_map[player_name]

        player = None
        while not player:
            playerlist = syt.Menu(name='Load Player', choices=options, function=get_player_string, type=syt.Menu.LOAD, drop_down=True).run()
            player = Player.load_player(playerlist, game, dealer)
        player.load_player_standings()
        return player

    @staticmethod
    def load_player(player_list, game, dealer=0):
        if len(player_list) != 7: return None
        id, name, play_Style, random_play_duration, weighted_play_duration, top, value_assist = player_list
        player = None
        if play_Style == Player.RULES_PLAY:
            player = PlayerRules(name=name, id=id, dealer=dealer, current_game=game)
        elif play_Style == Player.RANDOM_PLAY:
            player = PlayerRandom(name=name, id=id, dealer=dealer, current_game=game)
        elif play_Style == Player.WEIGHTED_PLAY:
            player = PlayerLearning(name=name, id=id, random_play_duration=random_play_duration, weighted_play_duration=weighted_play_duration, enable_top=top, value_assist=value_assist, dealer=dealer, current_game=game)
        elif play_Style == Player.BASIC_STRATEGY:
            player = PlayerBasicStrategy(name=name, id=id, dealer=dealer, current_game=game)
        elif play_Style == Player.MANUAL_PLAY:
            player = PlayerManual(name=name, id=id, dealer=dealer, current_game=game)
        player.load_player_standings()
        player.load_player_matchups()
        if player.value_assist:
            player.load_value_matchups()
        return player

    def load_player_standings(self):
        sql = "SELECT player_id, hands_won, hands_lost, hands_push, hands_played, money_won, money_lost, money" \
              " FROM player_standings WHERE hands_played = (SELECT max(hands_played) FROM player_standings where player_id={});".format(self.db_id)
        psq =  db.lte_run_sql(sql, one=True, db=self.game.game_database)
        if not psq: return None

        self.hands_won = psq[1]
        self.hands_lost = psq[2]
        self.hands_push = psq[3]
        self.hands_played = psq[4]
        self.money_won = psq[5]
        self.money_lost = psq[6]
        self.money = psq[7]


    def store_player_standings(self):
        self.standings2save[self.hands_played] = self.player_standings_array

    def save_player_standings(self):
        sql = "INSERT INTO player_standings(player_id, hands_won, hands_lost, hands_push, " \
                            "hands_played, money_won, money_lost, money, " \
                            "moving_avg_won, moving_avg_lost, moving_avg_push, moving_avg_played) " \
                            "values(?,?,?,?,?,?,?,?,?,?,?,?)"
        db.lte_batch_update(sql, csvfile=self.standings2save.values(), db=self.game.game_database)
        self.standings2save = {}
        if self.game.verbose: print("Player Saved: {}".format(self.name))

    @staticmethod
    def save_all_player_standings(game):
        for p in game.players:
            p.save_player_standings()

    @staticmethod
    def store_all_player_standings(game):
        for p in game.players:
            p.store_player_standings()

    def load_player_matchups(self):
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
              "FROM matchups WHERE player_id={}".format(self.db_id)
        matchups = db.lte_run_sql(sql, db=self.game.game_database)
        if matchups:
            for m in matchups:
                new_matchup = HandMatchup.build_matchup_from_array(m)
                if new_matchup != None:
                    self.matchups.update(new_matchup)
        print("{} Matchups Loaded".format(len(self.matchups)))

    # def save_game(self):
    #     self.save_matchups()

    def load_value_matchups(self):
        self.value_matchups = dict()
        # Returns the highest probability play for all matching bs_value matchups
        # print("Loading BS Value Matchups")
        sql = "SELECT bs_string, count(bs_string), (SUM(stand_mwon)-SUM(stand_mlost))/(SUM(stand_mwon)+SUM(stand_mlost))*1000, (SUM(hit_mwon)-SUM(hit_mlost))/(SUM(hit_mwon)+SUM(hit_mlost))*1000, (SUM(doub_mwon)-SUM(doub_mlost))/(SUM(doub_mwon)+SUM(doub_mlost))*1000, (SUM(split_mwon)-SUM(split_mlost))/(SUM(split_mwon)+SUM(split_mlost))*1000 FROM matchups WHERE player_id = {} GROUP BY bs_string;".format(self.db_id)
        v_matchups = db.lte_run_sql(sql, db=self.game.game_database)
        #action_lookup = {0: None, 2: "stand", 3: "hit", 4: "doub", 5: "split"} #Corrisponds to column numbers in the return sql
        for m in v_matchups:
            probabilities = {"stand" : m[2], "hit" : m[3], "doub" : m[4], "split" : m[5]}
            self.value_matchups[m[0]] = probabilities
        if self.game.verbose: print("{} Value Matchups Loaded".format(len(v_matchups)))

    def get_missing_value_matchup(self,lu_bs_string):
        mups = self.matchups
        b = np.sum(np.array([(mups[d].action_record['stand']['mwon'],
                    mups[d].action_record['stand']['mlost'],
                    mups[d].action_record['hit']['mwon'],
                    mups[d].action_record['hit']['mlost'],
                    mups[d].action_record['doub']['mwon'],
                    mups[d].action_record['doub']['mlost'],
                    mups[d].action_record['split']['mwon'],
                    mups[d].action_record['split']['mlost'],
                    ) for d in self.matchups if mups[d].bs_string == lu_bs_string]),axis=0)
        if np.sum(b)==0:
            return None
        def p(l,n):
            if l[n]+l[n+1] == 0: return None
            return ((l[n]-l[n+1])/(l[n]+l[n+1]))*1000
        probabilities = {"stand": p(b,0), "hit": p(b,2), "doub": p(b,4), "split": p(b,6)}
        self.value_matchups[lu_bs_string] = probabilities
        return probabilities

    def save_player_matchups(self):
        # print("Saving Matchups")
        matchup_lists = []
        for m in self.matchups:
            matchup_lists.append((self.db_id,) + self.matchups[m]._matchup_array)
        sql = "DELETE FROM matchups WHERE player_id={};".format(self.db_id)
        db.lte_run_sql(sql, db=self.game.game_database)
        sql2 = 'INSERT INTO matchups(player_id, ' \
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
               'value_name, ' \
               'bs_string, ' \
               'num_cards) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        db.lte_batch_update(sql2, matchup_lists, db=self.game.game_database)
        if self.hands_played > 1000 or self.game.verbose: print("{} Matchups Saved".format(len(matchup_lists)))

    @staticmethod
    def save_all_player_matchups(game):
        for p in game.players:
            p.save_player_matchups()

    @staticmethod
    def load_all_value_matchups(game):
        for p in game.players:
            p.load_value_matchups()

    @staticmethod
    def build_all_value_matchups_from_memory(game):
        for p in game.players:
            p.build_value_matchups_from_memory()



class PlayerManual(Player):
    def __init__(self, name="", dealer=0, current_game=None, standings=None, id=None):
        super().__init__(name=name, dealer=dealer, current_game=current_game, standings=standings, id=id)
        self.play_style = Player.MANUAL_PLAY

    @staticmethod
    def build_player(current_game):
        return PlayerManual(name='Self', current_game=current_game)

    def auto_play_hand(self, chand):
        pass



class PlayerRandom(Player):
    def __init__(self, name="", dealer=0, current_game=None, standings=None, id=None):
        super().__init__(name=name, dealer=dealer, current_game=current_game, standings=standings, id=id)
        self.play_style = Player.RANDOM_PLAY

    @staticmethod
    def build_player(current_game, dealer=0):
        if not dealer:
            name = input('Please give the player a name: ')
        else:
            name = 'Dealer_{}'.format(datetime.now().strftime('%j%H%M%S'))
        return PlayerRandom(name=name, dealer=dealer, current_game=current_game)

    def auto_play_hand(self, chand):
        while not chand.is_stand:
            if chand.bust:
                self.bust(chand)
                break
            if not chand.bust and not chand.blackjack:
                play_options = self.play_options(chand)
                play_choice = play_options[random.choice(list(play_options.keys()))]
                play_choice(chand)
                if play_choice == self.split:
                    break
            else:
                self.stand(chand)


class PlayerRules(Player):
    def __init__(self, name="", dealer=0, current_game=None, standings=None, id=None):
        super().__init__(name=name, dealer=dealer, current_game=current_game, standings=standings, id=id)
        self.play_style = Player.RULES_PLAY

    @staticmethod
    def build_player(current_game, dealer=0):
        if not dealer:
            name = input('Please give the player a name: ')
        else:
            name = 'Dealer_{}'.format(datetime.now().strftime('%j%H%M%S'))
        return PlayerRules(name=name, dealer=dealer, current_game=current_game)

    def auto_play_hand(self, chand):
        while not chand.is_stand:
            if chand.bust:
                self.bust(chand)
                break
            elif chand.blackjack:
                self.stand(chand)
            else:
                if chand.max_value == 17 and chand.min_value < 17 and chand.soft:
                    # If it is a hard 17 don't follow these rules
                    # A+6 = True
                    # A+T+5 = False
                    if self.game.dealer_rules["soft_17_hit"]:
                        self.stand(chand)
                    else:
                        self.hit(chand)
                elif chand.max_value <= self.game.dealer_rules["hit_until"]:
                    # Hit if hand is 16 or less. Max value gives largest value 21 or below so this doesn't
                    #  need any more qualifiers
                    self.hit(chand)
                else:
                    self.stand(chand)




class PlayerBasicStrategy(Player):
    def __init__(self, name="", dealer=0, current_game=None, standings=None, id=None):
        super().__init__(name=name, dealer=dealer, current_game=current_game, standings=standings, id=id)
        self.play_style = Player.BASIC_STRATEGY
        self.bs_db = get_strategy_map(current_game.strat_string)

    @staticmethod
    def build_player(current_game, dealer=0):
        '''Need to lookup the basic strategy and attach it for this'''
        if not (dealer):
            name = input('Please give the player a name: ')
        else:
            name = 'Dealer_{}'.format(datetime.now().strftime('%j%H%M%S'))
        return PlayerBasicStrategy(name=name, dealer=dealer, current_game=current_game)

    @staticmethod
    def get_bs_choice(bs_db, chand, dealer_hand, play_options, name_only=False):
        def _make_bs_matchup(chand, dealer_hand):
            dealer_card = repr(dealer_hand)[0]
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
        lu_string = _make_bs_matchup(chand, dealer_hand)
        if lu_string in bs_db and bs_db[lu_string]:
            if bs_db[lu_string][0] in play_options:
                if name_only: return bs_db[lu_string][0] #This is for comparing to other methods
                play_choice = play_options[bs_db[lu_string][0]]
            elif len(bs_db[lu_string]) == 2 and bs_db[lu_string][1] in play_options:
                if name_only: return bs_db[lu_string][1]
                play_choice = play_options[bs_db[lu_string][1]]
            else:
                play_choice = None
        if play_choice == None:
            print("",end="")
        return play_choice

    def auto_play_hand(self, chand):
        '''
        Foll imported basic strategy
        :param chand:
        :return:
        '''
        #bs_db = basic[self.game.bs_name]
        play_options = self.play_options(chand)
        while not chand.is_stand:
            if chand.bust:
                self.bust(chand)
                break

            play_choice = PlayerBasicStrategy.get_bs_choice(self.bs_db, chand, self.game.current_dealer_hand, play_options)

            if not play_choice:
                print("Random Pick")
                play_choice = play_options[random.choice(list(play_options.keys()))]
            play_choice(chand)
            if play_choice == self.split:
                break

class PlayerLearning(Player):

    def __init__(self, name="", dealer=0, current_game=None, standings=None, random_play_duration=10, weighted_play_duration=10, enable_top=0, id=None, bs_eval=False, value_assist=True):
        super().__init__(name=name, dealer=dealer, current_game=current_game, standings=standings, id=id)
        self.random_play_duration = random_play_duration # The number of repeated hands before it starts to take into account weights
        self.weighted_play_duration = weighted_play_duration # The number of repeated hands before it goes to top only
        self.top = enable_top #If true, the player will always pick the top choice based on hand wins. Will still consider the random_duration
        self.play_style = Player.WEIGHTED_PLAY
        self.bs_db = None
        self.value_assist = value_assist #Should we use other hands results with BD classifications for under formed hands (while learning and top)
        if bs_eval: self.bs_db = get_strategy_map(current_game.strat_string)


    @staticmethod
    def build_player(current_game, dealer=0):
        if not(dealer):
            name = input('Please give the player a name: ')
        else:
            name = 'Dealer_{}'.format(datetime.now().strftime('%j%H%M%S'))

        random_duration = None
        while random_duration is None:
            try:
                random_duration = int(input('How many hands before learning kicks in?: '))
            except:
                random_duration = None
        enable_top = input('Enable Top Choice Play? t/f (default false): ')
        if enable_top.lower() in ('t','true','y','yes','1'):
            enable_top = 1
        else:
            enable_top = 0
        weighted_duration = 0
        if enable_top:
            try:
                weighted_duration = int(input('How many weighted hands before Top Only kicks in?: '))
            except:
                weighted_duration = 0
        value_assist = input('Enable Value Based Assist t/f (default true): ')
        if value_assist.lower() in ('t', 'true', 'y', 'yes', '1'):
            value_assist = True
        else:
            value_assist = False
        return PlayerLearning(name=name, dealer=dealer, current_game=current_game, random_play_duration=random_duration, weighted_play_duration=weighted_duration, enable_top=enable_top, value_assist=value_assist)

    def auto_play_hand(self, chand):
        '''
        Learning weighted on wins
        :param chand:
        :return:
        '''
        while not chand.is_stand:
            if chand.bust:
                self.bust(chand)
                break
            if not chand.bust and not chand.blackjack:
                play_options = self.play_options(chand)

                choice = self.get_matchup_choice(chand, play_options.keys())

                if not choice or choice not in play_options:
                    if choice != 'doub':
                        print('      NOT DOUB: {}'.format(choice))
                    # All this below should not be accessable anymore
                    if self.game.verbose:
                        if choice not in play_options:
                            print('      Invalid Choice: {}'.format(choice))
                        else:
                            print('      No Choice: {}'.format(choice))
                        print('R$', end='')
                    # This seems to mostly be for doubs when doub isn't valid, should just go to hit, but why isn't doub valid
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

    def get_matchup_choice(self, hand, play_options):
        matchup = self.get_matchup(hand)
        choice = None
        if matchup.played <= self.random_play_duration:
            if self.game.verbose: print("  Random Hand Played - Total {}".format(matchup.played))
            choice = matchup.pick_random_action(play_options)
        elif self.top and matchup.played > self.random_play_duration + self.weighted_play_duration:
            if self.game.verbose: print("  Top Hand Played - Total {}".format(matchup.played))
            choice = self.get_top_choice(matchup, play_options)
        else:
            if self.value_assist and matchup.played <= self.random_play_duration + self.weighted_play_duration:
                if self.game.verbose: print("  Value Assist Hand Played - Total {}".format(matchup.played))
                if matchup.bs_string not in self.value_matchups:
                    self.get_missing_value_matchup(matchup.bs_string)
                if matchup.bs_string in self.value_matchups:
                    choice = self.get_value_choice(matchup, self.value_matchups[matchup.bs_string])
            else:
                if self.game.verbose: print("  Weighted Hand Played - Total {}".format(matchup.played))
                choice = self.get_weighted_choice(matchup, play_options)
                if not choice and self.value_assist:
                    if matchup.bs_string not in self.value_matchups:
                        self.get_missing_value_matchup(matchup.bs_string)
                    if matchup.bs_string in self.value_matchups:
                        choice = self.get_value_choice(matchup, self.value_matchups[matchup.bs_string])
            if not choice:
                choice = matchup.pick_random_action(play_options)
        return choice

    def get_weighted_choice(self, matchup, play_options):
        return matchup.pick_action(play_options=play_options)

    def get_value_choice(self, matchup, play_options):
        return matchup.pick_value_action(play_options_dict=play_options)

    def get_top_choice(self, matchup, play_options):
        choice = None
        choice = matchup.get_clear_top_choice(play_options)
        if not choice:
            if self.game.verbose: print("  No Clear Top? {}".format(matchup.probabilities))
            return matchup.pick_random_action(play_options)
        else:
            if self.game.verbose: print("  Top Choice")
            return choice



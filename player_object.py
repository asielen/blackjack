from deck_objects import Hand, HandMatchup
import system as syt
import database as db
import random
from datetime import datetime
from basic_strategy_dicts import basic
from basicStrategybuilder import get_strategy_map

class Player(object):
    MANUAL_PLAY = 1
    RULES_PLAY = 2
    RANDOM_PLAY = 3
    WEIGHTED_PLAY = 4
    BASIC_STRATEGY = 5
    TOP_CHOICE = 6

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
        self.recent_record = []
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
        self.play_style_delay = 0
        self.top = 0
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

    def lost_hand(self, money_lost, hand):
        self.update_matchups(hand, -1, money_lost)
        if self.game.verbose:
            print("LOST HAND {} to {}".format(repr(hand), repr(self.game.current_dealer_hand)))
            self.hand_result(hand)
        self.hands_lost += 1
        self.hands_played += 1
        self.money_lost += money_lost
        if len(self.recent_record) >= self.game.RECENT_HANDS_LEN:
            self.recent_record.pop(0)
        self.recent_record.append(-money_lost)
        # print(hand.actions_taken)

    def won_hand(self, money_won, hand):
        self.update_matchups(hand, 1, money_won)
        if self.game.verbose:
            print("WON HAND {} to {}".format(repr(hand), repr(self.game.current_dealer_hand)))
            self.hand_result(hand)
        self.hands_won += 1
        self.hands_played += 1
        self.money_won += money_won
        self.money += money_won
        if len(self.recent_record) >= self.game.RECENT_HANDS_LEN:
            self.recent_record.pop(0)
        self.recent_record.append(money_won)
        # print(hand.actions_taken)

    def push_hand(self, money_push, hand):
        self.update_matchups(hand, 0, money_push)
        if self.game.verbose:
            print("PUSH HAND {} to {}".format(repr(hand), repr(self.game.current_dealer_hand)))
            self.hand_result(hand)
        self.hands_played += 1
        self.hands_push += 1
        self.money += money_push
        if len(self.recent_record) >= self.game.RECENT_HANDS_LEN:
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
            result = "    matchup {} played {} times. won {}%\n".format(matchup.name,
                                                                     matchup.played,
                                                                     round((matchup.won / matchup.played)*100, 2))
            if action[0].upper() == matchup.top_choiceP[0].upper():
                result += "      played: {} returns {}%".format(
                                                                         action[0].upper(),
                                                                         round(((matchup.action_record[action[0]]["mwon"] -
                                                                                 matchup.action_record[action[0]][
                                                                                     "mlost"]) /
                                                                                max(matchup.action_record[action[0]]["played"],0.01)),
                                                                               2) * 100,
                                                                         matchup.top_choice[0].upper(),matchup.top_choice[1])
            else:
                result += "      !!played: {} returns {}% !! top action {} returns {}%".format(
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
            return round((self.moving_avg_won + 0.5*self.moving_avg_push) / (self.moving_avg_won+self.moving_avg_lost+self.moving_avg_push), 4) * 100
        return 0

    def standings(self):
        print(
            "{} | Win/Loss/Push/Total {}/{}/{}|{} ({}% | {}% +Pushes)  MA: {}/{}/{}|{} {}% | Win/Loss ${}/${} | Current Money ${} | {}%".format(
                self.name,
                self.hands_won,
                self.hands_lost,
                self.hands_push,
                self.hands_played,
                round((self.hands_won / (self.hands_played - self.hands_push)) * 100, 4),
                round(((self.hands_won+(0.5*self.hands_push)) / self.hands_played) * 100, 4),
                self.moving_avg_won,
                self.moving_avg_lost,
                self.moving_avg_push,
                self.moving_avg_played,
                self.moving_avg,
                round(self.money_won, 2),
                round(self.money_lost, 2),
                round(self.money, 2),
                round(self.money_won/(self.money_won+self.money_lost), 2)))

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
            self.moving_avg_played
        )

    @property
    def player_game_array(self):
        return tuple([self.name, self.dealer, self.play_style, self.play_style_delay, self.top]+self.game.game_array)


    @staticmethod
    def save_players(players, game):
        save_array = [p.player_game_array for p in players if p.db_id is None and p.dealer==0]
        db.lte_run_batch_sql(
            "INSERT INTO players(name, dealer, play_style, play_style_delay, top, decks, penetration, players,  soft_17_hit, hit_until, multi_split, doub_after_split, blackjack_payout, game_string) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
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
        sql = "SELECT id, name, play_style, play_style_delay, top FROM players WHERE game_string = '{}';".format(game.game_string)
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
        if len(player_list) != 5: return None
        id, name, play_Style, play_style_delay, top = player_list
        player = None
        if play_Style == Player.RULES_PLAY:
            player = PlayerRules(name=name, id=id, dealer=dealer, current_game=game)
        elif play_Style == Player.RANDOM_PLAY:
            player = PlayerRandom(name=name, id=id, dealer=dealer, current_game=game)
        elif play_Style == Player.WEIGHTED_PLAY:
            player = PlayerLearning(name=name, id=id, play_style_delay=play_style_delay, top_only=top, dealer=dealer, current_game=game)
        elif play_Style == Player.BASIC_STRATEGY:
            player = PlayerBasicStrategy(name=name, id=id, dealer=dealer, current_game=game)
        elif play_Style == Player.MANUAL_PLAY:
            player = PlayerManual(name=name, id=id, dealer=dealer, current_game=game)
        player.load_player_standings()
        player.load_player_matchups()
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
        print("Saving Player: {}".format(self.name))
        sql = "INSERT INTO player_standings(player_id, hands_won, hands_lost, hands_push, " \
                            "hands_played, money_won, money_lost, money, " \
                            "moving_avg_won, moving_avg_lost, moving_avg_push, moving_avg_played) " \
                            "values(?,?,?,?,?,?,?,?,?,?,?,?)"
        db.lte_batch_update(sql, csvfile=self.standings2save.values(), db=self.game.game_database)
        self.standings2save = {}

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
        print("Loading Value Matchups")
        sql = "SELECT value_name, count(value_name), (SUM(stand_mwon)-SUM(stand_mlost))/SUM(stand_played)*100, (SUM(hit_mwon)-SUM(hit_mlost))/SUM(hit_played)*100, (SUM(doub_mwon)-SUM(doub_mlost))/SUM(doub_played)*100, (SUM(split_mwon)-SUM(split_mlost))/SUM(split_played)*100 FROM matchups WHERE player_id = {} GROUP BY value_name;".format(self.db_id)
        v_matchups = db.lte_run_sql(sql, db=self.game.game_database)
        action_lookup = {0: None, 2: "stand", 3: "hit", 4: "doub", 5: "split"}
        for m in v_matchups:
            try:
                top_return = m.index(max(value for value in m[2:] if value is not None))
            except:
                top_return = 0
            self.value_matchups[m[0]] = action_lookup[top_return]

    def save_player_matchups(self):
        print("Saving Matchups")
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
               'num_cards) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        db.lte_batch_update(sql2, matchup_lists, db=self.game.game_database)
        print("{} Matchups Saved".format(len(matchup_lists)))

    @staticmethod
    def save_all_player_matchups(game):
        for p in game.players:
            p.save_player_matchups()


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

    def __init__(self, name="", dealer=0, current_game=None, standings=None, play_style_delay=10, top_only=0, id=None, bs_eval=True):
        super().__init__(name=name, dealer=dealer, current_game=current_game, standings=standings, id=id)
        self.play_style_delay = play_style_delay # The number of repeated hands before it starts to take into account weights
        self.top = top_only #If true, the player will always pick the top choice based on hand wins
        self.play_style = Player.WEIGHTED_PLAY
        self.bs_db = None
        if bs_eval: self.bs_db = get_strategy_map(current_game.strat_string)

    @staticmethod
    def build_player(current_game, dealer=0):
        if not(dealer):
            name = input('Please give the player a name: ')
        else:
            name = 'Dealer_{}'.format(datetime.now().strftime('%j%H%M%S'))

        play_delay = None
        while play_delay is None:
            try:
                play_delay = int(input('How many hands before auto kicks in?: '))
            except:
                play_delay = None
        top_only = input('Top only? t/f (default false): ')
        if top_only.lower() in ('t','true','y','yes','1'):
            top_only = 1
        else:
            top_only = 0
        return PlayerLearning(name=name, dealer=dealer, current_game=current_game, play_style_delay=play_delay, top_only=top_only)

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
                if self.top:
                    choice = self.get_top_choice(chand, play_options.keys())
                else:
                    choice = self.get_matchup_choice(chand, play_options.keys())

                if not choice or choice not in play_options:
                    if self.game.verbose:
                        if choice not in play_options:
                            print('      Invalid Choice: {}'.format(choice))
                        else:
                            print('      No Choice: {}'.format(choice))
                        print('R$', end='')
                    play_choice = play_options[random.choice(list(play_options.keys()))]
                else:
                    play_choice = play_options[choice]
                # Compare to basic strategy choices
                # if self.game.verbose :
                #     bs_choice = PlayerBasicStrategy.get_bs_choice(self.bs_db, chand, self.game.current_dealer_hand, play_options, name_only=True)
                #     if bs_choice != choice:
                #         print("  NBS {}: PICKED {} | BS: {}".format(chand,choice,bs_choice))
                #         # print("!", end='')
                play_choice(chand)
                if play_choice == self.split:
                    break
            elif chand.blackjack:
                self.stand(chand)
            else:
                print("NO ACTION {}".format(chand))
                self.stand(chand)

    def get_matchup_choice(self, hand, play_options):
        """Todo: for some reason this doesn't always return the best weighted choice. there should be some randomness but not often"""
        matchup = self.get_matchup(hand)
        if matchup.played == 1:
            try:
                mtch = self.value_matchups["{}+{}".format(matchup.player_hand_max_value, matchup.dealer_hand)]
                if mtch in play_options:
                    #print('V#',end='')
                    return mtch
                else:
                    pass
            except:
                pass
        return matchup.pick_action(play_options=play_options, delay=self.play_style_delay)

    def get_top_choice(self, hand, play_options):
        """

        :param hand:
        :param delay:
        :return:
        """

        matchup = self.get_matchup(hand)
        if matchup.played < self.play_style_delay:
            if self.game.verbose: print("  New hand - Hand Played {}".format(matchup.played))
            return matchup.pick_random_action(play_options)
        elif not matchup.clear_top_choice:
            if self.game.verbose: print("  Clear Top? {} - {}".format(matchup.clear_top_choice, matchup.probabilities))
            return matchup.pick_random_action(play_options)
        elif matchup.top_choice not in play_options:
            if self.game.verbose: print("  Not Valid? {} - {}".format(matchup.top_choice, play_options.keys()))
            return matchup.pick_random_action(play_options)
        else:
            if self.game.verbose: print("  Top Choice")
            return matchup.top_choice



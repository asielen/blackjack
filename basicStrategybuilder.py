import system as syt
from system import soupify
import json


strategy_url = "https://www.blackjackinfo.com/blackjack-basic-strategy-engine/"

def get_strategy_map(strat_string):
    '''
    1) try to load
    2) try to get online (save if new)
    3) return dict
    '''
    bs_dict = {}
    try:
        with open('basic_strategy.json', 'r') as fp:
            bs_dict = json.load(fp)
    except FileNotFoundError:
        print("No save file")
    if strat_string in bs_dict:
        print("Found {}... Loading".format(strat_string))
        return bs_dict[strat_string]
    else:
        print("Building {}... Downloading".format(strat_string))
        bs_dict[strat_string] = get_strategy_map_from_string(strat_string)
    with open('basic_strategy.json', 'w') as fp:
        json.dump(bs_dict, fp)
    return bs_dict[strat_string]


def save_strategy_map():
    bs_dict = {}
    with open('basic_strategy.json', 'r') as fp:
        json.dump(bs_dict, fp)

def get_strategy_map_from_string(strat_string):
    num_decks, strat_string = strat_string.split('-')
    num_decks = int(num_decks)
    soft17 = True
    double = True
    double_after_split = True
    surrender = False
    peek = True
    if not int(strat_string[0]): soft17 = False
    if not int(strat_string[1]): double_after_split = False
    if not int(strat_string[2]): double = False
    if int(strat_string[3]): surrender = True
    if not int(strat_string[4]): peek = True
    return build_basic_strategy(get_strategy_table(num_decks, soft17, double, double_after_split, surrender, peek))



def get_strategy_table(num_decks=1,soft17=True,double=True,double_after_split=True,surrender=False,peek=True):
    if soft17: soft17 = 'h17'
    else: soft17 = 's17'
    if double: double = 'all'
    if double_after_split: double_after_split = 'yes'
    else: double_after_split = 'no'
    if surrender: surrender = 'ls'
    else: surrender = 'ns'
    if peek: peek = 'yes'
    else: peek = 'no'
    url = strategy_url+"?numdecks={}&soft17={}&dbl={}&das={}&surr={}&peek={}".format(num_decks,
                                                                                     soft17,
                                                                                     double,
                                                                                     double_after_split,
                                                                                     surrender,
                                                                                     peek)
    soup = soupify(url)
    if not soup:
        return
    tables = soup.findAll("table", {"class": "mB30"})
    if len(tables) != 3:
        print("Didn't find the right number of tables")
        return
    hard = syt.parse_html_table(tables[0])
    soft = syt.parse_html_table(tables[1])
    pair = syt.parse_html_table(tables [2])
    return {'hard':hard,'soft':soft,'pair':pair}


def build_basic_strategy(tables):
    bs_dict = {}
    dealer_value_list = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "A"]
    play_dict_lu = {"S": ["stand"], "H": ["hit"], "P": ["split"],"D":["doub"],"DH": ["doub", "hit"], "DS": ["doub", "split"],"RH":["hit", "surr"],"RS":["stand", "surr"]}

    def _parse_player_value(value_string):
        """
            Hard format = just the number
            Soft format = max value S
            Pair format = Value,Value
        :param value_string:
        :return:
        """
        if 'Hard' in value_string:
            return value_string.split(" ")[1].replace("+","")
        elif 'Ace' in value_string:
            return str(11+int(value_string[-1]))+"S"
        else:
            return value_string.replace("(","").replace(")","")

    for t in tables.values():
        for row in t:
            if len(row) == 2 or len(row) == 10:
                # print("skip line")
                continue
            current_player_value = [_parse_player_value(row[0])]
            current_play_list = row[1:]
            if len(current_play_list) != 10:
                print("Wrong sized row")
            if current_player_value[0] == '18':
                current_player_value = ['18','19','20','21']  #Go through 18, 19, 20, 21
            if current_player_value[0] == '20S':
                current_player_value = ['20S', '21S']  # Go through 18, 19, 20, 21
            for player_value in current_player_value:
                for i, m in enumerate(current_play_list):
                    current_matchup = "{}X{}".format(player_value, dealer_value_list[i])
                    bs_dict[current_matchup] = play_dict_lu[m]
                    if dealer_value_list[i] == "T":
                        for c in ["J", "Q", "K"]:
                            current_matchup = "{}X{}".format(player_value, c)
                            bs_dict[current_matchup] = play_dict_lu[m]
    return bs_dict



def main():
    print(get_strategy_map('1-11101'))
    for n in range(8):
        get_strategy_map('{}-11101'.format(n+1))
        get_strategy_map('{}-10101'.format(n + 1))
        get_strategy_map('{}-01101'.format(n + 1))
        get_strategy_map('{}-00101'.format(n + 1))

if __name__ == "__main__":
    main()
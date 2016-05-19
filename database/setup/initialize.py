# External
import sqlite3 as lite

# Internal
import database as db



def create_database():
    """
    Simply creates the framework of the database
    @return:
    """
    _initiate_database()


def _initiate_database():
    con = lite.connect(db.database)
    with con:

        con.execute("CREATE TABLE IF NOT EXISTS games(id INTEGER PRIMARY KEY,"
                    "decks INTEGER, "
                    "players INTEGER, "
                    "hands_played INTEGER, "
                    "soft_17_hit INTEGER, "
                    "hit_until INTEGER, "
                    "multi_split INTEGER, "
                    "allow_insurance INTEGER, "
                    "blackjack_payout FLOAT);")

        con.execute("CREATE TABLE IF NOT EXISTS matchups(id INTEGER PRIMARY KEY,"
                    "game_id INTEGER, "
                    "player_id INTEGER, "
                    "player_hand TEXT, "
                    "dealer_card TEXT, "
                    "player_max_value INTEGER, "
                    "player_min_value INTEGER, "
                    "soft_hand INTEGER, "
                    "hit_played INTEGER, "
                    "hit_won INTEGER,"
                    "hit_lost INTEGER,"
                    "hit_mwon FLOAT,"
                    "hit_mlost FLOAT,"
                    "stand_played INTEGER, "
                    "stand_won INTEGER,"
                    "stand_lost INTEGER,"
                    "stand_mwon FLOAT,"
                    "stand_mlost FLOAT,"
                    "doub_played INTEGER, "
                    "doub_won INTEGER,"
                    "doub_lost INTEGER,"
                    "doub_mwon FLOAT,"
                    "doub_mlost FLOAT,"
                    "split_played INTEGER, "
                    "split_won INTEGER,"
                    "split_lost INTEGER,"
                    "split_mwon FLOAT,"
                    "split_mlost FLOAT,"
                    "bust INTEGER, "
                    "lost_to_blackjack INTEGER,"
                    "pushed INTEGER);")

        con.execute("CREATE TABLE IF NOT EXISTS players(id INTEGER PRIMARY KEY,"
                    "game_id INTEGER, "
                    "name TEXT,"
                    "hands_won INTEGER, "
                    "hands_lost INTEGER, "
                    "money_won FLOAT, "
                    "money_lost FLOAT, "
                    "hands_played INTEGER);")

        con.execute("CREATE TABLE IF NOT EXISTS hands(id INTEGER PRIMARY KEY,"
                    "game_id INTEGER, "
                    "player_id INTEGER, "
                    "hand_number INTEGER, "
                    "hands_won INTEGER, "
                    "hands_lost INTEGER, "
                    "money_won FLOAT, "
                    "money_lost FLOAT, "
                    "hands_played INTEGER);")

        con.execute("PRAGMA FOREIGN_KEYS=1;") # Enforce foreign keys

        print("%%% Database Created")

if __name__ == "__main__":
    create_database()
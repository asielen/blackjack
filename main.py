import system as syt

from game_object import Game


def main_menu():
    def start_new_game():
        new_game = Game()
        new_game.start_game()

    def system_settings():
        pass

    options = (
        ("Start New game", start_new_game),
        ("System Settings", system_settings)
    )
    syt.Menu(name='Play Blackjack', choices=options, quit_tag="Exit").run()




def main():

    new_game = Game()
    #new_game.start_game()
    #new_game = Game(play_type_delay=50, deck_penetration=60, num_decks=6, play_type=player.TOP_CHOICE,
    #                    soft_17_hit=False, backjack_payout=1.5, multi_split=True, double_after_split=True, verbose=True)
    #new_game.start_game(10000000)


main_menu()
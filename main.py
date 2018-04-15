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

main_menu()
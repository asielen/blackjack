
import os
def make_project_path(string=""):
    """
     Windows uses \, mac uses /
    @return: the path to the price_capture_menu project folder with an optional string
    """
    path = os.path.dirname(os.path.realpath(__file__)).split("blackjack")[0]
    if string != "":
        string = string.replace("/", os.sep)  # To fix mac > pc
        string = string.replace("\\", os.sep)  # To fix pc > mac
        return os.path.abspath(path+'blackjack'+os.sep+string)
    else:
        return os.path.abspath(path+"blackjack"+os.sep)

database = make_project_path("database/BlackJackDatabase.sqlite")



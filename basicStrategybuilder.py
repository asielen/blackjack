import system as syt
import csv
import pprint

def main():
    """
    Build basic strategy dict from csv doc
    """



    csv_dir = 'bscsvfiles/'
    print(syt.make_dir('{}{}'.format(csv_dir,"test")))
    def _load(file):
        return syt.make_dir('{}{}'.format(csv_dir,file))

    choices = syt.Load_Menu.find_saveFiles(csv_dir, '.csv')
    csv_file = syt.Load_Menu(name="- Load csv file -", function=_load, choices=choices).run()
    print(csv_file)
    if csv_file is not None and csv_file != 0:
        bs_dict = {}
        current_player_value = None
        dealer_value_list = ["2","3","4","5","6","7","8","9","T","A"]
        current_matchup = ""
        current_play_list = []
        play_dict_lu = {"S":["stand"],"H":["hit"],"P":["split"],"Dh":["doub","hit"],"Ds":["doub","split"]}
        with open(csv_file, newline='', encoding='utf-8') as cf:
            creader = csv.reader(cf)
            for row in creader:
                if row[0] in ["Hard","Soft","Pair"]:
                    # print("skip line")
                    continue
                current_player_value = row[0]
                current_play_list = row[1:]
                if len(current_play_list) != 10:
                    print("Wrong sized row")
                for i, m in enumerate(current_play_list):
                    # print(m)
                    current_matchup = "{}X{}".format(current_player_value,dealer_value_list[i])
                    bs_dict[current_matchup] = play_dict_lu[m]
                    if dealer_value_list[i] == "T":
                        for c in ["J","Q","K"]:
                            current_matchup = "{}X{}".format(current_player_value,c)
                            bs_dict[current_matchup] = play_dict_lu[m]

        pprint.pprint(bs_dict)
        print(bs_dict)



if __name__ == "__main__":
    main()
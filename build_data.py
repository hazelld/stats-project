import csv


STATS = ["MP","FG","FGA","3P","3PA","FT","FTA","ORB","DRB","TRB","AST","STL","BLK","TOV","PF","PTS"]

def find_player(player_list, player = "LeBron James"):
    for player_dict in player_list:
        if player_dict["Player"] == player:
            return player_dict
    print("Error: Can't find " + player + " in data: ")
    print(player_list)
    return -1

def split_data(boxscore_data):
    """
    This function will split the data from one CSV file into three parts. The first is the
    "LeBron" part, that is a dict that stores his stats from a game. The second is the 
    "Opponent" part that stores the totals for the other team. Last is the sum of his team's
    stats.
    """
    # Get Lebron's stats and cut out unneeded ones
    lebron_tmp = dict(find_player(boxscore_data))
    lebron = {"Team": lebron_tmp["Team"]}
    for stat, val in lebron_tmp.items():
        if stat in STATS:
            lebron[stat] = val

    team_totals = [{}, {}]
    for player in boxscore_data:

        # Sometimes the "Team Totals" line doesn't save properly and the row is offset by 1,
        # this will fix that by skipping it.
        if player["Player"].isdigit() or player["Player"] == "Team Totals":
            continue
        team_index = int(player["Team"])

        if player["Team"] == lebron["Team"]:
            team_prefix = "Team_"
        else:
            team_prefix = "Opponent_"

        # Add totals
        for stat, val in player.items():
            if stat not in STATS:
                continue
             
            stat = team_prefix + stat
            if stat not in team_totals[team_index]:
                team_totals[team_index][stat] = 0

            # Hacky way of adding up opponent's MP
            if stat == "Opponent_MP" or stat == "Team_MP":
                min_sum = sum_minutes(team_totals[team_index][stat], val)
                team_totals[team_index][stat] = min_sum
            else:
                team_totals[team_index][stat] += int(val)
   
    # Sum up the minutes
    lb_team = int(lebron["Team"])
    other_team = 1 - lb_team
    return {"LeBron": lebron, "Opponent": team_totals[other_team], "Team": team_totals[lb_team]}

def sum_minutes(m1, m2):
    if m1 == 0:
        return m2

    min1 = m1.split(":")
    min2 = m2.split(":")

    minutes = int(min1[0]) + int(min2[0])
    seconds = int(min1[1]) + int(min2[1])

    minutes += int(seconds / 60)
    seconds = seconds % 60

    if seconds < 10:
        seconds = "0" + str(seconds)
    return str(minutes) + ":" + str(seconds)



def sum_splits(splits, player="LeBron"):
    """
    This function will sum up a list of dicts returned from split_data() into one single dict
    that has the totals of all 3.
    """
    sum_dict = {player:{}, "Team": {}, "Opponent": {}}
    for split in splits:
        for split_name, stat_dict in split.items():
            for stat, value in stat_dict.items():
                if stat == "Player":
                    continue
                if stat not in sum_dict[split_name]:
                    sum_dict[split_name][stat] = 0
                if stat in ["Opponent_MP", "Team_MP", "MP"]:
                    mp = sum_dict[split_name][stat]
                    sum_dict[split_name][stat] = sum_minutes(mp, value)
                else:
                    sum_dict[split_name][stat] += int(value)
    return sum_dict

def load_file(fname):
    with open(fname) as csvfile:
        reader = csv.DictReader(csvfile)
        players = []
        for row in reader:
            players.append(row)
        return split_data(players)

game_1 = 'data/boxscores/20091028.csv'
game_2 = 'data/boxscores/20091030.csv'

data_1 = load_file(game_1)
data_2 = load_file(game_2)
total = sum_splits([data_1, data_2])
print(total["LeBron"])
print(total["Team"])
print(total["Opponent"])

import csv
import calc


STATS = ["MP","FGM","FGA","3PM","3PA","FTM","FTA","ORB","DRB","TRB","AST","STL","BLK","TOV","PF","PTS"]

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
                if isinstance(val, int) or val.isdigit():
                    team_totals[team_index][stat] += int(val)
   
    # Sum up the minutes
    lb_team = int(lebron["Team"])
    other_team = 1 - lb_team
    return {"Player": lebron, "Opponent": team_totals[other_team], "Team": team_totals[lb_team]}

def sum_minutes(m1, m2):
    """
    This function is used to sum minutes in the form of "mm:ss", it will 
    return a string in the format "mm:ss".
    """
    if m1 == 0:
        return m2

    min1 = m1.split(":")
    min2 = m2.split(":")

    if not min1[0].isdigit() or not min2[0].isdigit():
        return m1

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
    sum_dict = {"Player":{}, "Team": {}, "Opponent": {}}
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
                    # Sometimes get nan and stuff
                    if isinstance(value, int) or value.isdigit():
                        sum_dict[split_name][stat] += int(value)
    return sum_dict

def load_boxscore_file(fname):
    with open(fname) as csvfile:
        reader = csv.DictReader(csvfile)
        players = []
        for row in reader:
            players.append(row)
        return split_data(players)

def load_league_info(game_date):
    # game_date in form yyyymmdd
    year = game_date[0:4]
    month = game_date[4:6]

    if month in ["10", "11", "12"]:
        year = int(year) + 1
    
    with open('data/League_Data.csv') as csvfile:
        creader = csv.DictReader(csvfile, delimiter=',')
        for row in creader:
            if row["Year"] == str(year):
                return row
    return None
    

def calculate_advanced_stats(split):
    """
    This function takes the 4 dicts (Player, Opponent, Team, LeagueInfo) and will calculate the
    advanced statistics for the player, and will merge all 3 dicts into 1.

    Calculated stats are:
    - OffensiveWinShares
    - DefensiveWinShares
    - DRtg (defensive rating)
    - ORtg (offensive rating)

    Note: split["Year"] must equal the SEASON the game takes place in, not the year
    the game took place in. For instance, a game in December 2008 should have the 
    season 2009. This corresponds with the data in the data/League_Data.csv file.
    """
    all_stats = {**split["Player"], **split["Opponent"], **split["Team"], **split["LeagueInfo"]}
    all_stats = convert_data(all_stats)
    all_stats["OffensiveWinShares"] = calc.OffensiveWinShares(all_stats)
    all_stats["DefensiveWinShares"]  = calc.DefensiveWinShares(all_stats)
    all_stats["DRtg"] = calc.DRtg(all_stats)
    all_stats["ORtg"] = calc.ORtg(all_stats)
    return all_stats

def convert_data(data):
    """
    This function converts the given data to the proper formats from the strings we read in
    """
    prefixs = ["", "Opponent_", "Team_"]
    ints_end  = ["FGM","FGA","3PM","3PA","FTM","FTA","ORB","DRB","TRB","AST","STL","BLK","TOV","PF","PTS"]
    floats_end= ["Team_Pace", "League_Pace", "LPPP", "LPPG"]
    mps_end = ["MP"]

    ints = [p+i for p in prefixs for i in ints_end]
    floats = [p+f for p in prefixs for f in floats_end]
    mps = [p+m for p in prefixs for m in mps_end]
    
    for key, val in data.items():
        if key in ints:
            if isinstance(val, int) or val.isdigit():
                data[key] = int(val)
        elif key in floats:
            data[key] = float(val)
        elif key in mps:
            mins = val.split(":")
            if mins[0].isdigit():
                data[key] = int(mins[0])
            else: # Count DNPs as 0 minutes
                data[key] = 0

    return data

def print_dict(stats):
    for key, val in stats.items():
        print(key + " == " + str(val))

with open('data/seasons/2009.csv') as csvfile:
    creader = csv.DictReader(csvfile, delimiter=',')
    data = []
    for row in creader:
        """
        if ((row["Date"][0:4] == "2009" and row["Date"][5:7] in ["10", "11", "12"]) or
            (row["Date"][0:4] == "2010" and row["Date"][5:7] not in ["10", "11", "12"])):
        """
        print("Loading data from: " + row["Date"])
        date = row["Date"].replace("-", "")
        box_data = load_boxscore_file("data/boxscores/" + date + ".csv")
        box_data["Player"]["Date"] = date
        data.append(box_data)
    final = sum_splits(data)
    final["LeagueInfo"] = load_league_info("20090101")
    stats = calculate_advanced_stats(final)
    print_dict(stats)
    print(calc.TotalPossessions(stats))
    print(calc.PointsProduced(stats))


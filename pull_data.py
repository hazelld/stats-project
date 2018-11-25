import requests
import csv
import pandas as pd

INPUT_FIELDS = ["Starters","MP","FG","FGA","FG%","3P","3PA","3P%","FT","FTA","FT%","ORB", 
                "DRB","TRB","AST","STL","BLK","TOV","PF","PTS","+/-"]
OUTPUT_FIELDS = ["Player","MP","FGM","FGA","FG%","3PM","3PA","3P%","FTM","FTA","FT%","ORB", 
                "DRB","TRB","AST","STL","BLK","TOV","PF","PTS","+/-", "Team"]

def parse_team_table(table):
    """
    This horrendous function parses one of the tables on the bball ref page, and will put all the stats 
    into a list of players that all stats are accessible by key. Note that "Starters" column is changed
    to "Player".
    """
    player_list = []
    for i in table.iteritems():
        index = 0
        column_name = i[0][1]
        if column_name in INPUT_FIELDS:
            for stat in i[1].values:
                # Create dict if it doesn't exist
                if len(player_list) <= index:
                    player_list.append({})

                output_column_name = OUTPUT_FIELDS[INPUT_FIELDS.index(column_name)]
                player_list[index][output_column_name] = stat
                index += 1
   
    return player_list

def get_boxscore(date, home_team):
    """
    """
    url = "https://www.basketball-reference.com/boxscores/" + date + "0" + home_team + ".html"
    r = requests.get(url)
    tables = pd.read_html(r.text)
    
    team1 = parse_team_table(tables[0])
    team2 = parse_team_table(tables[2])
    save_boxscore(date, [ team1, team2 ])


def save_boxscore(date, team_data):
    """
    Saves the boxscore, differentiating the players by a simple field "Team" that will be 
    0/1. Note this is pretty hacky for my need, since I don't really care which team the 
    player is on, only if they are on LeBron's or not.
    """
    with open('data/boxscores/' + date + '.csv', 'w', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=OUTPUT_FIELDS)
        writer.writeheader()

        for z in range(0, 2):
            for i in team_data[z]:
                i["Team"] = z
                if i["Player"] == "Reserves":
                    continue
                if i["Player"] == "":
                    i["Player"] = "Team Totals"
                writer.writerow(i)

"""
Go through the master list of LeBron's games, and get each boxscore and save it
"""
with open('data/seasons/master.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        new_date = row["Date"].replace('-', '')
        if row["Loc"] == "@":
            home_team = row["Opp"]
        else:
            home_team = row["Tm"]

        get_boxscore(new_date, home_team)

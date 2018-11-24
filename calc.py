import math

"""
Note all naming matches the formuli on this page:

https://www.basketball-reference.com/about/ratings.html
"""


def ScoringPossessions(data):
    """
    The following need defined for calculation (and the requirements for each func)
        - data["Team_ORB"]-> Team's offensive rebounds
    """
    return ((FG_Part(data) + AST_Part(data) + FT_Part(data)) *
            (1 - (data["Team_ORB"] / Team_Scoring_Poss(data)) * Team_ORB_Weight(data)
                * Team_Play_Percent(data)) +
            ORB_Part(data))


def FG_Part(data):
    """
    The following must be defined for calculation:
        - data["FGM"] -> Field goals made
        - data["PTS"] -> Points
        - data["FTM"] -> Free throws made
        - data["FGA"] -> Free throws attempted
    """
    return ( data["FGM"] * (1 - 0.5 * ((data["PTS"] - data["FTM"]) /
            (2 * data["FGA"])) * qAST(data)))

def qAST(data):
    """
    The following must be defined:
        - data["MP"] -> Minutes played (player)
        - data["Team_MP"] -> Team Minutes played
        - data["Team_AST"] -> Team Assists
        - data["AST"] -> Assists (player)
        - data["Team_FGM"] -> Team FieldGoal Made
        - data["Team_AST"] -> Team Assists
        - data["FGM"] -> Field Goal made (player)

        This is one ugly calculation
    """
    return ((data["MP"] / (data["Team_MP"] / 5)) *
            (1.14 * ((data["Team_AST"] - data["AST"]) / data["Team_FGM"])) +
            ((((data["Team_AST"] / data["Team_MP"]) * data["MP"] * 5 - data["AST"]) /
                ((data["Team_FGM"] / data["Team_MP"]) * data["MP"] * 5 - data["FGM"])) *
                (1 - (data["MP"] / (data["Team_MP"] / 5)))))

def AST_Part(data):
    """
    The following must be defined:
        - data["Team_PTS"] -> Team points
        - data["Team_FTM"] -> Team Free throw made
        - data["PTS"] -> Player points
        - data["FTM"] -> Free throw made player
        - data["Team_FGA"] -> Team field goal attempted
        - data["FGA"] -> Player field goal attempted
        - data["AST"] -> Player assists
    """
    return (0.5 * (((data["Team_PTS"] - data["Team_FTM"]) - (data["PTS"] - data["FTM"])) /
            (2 * (data["Team_FGA"] - data["FGA"]))) * data["AST"])

def FT_Part(data):
    """
    The following must be defined:
        - data["FTM"] - Player free throws made
        - data["FTA"] - Player free throws attempted
    """
    return ((1 - math.pow((1 - (data["FTM"] / data["FTA"])), 2)) * 0.4 * data["FTA"])

def Team_Scoring_Poss(data):
    """
    The following must be defined:
        - data["Team_FGM"] - Team field goal made
        - data["Team_FTM"] - Team free throw made
        - data["Team_FTA"] - Team free throw attempted
    """
    return (data["Team_FGM"] + (1 - (math.pow(1 - (data["Team_FTM"] / data["Team_FTA"]), 2))) *
            data["Team_FTA"] * 0.4)

def Team_Poss(data):
    return (Team_Scoring_Poss(data) + TeamFGxPoss(data) + TeamFTxPoss(data) + data["Team_TOV"])

def Team_ORB_Weight(data):
    """
    The following must be defined:
    """
    tpp = Team_Play_Percent(data)
    torbp = Team_ORB_Percent(data)
    return (((1 - torbp) * tpp) / ((1 - torbp) * tpp + torbp * (1 - tpp)))

def Team_ORB_Percent(data):
    """
    The following must be defined:
        - data["Team_ORB"] -> Team offensive rebounds
        - data["Opponent_TRB"] -> Opponent total rebounds
        - data["Opponent_ORB"] -> Opponent offensive rebounds
    """
    return (data["Team_ORB"] / (data["Team_ORB"] + (data["Opponent_TRB"] - data["Opponent_ORB"])))

def Team_Play_Percent(data):
    """
    The following must be defined:
        - data["Team_FGA"] -> Team field goals attempted
        - data["Team_FTA"] -> Team free throws attempted
        - data["Team_TOV"] -> Team turnovers
    """
    return (Team_Scoring_Poss(data) / (data["Team_FGA"] + data["Team_FTA"] * 0.4 + data["Team_TOV"]))

def ORB_Part(data):
    """
    The following must be defined:
        - data["ORB"] -> Player offensive rebounds
    """
    return data["ORB"] * Team_ORB_Weight(data) * Team_Play_Percent(data)

def FGxPoss(data):
    """
    The following must be defined:
        - data["FGA"] -> Player field goal attempted
        - data["FGM"] -> Player field goal made
    """
    return ((data["FGA"] - data["FGM"]) * (1 - 1.07 * Team_ORB_Percent(data)))

def TeamFGxPoss(data):
    return ((data["Team_FGA"] - data["Team_FGM"]) * (1 - 1.07 * Team_ORB_Percent(data)))

def FTxPoss(data):
    """
    The following must be defined:
        - data["FTA"] -> Player free throw attempted
        - data["FTM"] -> Player free throw made
    """
    return (math.pow(1 - (data["FTM"] / data["FTA"]), 2) * 0.4 * data["FTA"])

def TeamFTxPoss(data):
    return (math.pow(1 - (data["Team_FTM"] / data["Team_FTA"]), 2) * 0.4 * data["Team_FTA"])

def TotalPossessions(data):
    """
    The following must be defined (this includes _all_ sub function's requirements):
        data["FGM"] - Player field goals made
        data["FGA"] - Player field goals attempted
        data["FTM"] - Player free throws made
        data["FTA"] - Player free throws attempted
        data["ORB"] - Player offensive rebounds
        data["DRB"] - Player defensive rebounds
        data["AST"] - Player assists
        data["TOV"] - Player turnovers
        data["PTS"] - Player points
        data["MP"]  - Player minutes playe
        data["Team_FGM"] - Team field goals made
        data["Team_FGA"] - Team field goals attempted
        data["Team_FTM"] - Team free throws made
        data["Team_FTA"] - Team free throws attempted
        data["Team_ORB"] - Team offensive rebounds
        data["Team_DRB"] - Team defensive rebounds
        data["Team_AST"] - Team assists
        data["Team_TOV"] - Team turnovers
        data["Team_PTS"] - Team points
        data["Team_MP"]  - Team minutes played
        data["Opponent_TRB"] - Opponent's total rebounds
        data["Opponent_ORB"] - Opponent's offensive rebounds
    """
    return ScoringPossessions(data) + FGxPoss(data) + FTxPoss(data) + data["TOV"]

def PointsProduced(data):
    return ((PProd_FG_Part(data) + PProd_AST_Part(data) + data["FTM"]) *
            (1 - (data["Team_ORB"] / Team_Scoring_Poss(data)) * Team_ORB_Weight(data) * 
                Team_Play_Percent(data)) +
            PProd_ORB_Part(data))

def PProd_FG_Part(data):
    return (2 * (data["FGM"] + 0.5 * data["3PM"]) * (1 - 0.5 * ((data["PTS"] - data["FTM"]) /
            (2 * data["FGA"])) * qAST(data)))

def PProd_AST_Part(data):
    return (2 * ((data["Team_FGM"] - data["FGM"] + 0.5 * (data["Team_3PM"] - data["3PM"])) /
        (data["Team_FGM"] - data["FGM"])) * 0.5 * (((data["Team_PTS"] - data["Team_FTM"]) -
            (data["PTS"] - data["FTM"])) / (2 * (data["Team_FGA"] - data["FGA"]))) *
        data["AST"])

def PProd_ORB_Part(data):
    return (data["ORB"] * Team_ORB_Weight(data) * Team_Play_Percent(data) *
            (data["Team_PTS"] / (data["Team_FGM"] + (1 - 
                math.pow(1 - (data["Team_FTM"] / data["Team_FTA"]), 2)) * 0.4 * data["Team_FTA"])))

def FloorPercentage(data):
    return ScoringPossessions(data) / TotalPossessions(data)

def MarginalOffensePlayer(data):
    """
    The following must be defined:
        - data["LPPP"] -> League points per possessions 
    """
    return PointsProduced(data) - 0.92 * data["LPPP"] * TotalPossessions(data)

def MarginalPointsPerWin(data):
    """
    The following must be defined:
        - data["LPPG"] -> League Points per game average
        - data["Team_Pace"] -> Teams points per 100 possessions
        - data["League_Pace"] -> League average points per 100 possessions
    """
    return 0.32 * data["LPPG"] * (data["Team_Pace"] / data["League_Pace"])

def OffensiveWinShares(data):
    return MarginalOffensePlayer(data) / MarginalPointsPerWin(data)

"""
DEFENSIVE CALCULATIONS
"""
def Stops(data):
    return StopsOne(data) + StopsTwo(data)

def StopsOne(data):
    return (data["STL"] + data["BLK"] * FMwt(data) * (1 - 1.07 * DOR_Percent(data)) + 
            data["DRB"] * (1 - FMwt(data)))

def StopsTwo(data):
    return ((((data["Opponent_FGA"] - data["Opponent_FGM"] - data["Team_BLK"])) /
            data["Team_MP"]) * FMwt(data) * (1 - 1.07 * DOR_Percent(data)) + 
            ((data["Opponent_TOV"] - data["Team_STL"]) / data["Team_MP"]) * data["MP"] +
            (data["PF"] / data["Team_PF"]) * 0.4 * data["Opponent_FTA"] * 
            math.pow(1 - (data["Opponent_FTM"] / data["Opponent_FTA"]), 2))

def FMwt(data):
    return ((DFG_Percent(data) * (1 - DOR_Percent(data))) / (DFG_Percent(data) * 
            (1 - DOR_Percent(data)) + (1 - DFG_Percent(data)) * DOR_Percent(data)))

def DOR_Percent(data):
    return (data["Opponent_ORB"] / (data["Opponent_ORB"] + data["Team_DRB"]))

def DFG_Percent(data):
    return (data["Opponent_FGM"] / data["Opponent_FGA"])

def Stop_Percent(data):
    return ((Stops(data) * data["Opponent_MP"]) / (Team_Poss(data) * data["MP"]))

def DRtg(data):
    print(str(Team_Defensive_Rating(data)) + "+ 0.2 * (100 * " + str(D_Pts_per_ScPoss(data)) + " * (1 - " + str(Stop_Percent(data)) + ") - " + str(Team_Defensive_Rating(data)) + ")")
    return (Team_Defensive_Rating(data) + 0.2 * (100 * D_Pts_per_ScPoss(data) * 
            (1 - Stop_Percent(data)) - Team_Defensive_Rating(data)))

def Team_Defensive_Rating(data):
    return 100 * (data["Opponent_PTS"] / Team_Poss(data))

def D_Pts_per_ScPoss(data):
    return (data["Opponent_PTS"] / (data["Opponent_FGM"] + (1 - 
        math.pow(1 - (data["Opponent_FTM"] / data["Opponent_FTA"]), 2)) *
        data["Opponent_FTA"] * 0.4))
"""
Lebron 2008/2009
"""
data = {
    "FGM": 789,
    "FGA": 1613,
    "FTM": 594,
    "FTA": 762,
    "ORB": 106,
    "DRB": 507,
    "AST": 587,
    "TOV": 241,
    "PTS": 2304,
    "3PM": 132,
    "BLK": 93,
    "STL": 137,
    "PF": 139,
    "MP": 3054,
    "Team_FGM": 3022, 
    "Team_FGA": 6454,
    "Team_FTM": 1523,
    "Team_FTA": 2012,
    "Team_ORB": 886,
    "Team_DRB": 2574,
    "Team_AST": 1663,
    "Team_TOV": 1045,
    "Team_PTS": 8223,
    "Team_3PM": 656,
    "Team_BLK": 435,
    "Team_STL": 593,
    "Team_PF": 1663,
    "Team_MP": 19780,
    "Opponent_TRB": 3188,
    "Opponent_ORB": 878,
    "Opponent_FGA": 6444,
    "Opponent_FGM": 2775,
    "Opponent_PTS": 7491,
    "Opponent_FTA": 1459,
    "Opponent_FTM": 1895,
    "Opponent_TOV": 1137,
    "Opponent_MP": 19780,
    "Opponent_Possessions": 88.7 * 82,
    "Team_Possessions": 88.7 * 82,
    "LPPP": 1.083,
    "LPPG": 100,
    "Team_Pace": 88.7,
    "League_Pace": 91.7,
}

print("Team Defensive Rating:")
print(Team_Defensive_Rating(data))
print("D_Pts_per..:")
print(D_Pts_per_ScPoss(data))
print("Stop %:")
print(Stop_Percent(data))
print("LBJ Defensive Rating:")
print(DRtg(data))
print("\n\n\n\nTeam Poss:")
print(Team_Poss(data))


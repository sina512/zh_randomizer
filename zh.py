import re
import numpy as np
import random
import pandas as pd
import time

armies = [
        "GLA",
        "TOXIN",
        "STEALTH",
        "DEMOLATION",
        "CHINA",
        "TANK",
        "NUKE",
        "INFANTRY",
        "USA",
        "SUPER WEAPON",
        "LASER",
        "AIR FORCE"
]

'''
DOMINATOR:
TD NO CARS
Both players super pros
No major mistakes in game
Random balance is ON
'''
matchup_str = """ 
SUPER WEAPON vs AIR FORCE 5
NUKE vs AIR FORCE 5
USA vs AIR FORCE 10
LASER vs AIR FORCE 10
CHINA vs AIR FORCE 10
NUKE vs LASER 10
CHINA vs TOXIN 10
CHINA vs STEALTH 10
CHINA vs DEMOLATION 10
CHINA vs GLA 10
NUKE vs INFANTRY 10
NUKE vs USA 10
TANK vs INFANTRY 10
CHINA vs LASER 15
CHINA vs USA 15
NUKE vs SUPER WEAPON 15
TANK vs TOXIN 20
TANK vs DEMOLATION 20
INFANTRY vs TOXIN 25
TANK vs AIR FORCE 25
TANK vs USA 25
TANK vs LASER 25
TANK vs GLA 30
CHINA vs NUKE 30
SUPER WEAPON vs TOXIN 35
TANK vs NUKE 35
NUKE vs DEMOLATION 35
INFANTRY vs STEALTH 35
INFANTRY vs DEMOLATION 35
INFANTRY vs GLA 40
CHINA vs TANK 40
GLA vs DEMOLATION 40
SUPER WEAPON vs GLA 40
SUPER WEAPON vs DEMOLATION 40
SUPER WEAPON vs STEALTH 40
INFANTRY vs AIR FORCE 40
CHINA vs INFANTRY 40
DEMOLATION vs AIR FORCE 40
NUKE vs TOXIN 40
NUKE vs GLA 40
INFANTRY vs LASER 40
TANK vs SUPER WEAPON 40
SUPER WEAPON vs INFANTRY 45
SUPER WEAPON vs LASER 45
SUPER WEAPON vs CHINA 45
TOXIN vs DEMOLATION 45
GLA vs LASER 45
GLA vs TOXIN 45
GLA vs AIR FORCE 45
STEALTH vs DEMOLATION 45
STEALTH vs TOXIN 50
TANK vs STEALTH 50
GLA vs USA 50
TOXIN vs AIR FORCE 50
DEMOLATION vs LASER 50
STEALTH vs LASER 50
GLA vs STEALTH 50
USA vs INFANTRY 50
TOXIN vs LASER 50
DEMOLATION vs USA 50
STEALTH vs USA 50
TOXIN vs USA 50
USA vs SUPER WEAPON 50
USA vs LASER 50
AIR FORCE vs STEALTH 50
STEALTH vs NUKE 50
USA vs USA 50
LASER vs LASER 50
AIR FORCE vs AIR FORCE 50
SUPER WEAPON vs SUPER WEAPON 50
CHINA vs CHINA 50
INFANTRY vs INFANTRY 50
TANK vs TANK 50
NUKE vs NUKE 50
GLA vs GLA 50
DEMOLATION vs DEMOLATION 50
STEALTH vs STEALTH 50
TOXIN vs TOXIN 50
NUKE vs STEALTH 50
STEALTH vs AIR FORCE 50
LASER vs USA 50
SUPER WEAPON vs USA 50
USA vs TOXIN 50
USA vs STEALTH 50
USA vs DEMOLATION 50
LASER vs TOXIN 50
INFANTRY vs USA 50
STEALTH vs GLA 50
LASER vs STEALTH 50
LASER vs DEMOLATION 50
AIR FORCE vs TOXIN 50
USA vs GLA 50
STEALTH vs TANK 50
TOXIN vs STEALTH 50
DEMOLATION vs STEALTH 55
AIR FORCE vs GLA 55
TOXIN vs GLA 55
LASER vs GLA 55
DEMOLATION vs TOXIN 55
CHINA vs SUPER WEAPON 55
LASER vs SUPER WEAPON 55
INFANTRY vs SUPER WEAPON 55
SUPER WEAPON vs TANK 60
LASER vs INFANTRY 60
GLA vs NUKE 60
TOXIN vs NUKE 60
AIR FORCE vs DEMOLATION 60
GLA vs SUPER WEAPON 60
STEALTH vs SUPER WEAPON 60
INFANTRY vs CHINA 60
AIR FORCE vs INFANTRY 60
DEMOLATION vs SUPER WEAPON 60
DEMOLATION vs GLA 60
TANK vs CHINA 60
GLA vs INFANTRY 60
DEMOLATION vs INFANTRY 65
STEALTH vs INFANTRY 65
DEMOLATION vs NUKE 65
NUKE vs TANK 65
TOXIN vs SUPER WEAPON 65
NUKE vs CHINA 70
GLA vs TANK 70
AIR FORCE vs TANK 75
LASER vs TANK 75
USA vs TANK 75
TOXIN vs INFANTRY 75
DEMOLATION vs TANK 80
TOXIN vs TANK 80
SUPER WEAPON vs NUKE 85
USA vs CHINA 85
LASER vs CHINA 85
INFANTRY vs TANK 90
USA vs NUKE 90
INFANTRY vs NUKE 90
GLA vs CHINA 90
DEMOLATION vs CHINA 90
STEALTH vs CHINA 90
TOXIN vs CHINA 90
AIR FORCE vs CHINA 90
LASER vs NUKE 90
AIR FORCE vs LASER 90
AIR FORCE vs USA 90
AIR FORCE vs NUKE 95
AIR FORCE vs SUPER WEAPON 95
"""



match_up = pd.DataFrame(columns=armies,index=armies)

for army1 in match_up.columns.values:
    for army2 in match_up.index.values:
        pattern = re.compile('{} vs {} {}'.format(army1,army2,'[0-9]{1,2}'))
        result = re.findall(pattern, matchup_str)
        #print(army1+" "+army2)
        #print(result)
        if len(result) > 0:
            percentage = int(re.findall('[0-9]?[0-9]',result[0])[0])
            match_up.loc[army1,army2] = percentage
        else:
            print("missing matchup")  



class team:
    def __init__(self, name,n):
        self.name = name
        self.n = n
        self.players = []
        self.armies = []
        self.rates = []
        self.chance = 0
        self.single_rates = {}

    def add_player(self,player):
        self.players.append(player)
        self.armies.append(random.choices(armies,k=1)[0])

    def calculate_rates(self, other):
        for army1 in self.armies:
            rate=0
            for army2 in other.armies:
                self.rates.append(match_up.loc[army1, army2])
                other.rates.append(match_up.loc[army2, army1])
                self.single_rates[army1 + " vs " + army2] = match_up.loc[army1, army2]
                other.single_rates[army2 + " vs " + army1] = match_up.loc[army2, army1]

        self.chance = np.average(self.rates)
        other.chance = np.average(other.rates)


    def print(self):
        result = []
        # result.append("*" * 25)
        result.append("        TEAM " + self.name)
        for player, army in zip(self.players , self.armies):
            result.append(player + (" "*(10-len(player))) + "----->   " + army)
            # result.append("*" * 25)
        return "\n".join(result)

    def report(self):
        result = []
        # result.append("^" * 25)
        result.append("     " + self.name + "  winnig chance --->  " + str(round(self.chance)) + " %")
        # result.append("^" * 25)
        for key, value in self.single_rates.items():
            result.append("{} ---> {} % ".format(key, value))
            # result.append("-" * 25)
        return "\n".join(result)

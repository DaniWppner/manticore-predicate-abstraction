import numpy as np
import pandas as pd
files = ["DefectiveComponentCounter","SimpleMarketplace","RoomThermostat","HelloBlockchain","BasicProvenance"]

eps = 0.5

for name in files:
    with open(name+"Metrics/ConsoleOutput",'r') as file:
        lines = file.readlines()
        level0queries = [(float(almost[0]),almost[1][:-1]) for almost in  [l.split("took ")[1].split(" seconds ") for l in lines if "level 0" in l] ]
        queries = [(almost[0][1:-1],float(almost[1].split(" seconds")[0])) for almost in  [l.split(" took ") for l in lines if "(level" in l] ]        
        dfAll = pd.DataFrame(queries,columns=["Level","Time"])
        dfZero = pd.DataFrame(level0queries,columns=["Time","sat/unsat"])
        only_sat = dfZero.loc[dfZero['sat/unsat'] == "(sat)"]
        only_unsat = dfZero.loc[dfZero['sat/unsat'] == "(unsat)"]
        as_array = only_sat["Time"].values
        as_array_unsat = only_unsat["Time"].values
        big = [x for x in as_array if x > eps]
        big_unsat = [x for x in as_array_unsat if x > eps]
        print ("--"+name)
        '''print (f"sat = {len(as_array)}    unsat = {len(as_array_unsat)}    total = {len(dfZero['sat/unsat'].values)}")
        print (f"Number of greater than {eps} (sat): {len(big)}")
        print (f"Number of greater than {eps} (unsat): {len(big_unsat)}")
        print (f"Max (sat): {np.max(as_array)}")
        print (f"Mean (sat): {np.mean(as_array)}")
        print (f"Max (unsat): {np.max(as_array_unsat)}")
        print (f"Mean (unsat): {np.mean(as_array_unsat)}")'''

        print (list(filter((lambda l : "in total." in l), lines ))[0])
        print (list(filter((lambda l : "high level queries" in l), lines ))[0])
        

        for level in ["0","1.1","1.2","2.1","3"]:
            leveldf = dfAll.loc[dfAll["Level"] == f"level {level}"]["Time"]
            print (f"--- Took {np.sum(leveldf.values)} seconds (level {level})")

        level22lines = [(almost[0],float(almost[1].split(" seconds")[0])) for almost in  [l.split(" took ") for l in lines if "level(2.2)" in l] ]        
        print (f"--- Took {sum(time for (_,time) in level22lines)} seconds (level 2.2)")

        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


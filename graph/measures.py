import numpy as np
import pandas as pd
files = ["DefectiveComponentCounter","SimpleMarketplace","RoomThermostat","HelloBlockchain"]

eps = 0.5

for name in files:
    with open(name+"Metrics/ConsoleOutput",'r') as file:
        lines = file.readlines()
        satchecks = [(float(almost[0]),almost[1][:-1]) for almost in  [l.split("took ")[1].split(" seconds ") for l in lines if "Sat check took" in l] ]        
        df = pd.DataFrame(satchecks,columns=["Time","sat/unsat"])
        only_sat = df.loc[df['sat/unsat'] == "(sat)"]
        only_unsat = df.loc[df['sat/unsat'] == "(unsat)"]
        as_array = only_sat["Time"].values
        as_array_unsat = only_unsat["Time"].values
        big = [x for x in as_array if x > eps]
        big_unsat = [x for x in as_array_unsat if x > eps]
        print ("--"+name)
        print (f"sat = {len(as_array)}    unsat = {len(as_array_unsat)}    total = {len(df['sat/unsat'].values)}")
        print (f"Number of greater than {eps} (sat): {len(big)}")
        print (f"Number of greater than {eps} (unsat): {len(big_unsat)}")
        print (f"Max (sat): {np.max(as_array)}")
        print (f"Mean (sat): {np.mean(as_array)}")
        print (f"Max (unsat): {np.max(as_array_unsat)}")
        print (f"Mean (unsat): {np.mean(as_array_unsat)}")
        print (list(filter((lambda l : "in total." in l), lines ))[0])
        print (f"--- Took {np.sum(as_array) + np.sum(as_array_unsat)} seconds (solver checks)")



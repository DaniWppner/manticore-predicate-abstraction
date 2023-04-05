import numpy as np
import pandas as pd
files = ["DefectiveComponentCounter","SimpleMarketplace","RoomThermostat","HelloBlockchain","BasicProvenance"]

eps = 0.5

print("Directorio a analizar:")
path = input()

for name in files:
    with open(path+name+"Metrics/ConsoleOutput",'r') as file:
        lines = file.readlines()
        queries = [(almost[0][1:-1],float(almost[1].split(" seconds")[0])) for almost in  [l.split(" took ") for l in lines if "(level" in l] ]        
        dfAll = pd.DataFrame(queries,columns=["Level","Time"])
        
        print ("--"+name)
        print(''.join(filter((lambda l : l.startswith("--- ")), lines )))
        

        for level in ["_is_sat_z3_call","solver.can_be_true","state.can_be_true","_getvalue_all_z3_call","_getvalue_all","get_value_in_batch","solve_one_n_batched","3","_getvalue_z3_call"]:
            leveldf = dfAll.loc[dfAll["Level"] == f"level {level}"]["Time"]
            print (f"--- Took {np.sum(leveldf.values)} seconds (level {level})")

        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


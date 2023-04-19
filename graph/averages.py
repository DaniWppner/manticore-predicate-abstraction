import numpy as np
import pandas as pd
#"HelloBlockchain,RoomThermostat"
#files = ["DefectiveComponentCounter","SimpleMarketplace","BasicProvenance"]

eps = 0.5

print("Mode: (solver/accounts)")
mode = input()
assert mode in ("solver","accounts"),  "mode not supported"

solvers = ("Z3","Yices")

def analyze(files,categories):
    with open("averagesOutput"+mode,'w') as output:

        for name in files:
            print ("--"+name)
            for category in categories:
                print(category)
                totalTimes = []
                queryTImes = []
                dfs = []
                for i in range(5):  
                    with open(f"{category}Averages/{name}Metrics{i}/ConsoleOutput",'r') as file:
                        lines = file.readlines()
                        #parseando nuestros archivos que sabemos como estan escritos
                        almostTotal = [l.split("Took ") for l in lines if l.startswith("--- Took")]
                        almostHighLevel = [l.split("which took ") for l in lines if "high level queries" in l]
                        totalTimes.append(float(almostTotal[0][1].split(" seconds")[0]))
                        queryTImes.append(float(almostHighLevel[0][1].split(" seconds")[0]))

                        queries = [(almost[0][1:-1],float(almost[1].split(" seconds")[0])) for almost in  [l.split(" took ") for l in lines if "(level" in l] ]        
                        dfs.append(pd.DataFrame(queries,columns=["Level","Time"]))


                '''for level in ["_is_sat_z3_call","solver.can_be_true","state.can_be_true","_getvalue_all_z3_call","_getvalue_all","get_value_in_batch","solve_one_n_batched","3","_getvalue_z3_call"]:
                    levelTimes = []
                    for i in range(5):
                        dfAll = dfs[i]
                        leveldf = dfAll.loc[dfAll["Level"] == f"level {level}"]["Time"]
                        levelTimes.append(np.sum(leveldf.values))
                    print (f"--- Took {np.average(levelTimes)} seconds (level {level}) on average.")#     (standard deviation: {np.std(levelTimes)})")
                    #print (f"        min: {np.min(levelTimes)}      max: {np.max(levelTimes)}\n") '''       

                print(f"Total time average: {np.mean(totalTimes)}    (standard deviation: {np.std(totalTimes)})")
                print(f"        min: {np.min(totalTimes)}      max: {np.max(totalTimes)}\n")
                print(f"Total query time average: {np.mean(queryTImes)}    (standard deviation: {np.std(queryTImes)})")
                print(f"        min: {np.min(queryTImes)}      max: {np.max(queryTImes)}\n")
                print(f"{name}{category} \n {totalTimes}    (total times) \n {queryTImes}    (query times)",file=output)
            print("###################################")



if(mode == "solver"):
    print("Number of accounts (3 or 2):")
    numberOfaccounts = input()
    assert numberOfaccounts in ["3","2"]
    mode += numberOfaccounts + "Accounts"
    if numberOfaccounts == "3":
        files = ["DefectiveComponentCounter","SimpleMarketplace","BasicProvenance"]
        analyze(files,solvers)
    elif numberOfaccounts == "2":
        files = ["DefectiveComponentCounter","SimpleMarketplace","BasicProvenance","RoomThermostat"]
        analyze(files,("TwoAccountsZ3","TwoAccountsYices"))
    
elif(mode == "accounts"):
    files = ["DefectiveComponentCounter","SimpleMarketplace","BasicProvenance","RoomThermostat"]
    analyze(files,("Z3","TwoAccountsZ3"))

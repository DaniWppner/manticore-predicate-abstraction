import sys,os
up_two_levels = os.path.dirname(os.path.dirname(sys.path[0]))
sys.path.append(up_two_levels)
from state_constrainer_YY import state_constrainer
import time

def repr_state(state):
    text = ""
    for x in state:
        text += "T" if x else "F"
    return text

def transition_name(start,end):
    return repr_state(start)+"--"+repr_state(end)

def allowed_methods(state,methods):
    allowed = set()
    for pre,method in zip(state,methods):
        if pre:
            allowed.add(method)
    return allowed

def states_that_allow(method,states,allmethods):
    allowing = set()
    for state in states:
        if method in allowed_methods(state,allmethods):
            allowing.add(method)
    return allowing

start = time.time()
tchk = state_constrainer("Simple",outputspace="simple_from_py_no_constrain")

states = [[0,0,0], [0,0,1], [0,1,1], [1,0,1], [1,1,1], [0,1,0], [1,1,0], [1,0,0]]
traza = ["count_pre","reach_pre","reset_pre"]
methods = ["count","reachFlag","reset"]
reachable_states = set()
explored = {}
to_explore = {}

tchk.callContractFunction("count_pre")
tchk.callContractFunction("reach_pre")
tchk.callContractFunction ("reset_pre")

for ini_state in states:
    ini_state_count = tchk.generateTestCases(keys=traza,targets=(ini_state),testcaseName=f"STATE_{repr_state(ini_state)}")
    if ini_state_count > 0:
        print(f"found {ini_state_count} testcases that reach {repr_state(ini_state)} initial state")
        reachable_states.add(ini_state)
    else:
        print(f"found no testcases for {repr_state(ini_state)} initial state")

for state in reachable_states:
    for method in allowed_methods(state,methods):

############################################## DO NOT RUN VERY INCOMPLETE #####################################################

v = tchk.manticore.make_symbolic_value()
tchk.working_contract.count(v)

tchk.callContractFunction("count_pre")
tchk.callContractFunction("reach_pre")
tchk.callContractFunction("reset_pre")


states_count_is_allowed = [[1,0,1], [1,1,1], [1,1,0], [1,0,0]]

for ini_state in states_count_is_allowed:
    if ini_state not in reachable_states:
        continue
    else:
        for fin_state in states:
            result = tchk.generateTestCases(keys=traza+traza,targets=(ini_state + fin_state),testcaseName=f"transition{transition_name(ini_state,fin_state)}")
            if(result>0):
                print(f"found {result} testcases for {transition_name(ini_state,fin_state)}")
            else:
                print(f"no testcases for {transition_name(ini_state,fin_state)}")



end = time.time()
print(f"--- Took {end-start} seconds")

tchk.safedelete()

sys.exit()
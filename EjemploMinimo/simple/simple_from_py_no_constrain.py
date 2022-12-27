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
            allowing.add(state)
    return allowing

def explorable_from_states(states,methods):
    explorable = set()
    for state in states:
        for method in allowed_methods(state,methods):
            explorable.add((state,method))
    return explorable

start = time.time()
tchk = state_constrainer("Simple",outputspace="simple_from_py_programatic")

states = [(0,0,0), (0,0,1), (0,1,1), (1,0,1), (1,1,1), (0,1,0), (1,1,0), (1,0,0)]
traza = ["count_pre","reach_pre","reset_pre"]
methods = ["count","reachFlag","reset"]

reachable_states = set()
current_states = set()
explored = set()
global_snapshots_stack = []

for condition in traza:
    tchk.callContractFunction(condition)

for ini_state in states:
    ini_state_count = tchk.generateTestCases(keys=traza,targets=(ini_state),testcaseName=f"STATE_{repr_state(ini_state)}")
    if ini_state_count > 0:
        print(f"found {ini_state_count} testcases that reach {repr_state(ini_state)} initial state")
        reachable_states.add(ini_state)
    else:
        print(f"found no testcases for {repr_state(ini_state)} initial state")

current_states = list(reachable_states)


while True:
    '''Hace dfs sobre los estados, teniendo que capturar snapshots del estado global cada vez que se ejecuta una transicion, y levantandolas para retroceder'''
    to_explore = explorable_from_states(current_states,methods).difference(explored)
    if len(to_explore) == 0:
        if global_snapshots_stack:
            tchk.manticore.goto_snapshot()
            current_states = global_snapshots_stack.pop()
            continue
        else:
            break
    else:
        state,method = to_explore.pop() #any
        tchk.manticore.take_snapshot()
        global_snapshots_stack.append(current_states)
        tchk.callContractFunction(method)
        for condition in traza:
            tchk.callContractFunction(condition)
        new_states = []
        for ini_state in states_that_allow(method,current_states,methods):
            for fin_state in states:
                result = tchk.generateTestCases(keys=traza+traza,targets=(ini_state + fin_state),testcaseName=f"transition{transition_name(ini_state,fin_state)}")
                if(result>0):
                    print(f"found {result} testcases for {transition_name(ini_state,fin_state)}")
                    new_states.append(fin_state)
                else:
                    print(f"no testcases for {transition_name(ini_state,fin_state)}")
            explored.add((ini_state,method))

        reachable_states.update(new_states)
        current_states = new_states

end = time.time()
print(f"--- Took {end-start} seconds")


print("+++ Reached States:")
for state in reachable_states:
    print(f"      {repr_state(state)}")
print("+++ Explored Transitions:")
for state,method in explored:
    print(f"   from {repr_state(state)} executing {method}")

tchk.safedelete()

sys.exit()
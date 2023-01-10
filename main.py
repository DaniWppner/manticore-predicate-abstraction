import sys,os
#up_two_levels = os.path.dirname(os.path.dirname(sys.path[0]))
#sys.path.append(up_two_levels)
from state_constrainer_YY import state_constrainer
import itertools
import time
from collections import defaultdict
from contextlib import redirect_stdout

def repr_state(state,methods):
    text = ""
    for x,method in zip(state,methods):
        text += '_'+method if x else ""
    if text == "":
        text = "vacio"
    return text

def transition_name(start,method,end,allmethods):
    return repr_state(start,allmethods)+"-->"+method+"-->"+repr_state(end,allmethods)

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

def write_epa(epa,states,path,allmethods):
    with open(path+"/epa.txt",'w') as output:
        output.write("digraph { \n")
        output.write("init [label=init] \n")
        for state in states:
            output.write(f"{repr_state(state,allmethods)} [label={repr_state(state,allmethods)}] \n")
        for fin_state in epa["ini"]:
            output.write(f"init -> {repr_state(fin_state,allmethods)} [label=constructor] \n")
        for state in states:
            for method in allmethods:
                for fin_state in epa[state,method]:
                    output.write(f"{repr_state(state,allmethods)} -> {repr_state(fin_state,allmethods)} [label={method}] \n")
        output.write("}")

def construct_epa(path,output):
    with open(output+"/ConsoleOutput.txt",'w') as f:
        with redirect_stdout(f):
            start = time.time()
            tchk = state_constrainer(path,outputspace=output)

            deploy_time = time.time()

            traza = tchk.precon_names
            states = list(itertools.product([0,1],repeat=len(traza)))
            methods = []
            for condition in traza:
                methods.append(next(m for m in tchk.contractfunc_names if m==condition.replace('_precondition','')))

            reachable_states = set()
            current_states = set()
            explored = set()
            global_snapshots_stack = []
            epa = defaultdict(list)

            for condition in traza:
                tchk.callContractFunction(condition,tx_sender=tchk.witness_account)

            for ini_state in states:
                ini_state_count = tchk.generateTestCases(keys=traza,targets=(ini_state),testcaseName=f"STATE_{repr_state(ini_state,methods)}")
                if ini_state_count > 0:
                    print(f"found {ini_state_count} testcases that reach {repr_state(ini_state,methods)} initial state")
                    reachable_states.add(ini_state)
                    epa["ini"].append(ini_state)
                else:
                    print(f"found no testcases for {repr_state(ini_state,methods)} initial state")

            ini_states_time = time.time()

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
                    _state,method = to_explore.pop() #any
                    tchk.manticore.take_snapshot()
                    global_snapshots_stack.append(current_states)
                    tchk.callContractFunction(method)
                    

                    if not tchk.isallive():
                        #If trying to execute the method killed all states we should avoid executing anything else.
                        #Go back to before executing and mark this path as already explored. 
                        for ini_state in states_that_allow(method,current_states,methods):
                            explored.add((ini_state,method))
                        current_states = global_snapshots_stack.pop()
                        tchk.manticore.goto_snapshot()
                    else:
                        for condition in traza:
                            tchk.callContractFunction(condition,tx_sender=tchk.witness_account)
                        
                        new_states = []
                        for ini_state in states_that_allow(method,current_states,methods):
                            for fin_state in states:
                                result = tchk.generateTestCases(keys=traza+traza,targets=(ini_state + fin_state),testcaseName=f"transition{transition_name(ini_state,method,fin_state,methods)}")
                                if(result>0):
                                    print(f"found {result} testcases for {transition_name(ini_state,method,fin_state,methods)}")
                                    new_states.append(fin_state)
                                    epa[(ini_state,method)].append(fin_state)
                                else:
                                    print(f"no testcases for {transition_name(ini_state,method,fin_state,methods)}")
                            explored.add((ini_state,method))

                        reachable_states.update(new_states)
                        current_states = new_states

            end = time.time()
            print(f"--- Took {deploy_time-start} seconds to deploy the contract")
            print(f"--- Took {ini_states_time-deploy_time} seconds to find the initial states")
            print(f"--- Took {end-start} seconds in total.")

            print("+++ Reached States:")
            for state in reachable_states:
                print(f"      {repr_state(state,methods)}")
            print("+++ Explored Transitions:")
            for state,method in explored:
                print(f"   from {repr_state(state,methods)} executing {method}")

            write_epa(epa=epa,states=reachable_states,path=output,allmethods=methods)

            tchk.safedelete()


#print("Contract to analyze")
#path = input()
#print("Desired path to output")
#output = input()

#construct_epa(path,output)
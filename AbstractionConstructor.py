from state_constrainer_YY import state_constrainer
import itertools
import time
from collections import defaultdict
from contextlib import redirect_stdout


class abstraction_constructor:
    def __init__(self,path,output,advanceBlocks=False):
        self.path = path
        self.output = output
        self.tchk = state_constrainer(self.path,outputspace=self.output)
        self.advanceBlocks = advanceBlocks
        self.__init_states_and_methods__()

    def __init_states_and_methods__(self):
        raise NotImplementedError       

    def construct_abstraction(self):
        with open(self.output+"/ConsoleOutput.txt",'w') as f:
            with redirect_stdout(f):
                start = time.time()

                reachable_states = set()
                current_states = set()
                explored = set()
                global_snapshots_stack = []
                epa = defaultdict(list)
 
                self.check_preconditions()
                check_preconditions_time = time.time()

                for ini_state in self.states:
                    ini_state_count = self.tchk.generateTestCases(keys=self.traza,targets=(ini_state),testcaseName=f"STATE_{self.repr_state(ini_state)}")
                    if ini_state_count > 0:
                        print(f"found {ini_state_count} testcases that reach {self.repr_state(ini_state)} initial state")
                        reachable_states.add(ini_state)
                        epa["ini"].append(ini_state)
                    else:
                        print(f"found no testcases for {self.repr_state(ini_state)} initial state")

                ini_states_time = time.time()

                current_states = list(reachable_states)

                while True:
                    '''Hace dfs sobre los estados, teniendo que capturar snapshots del estado global cada vez que se ejecuta una transicion, y levantandolas para retroceder'''
                    to_explore = self.explorable_from_states(current_states).difference(explored)
                    if len(to_explore) == 0:
                        if global_snapshots_stack:
                            self.tchk.goto_snapshot()
                            current_states = global_snapshots_stack.pop()
                            continue
                        else:
                            break
                    else:
                        _state,method = to_explore.pop() #will loop through all the states anyways
                        self.tchk.take_snapshot()
                        global_snapshots_stack.append(current_states)
                        self.tchk.callContractFunction(method)
                        print(f"# -- Calling {method}")
                        if (self.advanceBlocks):
                            self.tchk.advance_symbolic_ammount_of_blocks()
                        

                        if not self.tchk.isallive():
                            #If trying to execute the method killed all states we should avoid executing anything else.
                            #Go back to before executing and mark this path as already explored. 
                            for ini_state in self.states_that_allow(method,current_states):
                                explored.add((ini_state,method))
                            current_states = global_snapshots_stack.pop()
                            self.tchk.manticore.goto_snapshot()
                        else:
                            self.check_preconditions()
                            
                            new_states = []
                            ini_result_states_time = time.time()
                            for ini_state in self.states_that_allow(method,current_states):
                                if (ini_state,method) not in explored:
                                    for fin_state in self.states:
                                        result = self.tchk.generateTestCases(keys=(self.traza+self.traza),targets=(ini_state + fin_state),testcaseName=f"transition{self.transition_name(ini_state,method,fin_state)}")
                                        if(result>0):
                                            print(f"found {result} testcases for {self.transition_name(ini_state,method,fin_state)}")
                                            new_states.append(fin_state)
                                            epa[(ini_state,method)].append(fin_state)
                                        else:
                                            print(f"no testcases for {self.transition_name(ini_state,method,fin_state)}")
                                    explored.add((ini_state,method))
                            end_result_states_time = time.time()
                            print(f"--- Took {end_result_states_time-ini_result_states_time} seconds to explore the transitions executing {method}")

                            reachable_states.update(new_states)
                            current_states = new_states

                end = time.time()
                print(f"--- Took {check_preconditions_time-start} seconds to execute the preconditions for the first time")
                print(f"--- Took {ini_states_time-start} seconds to find the initial states")
                print(f"--- Took {end-start} seconds in total.")

                print("+++ Reached States:")
                for state in reachable_states:
                    print(f"      {self.repr_state(state)}")
                print("+++ Explored Transitions:")
                for state,method in explored:
                    print(f"   from {self.repr_state(state)} executing {method}")

                self.write_epa(epa,reachable_states)

                self.tchk.safedelete()

    def check_preconditions(self):
        for condition in self.traza:
            self.tchk.callContractFunction(condition,tx_sender=self.tchk.witness_account)


    def repr_state(self,state):
        raise NotImplementedError

    def transition_name(self,start,method,end):
        raise NotImplementedError

    def allowed_methods(self,state):
        raise NotImplementedError

    def states_that_allow(self,method,current_states):
        raise NotImplementedError

    def explorable_from_states(self,states):
        raise NotImplementedError

    def write_epa(self,epa,reachable_states):
        raise NotImplementedError


class epa_constructor(abstraction_constructor):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def __init_states_and_methods__(self): 
        self.traza = self.tchk.precon_names
        self.states = list(itertools.product([0,1],repeat=len(self.traza)))
        self.methods = []
        for condition in self.traza:
            self.methods.append(next(m for m in self.tchk.contractfunc_names if m==condition.replace('_precondition','')))

    def repr_state(self,state):
        text = ""
        for x,method in zip(state,self.methods):
            text += '_'+method if x else ""
        if text == "":
            text = "vacio"
        return text

    def transition_name(self,start,method,end):
        return self.repr_state(start)+"-->"+method+"-->"+self.repr_state(end)

    def allowed_methods(self,state):
        allowed = set()
        for pre,method in zip(state,self.methods):
            if pre:
                allowed.add(method)
        return allowed

    def states_that_allow(self,method,current_states):
        allowing = set()
        for state in current_states:
            if method in self.allowed_methods(state):
                allowing.add(state)
        return allowing

    def explorable_from_states(self,states):
        explorable = set()
        for state in states:
            for method in self.allowed_methods(state):
                explorable.add((state,method))
        return explorable

    def write_epa(self,epa,reachable_states):
        with open(self.output+"/epa.txt",'w') as output:
            output.write("digraph { \n")
            output.write("init [label=init] \n")
            for state in reachable_states:
                output.write(f"{self.repr_state(state)} [label={self.repr_state(state)}] \n")
            for fin_state in epa["ini"]:
                output.write(f"init -> {self.repr_state(fin_state)} [label=constructor] \n")
            for state in reachable_states:
                for method in self.methods:
                    for fin_state in epa[state,method]:
                        output.write(f"{self.repr_state(state)} -> {self.repr_state(fin_state)} [label={method}] \n")
            output.write("}")
           
class state_abstraction_constructor(abstraction_constructor):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def __init_states_and_methods__(self): 
        self.enumdir = self.tchk.getEnumInfo()
        self.traza = list(self.enumdir.keys())
        #Cuando un contrato de solidity returnea Enum en realidad devuelve un uint8.
        enumReturnValues = list(map(lambda container : list(range(len(container))) ,self.enumdir.values()))
        self.states = list(itertools.product(*enumReturnValues))
        self.methods = []
        #Esto no está necesariamente bien? Dice que los metodos a considerar son los que tengan una precondicion explicita en el contrato.
        for condition in self.tchk.precon_names:
            self.methods.append(next(m for m in self.tchk.contractfunc_names if m==condition.replace('_precondition','')))

    def repr_state(self,state):
        text = ""
        for enumIndex,enumVar in zip(state,self.traza):
            text += (self.enumdir[enumVar])[enumIndex]
        return text

    def transition_name(self,start,method,end):
        return self.repr_state(start)+"-->"+method+"-->"+self.repr_state(end)

    def allowed_methods(self,state):
        return set(self.methods)

    def states_that_allow(self,method,current_states):
        return set(current_states)

    def explorable_from_states(self,states):
        explorable = set()
        for state in states:
            for method in self.methods:
                explorable.add((state,method))
        return explorable

    def write_epa(self,epa,reachable_states):
        with open(self.output+"/states.txt",'w') as output:
            output.write("digraph { \n")
            output.write("init [label=init] \n")
            for state in reachable_states:
                output.write(f"{self.repr_state(state)} [label={self.repr_state(state)}] \n")
            for fin_state in epa["ini"]:
                output.write(f"init -> {self.repr_state(fin_state)} [label=constructor] \n")
            for state in reachable_states:
                for method in self.methods:
                    for fin_state in epa[state,method]:
                        output.write(f"{self.repr_state(state)} -> {self.repr_state(fin_state)} [label={method}] \n")
            output.write("}")
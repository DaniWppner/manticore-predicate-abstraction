from state_constrainer_YY import state_constrainer
import itertools
import time
from collections import defaultdict
from contextlib import redirect_stdout
from pathlib import Path
import numpy as np


class epa_classic_constructor:
    def __init__(self,path,output,advanceBlocks=False):
        self.path = path
        self.output = output
        Path(output).mkdir(parents=True, exist_ok=True)
        self.manticore_handler = state_constrainer(self.path,outputspace=self.output)
        self.advanceBlocks = advanceBlocks
        self.__init_states_and_methods__()

    def __init_states_and_methods__(self): 
        self.traza = self.manticore_handler.precon_names
        self.states = list(itertools.product([0,1],repeat=len(self.traza)))
        self.methods = []
        for condition in self.traza:
            for m in self.manticore_handler.contractfunc_names:
                if m==condition.replace('_precondition',''):
                    self.methods.append(m)


    def construct_abstraction(self):
        with open(self.output+"/ConsoleOutput",'w') as f:
            with redirect_stdout(f):
                start = time.time()

                method_times = []
                precondition_times = []
                query_times = []

                self.__construct_abstraction(method_times, precondition_times, query_times)

                end = time.time()
                print(f"--- We executed the preconditions {len(precondition_times)} times, which took {sum(precondition_times)} seconds to execute, {np.mean(precondition_times)} on average (min={np.min(precondition_times)} max={np.max(precondition_times)})")
                print(f"--- We executed a method {len(method_times)} times, which took {sum(method_times)} seconds, {np.mean(method_times)} seconds on average (min={np.min(method_times)} max={np.max(method_times)})")
                print(f"--- We did {len(query_times)} high level queries, which took {sum(query_times)} seconds, {np.mean(query_times)} seconds on average (min={np.min(query_times)} max={np.max(query_times)})")
                print(f"--- Took {end-start} seconds in total.")

                print("+++ Reached States:")
                for state in self.reachable_states:
                    print(f"      {self.repr_state(state)}")
                print("+++ Explored Transitions:")
                for state,method in self.explored:
                    print(f"   from {self.repr_state(state)} executing {method}")

                self.write_epa(self.reachable_states)

                self.manticore_handler.safedelete()

    def __construct_abstraction(self, method_times, precondition_times, query_times):

        self.reachable_states = set()
        self.explored = set()
        self.epa = defaultdict(list)

        check_preconditions_time_init = time.time()
        self.check_preconditions()
        check_preconditions_time_fin = time.time()
        precondition_times.append(check_preconditions_time_fin-check_preconditions_time_init)
                
        #preguntar cuales son los estados iniciales
        ini_states_time_start = time.time()
        self.query_reached_states(ini_state,"init")
        for ini_state in self.states:
            ini_state_count = self.manticore_handler.generateTestCases(keys=self.traza,targets=(ini_state),testcaseName=f"STATE_{self.repr_state(ini_state)}")
            if ini_state_count > 0:
                print(f"found {ini_state_count} testcases that reach {self.repr_state(ini_state)} initial state")
                self.reachable_states.add(ini_state)
                self.epa["ini"].append(ini_state)
            else:
                print(f"found no testcases for {self.repr_state(ini_state)} initial state")
        ini_states_time_end = time.time()
        query_times.append(ini_states_time_end-ini_states_time_start)


        self.manticore_handler.callContractFunction("setter")
        if self.advanceBlocks:
                    #self.manticore_handler.setSymbolicBlock() 
            raise NotImplementedError
        self.manticore_handler.constrainTo("invariant",True)
        self.check_preconditions()

        to_explore = self.explorable_from_states(self.reachable_states).difference(self.explored)
        while len(to_explore) > 0:
            '''Hace bfs sobre los estados, captura un snapshot antes de cada método y retrocede al estado del setter global'''
            _,method = to_explore.pop() #will loop through all the states anyways
                    
            self.manticore_handler.take_snapshot()
            method_execution_time_ini = time.time()

            print(f"# -- Calling {method}")
            self.manticore_handler.callContractFunction(method)

            method_execution_time_fin = time.time()
            method_times.append(method_execution_time_fin-method_execution_time_ini)

            if not self.manticore_handler.isallive():
                        #If trying to execute the method killed all states we should avoid executing anything else.
                        #Go back to before executing and mark this path as already explored. 
                for state in self.states_that_allow(method,self.reachable_states):
                    self.explored.add((state,method))
                self.manticore_handler.goto_snapshot()
            else:
                if (self.advanceBlocks):
                    self.manticore_handler.advance_symbolic_ammount_of_blocks()

                check_preconditions_time_init = time.time()
                        
                self.check_preconditions()
                        
                check_preconditions_time_fin = time.time()
                precondition_times.append(check_preconditions_time_fin-check_preconditions_time_init)

                for ini_state in self.states_that_allow(method,self.reachable_states):
                    if (ini_state,method) not in self.explored:
                        query_start = time.time()
                        self.query_reached_states(ini_state, method)
                        query_times.append(time.time() - query_start)

            self.manticore_handler.goto_snapshot()

    def query_reached_states(self, ini_state, method):
        for fin_state in self.states:
            result = self.manticore_handler.generateTestCases(keys=(self.traza+self.traza),targets=(ini_state + fin_state),testcaseName=f"transition{self.transition_name(ini_state,method,fin_state)}")
            if(result>0):
                print(f"found {result} testcases for {self.transition_name(ini_state,method,fin_state)}")
                self.reachable_states.add(fin_state)
                self.epa[(ini_state,method)].append(fin_state)
            else:
                print(f"no testcases for {self.transition_name(ini_state,method,fin_state)}")

        self.explored.add((ini_state,method))

    def check_preconditions(self):
        for condition in self.traza:
            self.manticore_handler.callContractFunction(condition,tx_sender=self.manticore_handler.witness_account)
        #self.manticore_handler.callContractFunction("blockNumber")

    def repr_state(self,state):
        text = ""
        for x,cond in zip(state,self.traza):
            method = cond.replace('_precondition','')
            if method == "tau": ##no queremos que aparezca en la descripción de los estados
                continue
            else:
                text += '_'+method if x else ""
        if text == "":
            text = "vacio"
        return text
    
#    def short_repr_state(self,state):
#        return state

    def transition_name(self,start,method,end):
        return self.repr_state(start)+"-->"+method+"-->"+self.repr_state(end)
        #return self.short_repr_state(start)+"-->"+method+"-->"+self.short_repr_state(end)


    def allowed_methods(self,state):
        allowed = set()
        for pre,cond in zip(state,self.traza):
            if pre:
                for m in self.methods:
                    if m == cond.replace('_precondition',''):
                        allowed.add(m)
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

    def write_epa(self,reachable_states):
        with open(self.output+"/epa.txt",'w') as output:
            output.write("digraph { \n")
            output.write("init [label=init] \n")
            for state in reachable_states:
                output.write(f"{self.repr_state(state)} [label={self.repr_state(state)}] \n")
            for fin_state in self.epa["ini"]:
                output.write(f"init -> {self.repr_state(fin_state)} [label=constructor] \n")
            for state in reachable_states:
                for method in self.methods:
                    for fin_state in self.epa[state,method]:
                        output.write(f"{self.repr_state(state)} -> {self.repr_state(fin_state)} [label={method}] \n")
            output.write("}")          
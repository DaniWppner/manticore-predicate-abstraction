from manticore.ethereum import ABI
from manticore.core.smtlib import expression
from manticore.core.smtlib import operators
from transition_checkerXX import transition_checkerXX

class state_constrainer(transition_checkerXX):
    def callContractFunction(self,func_name,call_args=None,tx_value=None,tx_sender=None):
        func_id = self.nameToSelector[func_name]

        print(f"# -- Calling {func_name}")

        call_args, tx_value, tx_sender = self.make_transaction_parameters(func_id, call_args, tx_value, tx_sender)
    
        #__getattr__ is overriden to construct the function object.
        fun = getattr(self.working_contract,func_name)
        fun(*call_args,value=tx_value,caller=tx_sender)


    def constrainTo(self,func_name,expectedResult):
        self.callContractFunction(func_name)
        func_id = self.nameToSelector[func_name]

        for state in self.manticore.ready_states:
            tx = state.platform.last_human_transaction
            if(tx.data[:4] == func_id):
                result = self.result_of_tx(tx,func_id)
                assert result is not None
                #Constrain for each state
                print(f"# -- Constrain {func_name} in state #{state.id} to {repr(expectedResult)}")
                if isinstance(expectedResult,int):
                    expectedResult = expression.BitVecConstant(size=result.size,value=expectedResult)
                state.constrain(result==expectedResult)

    def generateTestCases(self,keys=None,targets=None,testcaseName="user"):
        '''generate testcases for each state where the function in keys has the result in targets'''
        count = 0
        func_ids = list(map(lambda name : self.nameToSelector[name],keys))
        for state in self.manticore.ready_states:        
            #find the result of each function in func_ids
            results = []
            temp = func_ids.copy()
            #human_transactions is in chronological order
            for tx in reversed(state.platform.human_transactions):
                if not temp:
                    break    
                if tx.data[:4] == temp[-1]:
                    results.append(self.result_of_tx(tx,temp[-1]))
                    temp.pop()
            results = list(reversed(results))

            #generate condition to be tested
            condition = expression.BoolConstant(value=True)
            for data,target in zip (results,targets):
                if isinstance(target,int):
                    target = expression.BitVecConstant(size=data.size,value=target)                
                condition = operators.AND(condition,data == target)
            
            can_be_true = state.can_be_true(condition)
            if can_be_true:
                count += 1
                with state as temp_state:
                    temp_state.constrain(condition)
                    self.manticore.generate_testcase(state=temp_state,name=testcaseName+f"_{count}")

                    #Also generate concrete values for variables that aren't included in transactions
                    to_concretize = list(self.symbolic_blockchain_vars)
                    values = temp_state.solve_one_n_batched(to_concretize)
                    #FIXME Even though temp_state is supposed to be a CoW version of state, both share the reference to the "context" attribute.
                    #This makes it so when the variables in "to_concretize" are migrated into "temp_state"'s set of constraints, 
                    # the name of the variables remains in the original state's map, even though the reference to the variables themselves is properly deleted.  
                    migration_map = temp_state.context.get("migration_map")
                    print(f"Testcase -- {count}")
                    for concrete,symbolic in zip(values,to_concretize):
                        print(f"-Concrete value for {symbolic.name} : {concrete}")
                        del migration_map[symbolic.name]
                    temp_state.context["migration_map"] = migration_map
                        
        return count

    def result_of_tx(self,transaction,func_id):
        if transaction.return_value == 1:
            return_types = self.contract_metadata.get_func_return_types(func_id)
            if (return_types != '()') :
                #FIXME quita los paréntesis a izquierda y derecha del tipo
                return_types = return_types[1:len(return_types)-1]
                result = ABI.deserialize(return_types,transaction.return_data)
                return result
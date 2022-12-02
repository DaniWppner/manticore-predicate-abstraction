from manticore.ethereum import ABI
from manticore.core.smtlib import expression
from manticore.core.smtlib import operators
from collections import defaultdict
from transition_checkerXX import transition_checkerXX

class state_constrainer(transition_checkerXX):
    def _initBlockchain(self):
        super()._initBlockchain()
        self.stateToTransactionResults = defaultdict(dict)

    def callContractFunction(self,func_name,call_args=None,tx_value=None,tx_sender=None):
        func_id = self.nameToSelector[func_name]
        print(f"# -- Calling {func_name}")

        call_args, tx_value, tx_sender = self.make_transaction_parameters(func_id, call_args, tx_value, tx_sender)
    
        #__getattr__ is overriden to construct the function object.
        fun = getattr(self.working_contract,func_name)
        fun(args=call_args,value=tx_value,caller=tx_sender)

        #Get the result of the most recent transaction
        for state in self.manticore.all_states:
            tx = state.platform.last_human_transaction
            if(func_id == tx.data[:4]):
                if tx.return_value == 1:
                    return_types = self.contract_metadata.get_func_return_types(func_id)
                    if (return_types != '()') :
                        #FIXME quita los paréntesis a izquierda y derecha del tipo
                        return_types = return_types[1:len(return_types)-1]
                        result = ABI.deserialize(return_types,tx.return_data)
                    else:
                        result = None
                    self.stateToTransactionResults[state.id][func_name] = result
                else:
                    self.stateToTransactionResults[state.id][func_name] = None

    def constrainTo(self,func_name,expectedResult):
        self.callContractFunction(func_name)
        for state in self.manticore.all_states:
            return_data = self.stateToTransactionResults[state.id][func_name]
            if return_data is not None:
                print(f"# -- Constrain #{state.id} to {repr(expectedResult)}")
                if isinstance(expectedResult,int):
                    expectedResult = expression.BitVecConstant(size=return_data.size,value=expectedResult)
                state.constrain(return_data==expectedResult)

    def generateTestCases(self,keys=None,targets=None,testcaseName="user"):
        '''generate testcases for each state where the function in keys has the result in targets'''
        count = 0
        for state in self.manticore.all_states:
            #generate condition to be tested
            condition = expression.BoolConstant(value=True)
            for key,target in zip (keys,targets):
                data = self.stateToTransactionResults[state.id][key] 
                if isinstance(target,int):
                    target = expression.BitVecConstant(size=data.size,value=target)                
                condition = operators.AND(condition,data == target)
            
            if state.can_be_true(condition):
                count += 1
                with state as temp_state:
                    temp_state.constrain(condition)
                    self.manticore.generate_testcase(state=temp_state,name=testcaseName+f"_{count}")

                    #Also generate concrete values for variables that aren't included in transactions
                    to_concretize = list(self.symbolic_blockchain_vars)
                    values = temp_state.solve_one_n_batched(to_concretize)
                    print(f"State -- {count}")
                    for concrete,symbolic in zip(values,to_concretize):
                        print(f"-Concrete value for {symbolic.name} : {concrete}")
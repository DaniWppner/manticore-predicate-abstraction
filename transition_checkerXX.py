import time
from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import expression
from manticore.core.smtlib.expression import BoolConstant

ETHER = 10**18

class ReachabilityError(Exception):
    pass

def state_is_reachable(machine):
    reachable = False
    for state in machine.all_states:
        reachable = reachable or state.is_feasible()
    if not reachable:
        print(" -- State is impossible")


class transition_checkerXX:
    def __init__(self,url,outputspace=None,workspace=None):
        if outputspace is None:
            outputspace = url + "_results"
        self.manticore = ManticoreEVM(workspace_url=workspace, outputspace_url="fs:"+outputspace)

        self._initUserAndContract(url) 
        self._initContractSelectorsAndMetadata()
        self._initBlockchain()

    def _initUserAndContract(self,url):
        self.owner_account = self.manticore.create_account(balance=1*ETHER)
        print("# -- Deploying Contract")
        with open(url,'r') as file:
            source_code = file.read() 
        #Hardcodeamos args=None para que use argumentos simbolicos por defecto
        self.working_contract = self.manticore.solidity_create_contract(source_code, owner=self.owner_account,args=None) 
        assert(self.working_contract is not None), "Problemas en el creado del contrato"
        print("# -- Contract Deployed")
        
    
    def _initContractSelectorsAndMetadata(self):
        self.nameToSelector = {}
        self.precon_names = []
        self.contractfunc_names = [] 
        self.contract_metadata = self.manticore.get_metadata(self.working_contract)
        
        for func_hsh in self.contract_metadata.function_selectors:
            func_name = self.contract_metadata.get_func_name(func_hsh)
            self.nameToSelector[func_name] = func_hsh
            if ("_precondition" in func_name):
                self.precon_names.append(func_name)
            else:
                self.contractfunc_names.append(func_name)

    def _initBlockchain(self):
        self.symbolic_blockchain_vars = set()
        initial_block= self.manticore.make_symbolic_value(name="initial_block")
        self.symbolic_blockchain_vars.add(initial_block)
        self.manticore.start_block(blocknumber=initial_block,
            timestamp=int(time.time()), # current unix timestamp, #FIXME?
            coinbase=self.owner_account,
            difficulty=0x200,
            gaslimit=0x7FFFFFFF)

    
    def callContractFunction(self,func_name,call_args=None,tx_value=None,tx_sender=None):
        func_id = self.nameToSelector[func_name]
        print(f"# -- Calling {func_name}")

        call_args, tx_value, tx_sender = self.make_transaction_parameters(func_id, call_args, tx_value, tx_sender)
    
        #__getattr__ is overriden to construct the function object.
        fun = getattr(self.working_contract,func_name)
        fun(*call_args,value=tx_value,caller=tx_sender)

        #Get the result of the most recent transaction
        for state in self.manticore.all_states:
            tx = state.platform.last_human_transaction
            if(func_id == tx.data[:4]):
                if tx.return_value == 1:
                    return_types = self.contract_metadata.get_func_return_types(func_id)
                    if (return_types != '()') :
                        #FIXME quita los paréntesis a izquierda y derecha del tipo
                        return_types = return_types[1:len(return_types)-1]
                        return ABI.deserialize(return_types,tx.return_data)
                    else:
                        return None
        raise Exception("No path to termination was found") 

    def make_transaction_parameters(self, func_id, call_args=None, tx_value=None, tx_sender=None):
        # construct the arguments passed to the contract method
        if call_args is None:
            arg_types = self.contract_metadata.get_func_argument_types(func_id)
            call_args = self.manticore.make_symbolic_arguments(arg_types)
    
        # make a symbolic (or zero) value for the transaction
        if tx_value is None:
            if self.contract_metadata.get_abi(func_id)['stateMutability'] == 'payable':
                tx_value = self.manticore.make_symbolic_value()
            else:
                tx_value = 0

        # construct a sender for the transaction
        if tx_sender is None:
            tx_sender = self.manticore.make_symbolic_address()
        return call_args,tx_value,tx_sender


    def constrainTo(self,func_name,expectedResult):
        return_data = self.callContractFunction(func_name)
        assert return_data is not None
        print(f"# -- Constrain to {repr(expectedResult)}")
        if isinstance(expectedResult,int):
            expectedResult = expression.BitVecConstant(size=return_data.size,value=expectedResult)
        self.manticore.constrain(return_data==expectedResult)
        state_is_reachable(self.manticore)
    
    def can_be_true(self,expr):
        count = 0
        for state in self.manticore.all_states:
            if state.can_be_true(expr):
                count += 1
        return count

    def generateTestCases(self,only_if=BoolConstant(value=True),testcaseName="user"):
        count = 0
        for state in self.manticore.all_states:
            if state.can_be_true(only_if):
                count += 1
                with state as temp_state:
                    temp_state.constrain(only_if)
                    self.manticore.generate_testcase(state=temp_state,name=testcaseName+f"_{count}")

                    #Also generate concrete values for variables that aren't included in transactions
                    to_concretize = list(self.symbolic_blockchain_vars)
                    values = temp_state.solve_one_n_batched(to_concretize)
                    print(f"State -- {count}")
                    for concrete,symbolic in zip(values,to_concretize):
                        print(f"-Concrete value for {symbolic.name} : {concrete}")

        return count

    def advance_symbolic_ammount_of_blocks(self):
        ammount = self.manticore.make_symbolic_value(name="blocks_advanced")
        self.symbolic_blockchain_vars.add(ammount)
        for state in self.manticore.all_states:
            world = state.platform
            world.advance_block_number(ammount)
        return ammount

    def safedelete(self):
        self.manticore.kill()
        self.manticore.remove_all()
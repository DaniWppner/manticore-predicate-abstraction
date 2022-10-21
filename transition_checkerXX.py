import time
from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import expression
from manticore.core.smtlib import operators

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
    def __init__(self,url):
        self.machine = ManticoreEVM()

        self._initUserAndContract(url) 
        self._initContractSelectorsAndMetadata()
        self._initBlockchain()

    def _initUserAndContract(self,url):
        self.owner_account = self.machine.create_account(balance=1*ETHER)
        print("# -- Deploying Contract")
        with open(url+".sol",'r') as file:
            source_code = file.read() 
        #Hardcodeamos args=None para que use argumentos simbolicos por defecto
        self.working_contract = self.machine.solidity_create_contract(source_code, owner=self.owner_account,args=None) 
        assert(self.working_contract is not None), "Problemas en el creado del contrato"
        print("# -- Contract Deployed")
        
    
    def _initContractSelectorsAndMetadata(self):
        self.nameToSelector = {}
        self.pred_names = []
        self.contractfunc_names = [] 
        self.contract_metadata = self.machine.get_metadata(self.working_contract)
        
        for func_hsh in self.contract_metadata.function_selectors:
            func_name = self.contract_metadata.get_abi(func_hsh)["name"]
            self.nameToSelector[func_name] = func_hsh
            if ("_predicate" in func_name):
                self.pred_names.append(func_name)
            else:
                self.contractfunc_names.append(func_name)

    def _initBlockchain(self):
        #Initialize blockchain state
                self.machine.start_block(blocknumber=self.machine.make_symbolic_value(),
                    timestamp=int(time.time()), # current unix timestamp, #FIXME?
                    coinbase=self.owner_account,
                    difficulty=0x200,
                    gaslimit=0x7FFFFFFF)

  
    def callContractFunction(self,func_name,call_args=None,tx_value=0,tx_sender=None):
        func_id = self.nameToSelector[func_name]
        print(f"# -- Calling {func_name}")

        call_args, tx_value, tx_sender = self.make_transaction_parameters(func_id, call_args, tx_value, tx_sender)
    
        #__getattr__ is overriden to construct the function object.
        getattr(self.working_contract,func_name)(args=call_args,value=tx_value,caller=tx_sender)

        #Get the result of the most recent transaction
        for state in self.machine.all_states:
            tx = state.platform.human_transactions[-1]
            if(func_id == tx.data[:4]):
                if tx.return_value == 1:
                    return_types = self.contract_metadata.get_func_return_types(func_id)
                    if (return_types != '()') :
                        #FIXME quita los paréntesis a izquierda y derecha del tipo
                        return_types = return_types[1:len(return_types)-1]
                        return ABI.deserialize(return_types,tx.return_data)
                    else:
                        return None
                elif tx.result == "REVERT" or tx.result == "THROW" :
                    print(f"-- reached {tx.result}")
                else:
                    print("-- something else went wrong")
        raise Exception("No path to termination was found") 

    def make_transaction_parameters(self, func_id, call_args=None, tx_value=0, tx_sender=None):
        # construct the arguments passed to the contract method
        if call_args is None:
            arg_types = self.contract_metadata.get_func_argument_types(func_id)
            call_args = self.machine.make_symbolic_arguments(arg_types)
    
        # make a symbolic value for the transaction
        if tx_value=="symbolic":
            tx_value = self.machine.make_symbolic_value()

        # construct a sender for the transaction
        if tx_sender is None:
            tx_sender = self.machine.make_symbolic_address()
        return call_args,tx_value,tx_sender


    def constrainTo(self,func_name,expectedResult):
        return_data = self.callContractFunction(func_name)
        assert return_data is not None
        datasize = return_data.size
        print(f"# -- Constrain to {repr(expectedResult)}")
        if expectedResult is int:
            expectedResult = expression.BitVecConstant(size=datasize,value=expectedResult)
        self.machine.constrain(return_data==expectedResult)
        state_is_reachable(self.machine)
    
    def can_all_be_true(self,expressions):
        can_be_true = False
        expr = self.predicate_expression(expressions)
        for state in self.machine.all_states:
            can_be_true = can_be_true or state.can_be_true(expr)
        return can_be_true


    def evaluate_all_properties(self):
        return_data = []
        for name in self.pred_names:
            return_data.append(self.callContractFunction(name))
        return return_data

    def end_block(self):
        self.machine.end_block()

    def advance_symbolic_ammount_of_blocks(self):
        ammount = self.machine.make_symbolic_value()
        for state in self.machine.all_states:
            world = state.platform
            world.advance_block_number(ammount)

    @staticmethod
    def predicate_expression(expressions):
        expr = expression.BoolConstant(value=True)
        for tmp_expr in expressions:
            expr = operators.AND(expr,tmp_expr)
        return (expr)
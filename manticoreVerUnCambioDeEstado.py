
import time
import sys
from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import expression

class ReachabilityError(Exception):
    pass

def state_is_reachable(machine):
    reachable = False
    for state in machine.all_states:
        reachable = reachable or state.is_feasible()
    if not reachable:
        print(" -- State is impossible")


m = ManticoreEVM(workspace_url="CrowdfundingPredicates_manticore_output")
ETHER = 10**18


#Initialize user and contracts
owner_account = m.create_account(balance=1*ETHER)
print("# -- Deploying Contract")
with open("CrowdfundingPredicates.sol",'r') as file:
    source_code = file.read() 
#Hardcodeamos args=None para que use argumentos simbolicos por defecto
Crowdfunding_contract = m.solidity_create_contract(source_code, owner=owner_account,args=None) 
assert(Crowdfunding_contract is not None), "Problemas en el creado del contrato"
print("# -- Contract Deployed") 

#Initialize blockchain state
current_block = m.make_symbolic_value()
m.start_block(blocknumber=current_block,
            timestamp=int(time.time()), # current unix timestamp, #FIXME?
            coinbase=owner_account,
            difficulty=0x200,
            gaslimit=0x7FFFFFFF)


#Get selectors
nameToSelector = {}
pred_names = []
contractfunc_names = [] 

md = m.get_metadata(Crowdfunding_contract)
for func_hsh in md.function_selectors:
    func_name = md.get_abi(func_hsh)["name"]
    nameToSelector[func_name] = func_hsh
    if ("_predicate" in func_name):
        pred_names.append(func_name)
    else:
        contractfunc_names.append(func_name)

def callContractFunction(func_name,call_args=None,tx_value=0):
    func_id = nameToSelector[func_name]
    print(f"# -- Calling {func_name}")

    # construct the arguments passed to the contract method
    if (call_args is None):
        arg_types = md.get_func_argument_types(func_id)
        call_args = m.make_symbolic_arguments(arg_types)

    # make a symbolic value for the transaction
    if tx_value=="symbolic":
        tx_value = m.make_symbolic_value()
        print("- Calling with symbolic transaction value")
  
    #__getattr__ is overriden to construct the function object.
    Crowdfunding_contract.__getattr__(func_name)(args=call_args,value=tx_value)

    #Find the result in the most recent transaction
    for state in m.all_states:
        tx = state.platform.human_transactions[-1]
        if(func_id == tx.data[:4]):
            assert tx.return_value == 1
            return_types = md.get_func_return_types(func_id)
            if (return_types != '()') :
                #FIXME quita los paréntesis a izquierda y derecha del tipo
                return_types = return_types[1:-1]
                return ABI.deserialize(return_types,tx.return_data)    



def constrainTo(func_name,expectedResult):
    return_data = callContractFunction(func_name)
    if return_data is not None:
        if (return_data is expression.Constant) or (not expression.issymbolic(return_data)):
            print("Data to constrain is not symbolic, are you sure?")
            print(f"Data : {return_data}")
        datasize = return_data.size
        print(f"# -- Constrain to {repr(expectedResult)}")
        if expectedResult is int:
            expectedResult = expression.BitVecConstant(size=datasize,value=expectedResult)
        m.constrain(return_data==expectedResult)
        state_is_reachable(m)


constrainTo("D_predicate",True)
constrainTo("F_predicate",False)
constrainTo ("C_predicate",False)

callContractFunction("Donate",tx_value="symbolic")
m.end_block()
m.end_block()
m.end_block()
m.end_block()

constrainTo("F_predicate",True)
constrainTo ("C_predicate",False)
constrainTo("D_predicate",False)

sys.exit()
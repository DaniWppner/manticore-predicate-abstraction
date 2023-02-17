import sys
from transition_checkerXX import transition_checkerXX
from manticore.core.smtlib.operators import AND,OR,NOT


tchk = transition_checkerXX("ContractPreconditionsOnSender")
owner = tchk.callContractFunction("owner")
counter = tchk.callContractFunction("counter")
tran_parameters = tchk.make_transaction_parameters(tchk.nameToSelector["countRequiresOwnership"])
tchk.constrainTo("senderIsOwner",True)
new_counter = tchk.callContractFunction("countRequiresOwnership",*tran_parameters)

tchk.generateTestCases(testcaseName="preconditionsOnSender",only_if=[AND(NOT(owner == 0), NOT(new_counter==counter))])

sys.exit()
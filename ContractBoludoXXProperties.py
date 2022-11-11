import sys
from transition_checkerXX import transition_checkerXX
from manticore.core.smtlib import operators


tchk = transition_checkerXX("ContractBoludoXX")

#DELETEME
""" tchk.callContractFunction("count",tx_value="symbolic")
blockNumber1 = tchk.callContractFunction("blockNumber")
balance1 = tchk.callContractFunction("balance")
counter1 = tchk.callContractFunction("counter")
sys.exit() """

#tchk.constrainTo("nextIsBlockNumber",False)
#tchk.constrainTo("isBlockNumber",False)
tchk.constrainTo("twoToBlockNumber",True)

blockNumber1 = tchk.callContractFunction("blockNumber")
#balance1 = tchk.callContractFunction("balance")
#counter1 = tchk.callContractFunction("counter")

tchk.callContractFunction("count")
tchk.advance_symbolic_ammount_of_blocks()

#balance2 = tchk.callContractFunction("balance")
#tchk.constrainTo("reachedGoal",True)
#balance3 = tchk.callContractFunction("balance")
#counter2 = tchk.callContractFunction("counter")
blockNumber2 = tchk.callContractFunction("blockNumber")
#tchk.constrainTo("isBlockNumber",True)
isBlockNumber = tchk.callContractFunction("isBlockNumber")

tchk.generateTestCases(testcaseName="constraining_blocks",only_if=[isBlockNumber==True])

sys.exit()
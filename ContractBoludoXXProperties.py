import sys
from transition_checkerXX import transition_checkerXX
from manticore.core.smtlib import operators


tchk = transition_checkerXX("ContractBoludoXX")

tchk.callContractFunction("count",tx_value="symbolic")

tchk.constrainTo("nextIsBlockNumber",False)
tchk.constrainTo("isBlockNumber",False)
tchk.constrainTo("twoToBlockNumber",True)

blockNumber1 = tchk.callContractFunction("blockNumber")
balance1 = tchk.callContractFunction("balance")
counter1 = tchk.callContractFunction("counter")

tchk.callContractFunction("count",tx_value="symbolic")
blocks = tchk.advance_symbolic_ammount_of_blocks()

balance2 = tchk.callContractFunction("balance")
counter2 = tchk.callContractFunction("counter")
blockNumber2 = tchk.callContractFunction("blockNumber")

isBlockNumber = tchk.callContractFunction("isBlockNumber")

tchk.generateTestCases(testcaseName="viendoBloques",only_if=[isBlockNumber == True],expressions_to_concretize=[blocks,tchk.initial_block])

sys.exit()
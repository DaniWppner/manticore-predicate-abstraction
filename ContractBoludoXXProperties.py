import sys
from transition_checkerXX import transition_checkerXX
from manticore.core.smtlib import operators


tchk = transition_checkerXX("ContractBoludoXX")


tchk.constrainTo("nextIsBlockNumber",False)
tchk.constrainTo("isBlockNumber",False)
tchk.constrainTo("twoToBlockNumber",True)

#blockNumber1 = tchk.callContractFunction("blockNumber")
#balance1 = tchk.callContractFunction("balance")

tchk.callContractFunction("count",tx_value="symbolic")
tchk.advance_symbolic_ammount_of_blocks()

#balance2 = tchk.callContractFunction("balance")
#blockNumber2 = tchk.callContractFunction("blockNumber")

#tchk.constrainTo("balance",balance1)
#balance3 = tchk.machine.make_symbolic_value()
#tchk.machine.constrain(operators.NOT(balance3==balance1))
#tchk.constrainTo("balance",balance3)


#tchk.constrainTo("blockNumber",blockNumber1)
#tchk.constrainTo("blockNumber",blockNumber2)

tchk.constrainTo("isBlockNumber",True)
tchk.constrainTo("nextIsBlockNumber",False)
tchk.constrainTo("twoToBlockNumber",False)

sys.exit()
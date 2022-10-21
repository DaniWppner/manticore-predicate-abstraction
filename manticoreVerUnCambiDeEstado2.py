import sys
from transition_checkerXX import transition_checkerXX

tchk = transition_checkerXX("CrowdfundingPredicates")


tchk.constrainTo("D_predicate",True)
tchk.constrainTo("F_predicate",False)
tchk.constrainTo ("C_predicate",False)

tchk.callContractFunction("Donate",tx_value="symbolic")
tchk.advance_symbolic_ammount_of_blocks()

tchk.constrainTo("D_predicate",False)
#tchk.constrainTo("F_predicate",True)
tchk.constrainTo ("C_1",False)
sys.exit()


tchk.constrainTo("D_predicate",True)
tchk.constrainTo("F_predicate",False)
tchk.constrainTo ("C_predicate",False)

tchk.callContractFunction("Donate",tx_value="symbolic")
tchk.advance_symbolic_ammount_of_blocks()

tchk.constrainTo("D_predicate",False)
tchk.constrainTo("F_predicate",True)
tchk.constrainTo("C_predicate",False)

tchk.constrainTo ("C_2",False)
tchk.constrainTo ("C_3",False)
tchk.constrainTo ("C_1",False)



sys.exit()
import sys
from transition_checkerXX import transition_checkerXX
from manticore.core.smtlib.operators import OR,AND,NOT


tchk = transition_checkerXX("CrowdfundingPredicates")


tchk.constrainTo("D_predicate",True)
tchk.constrainTo("F_predicate",False)
tchk.constrainTo ("C_predicate",False)

tchk.callContractFunction("Donate",tx_value="symbolic")
tchk.advance_symbolic_ammount_of_blocks()

#tchk.constrainTo("D_predicate",False)
#tchk.constrainTo("F_predicate",True)
#tchk.constrainTo ("C_1",False)
#tchk.constrainTo ("C_2",False)
'''
c_1 = tchk.callContractFunction("C_1")
c_2 = tchk.callContractFunction("C_2")
c_3 = tchk.callContractFunction("C_3")

c1_c3 = tchk.can_all_be_true([NOT(AND(c_1==True,c_3==True))],testcaseName="not (c1 and c3)")
c2_c3 = tchk.can_all_be_true([NOT(AND(c_1==True,c_3==True))],testcaseName="not (c2 and c3)")
c3_result = tchk.can_all_be_true([NOT(c_3==True)],testcaseName="not c3")

if(c1_c3):
    print(f"not (C_1 && C_3) can be true")
if(c2_c3):
    print(f"not (C_2 && C_3) can be true")
if(c3_result):
    print(f"not C_3 can be true") 
'''

#tchk.constrainTo("C_3",False)
tchk.constrainTo ("C_1_C_3",True)
#tchk.constrainTo ("notC_1_C_3",True)
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
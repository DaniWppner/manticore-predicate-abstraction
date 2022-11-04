import sys
from transition_checkerXX import transition_checkerXX
from manticore.core.smtlib.operators import OR,AND,NOT


tchk = transition_checkerXX("CrowdfundingPredicates",workspace="Concrete_inputs1")

tchk.constrainTo("D_predicate",True)
tchk.constrainTo("F_predicate",False)
tchk.constrainTo ("C_predicate",False)

tchk.callContractFunction("Donate",tx_value="symbolic")
blocks = tchk.advance_symbolic_ammount_of_blocks()

tchk.constrainTo("D_predicate",False)
#tchk.constrainTo("F_predicate",True)
#tchk.constrainTo("C_predicate",False)


c_1 = tchk.callContractFunction("C_1")
c_2 = tchk.callContractFunction("C_2")
c_3 = tchk.callContractFunction("C_3")
#c1_c2 = tchk.callContractFunction("C_1_C_2")
#c = tchk.callContractFunction("C_prima")

#c1_c2_result = tchk.generateTestCases(only_if=[NOT(AND(c_1==True,c_2==True))],testcaseName="not (c1 and c2)")
#c1_c2_result = tchk.generateTestCases(only_if=[c1_c2 == False],testcaseName="not (c1 and c2)")
c_result = tchk.generateTestCases([NOT(AND(c_1==True,c_2==True,c_3==True))],testcaseName="not c")


if(c_result>0):
    print(f"not C can be true, found {c_result} testcases for it")

sys.exit()

#tchk.constrainTo("C_3",False)
tchk.constrainTo ("C_1_C_2",False)
tchk.constrainTo("C_3",True)
tchk.constrainTo("C_prima",False)
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
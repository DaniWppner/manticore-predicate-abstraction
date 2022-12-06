import sys
from state_constrainer_YY import state_constrainer
from manticore.core.smtlib.expression import BoolConstant



tchk = state_constrainer("CrowdfundingPredicates",outputspace="new constrainer")

tchk.constrainTo("D_predicate",1)
tchk.constrainTo("F_predicate",0)
tchk.constrainTo ("C_predicate",0)

tchk.callContractFunction("Donate")
blocks = tchk.advance_symbolic_ammount_of_blocks()

tchk.constrainTo("D_predicate",0)
tchk.constrainTo("F_predicate",1)
tchk.constrainTo("C_predicate",0)

result1 = tchk.generateTestCases(only_if=BoolConstant(value=True),testcaseName="Transicion")
if(result1>0):
    print(f"found {result1} testcases for it")
else:
    print(":(")
print("\n")

sys.exit()
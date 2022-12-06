import sys

from pyparsing import counted_array
from transition_checkerXX import transition_checkerXX
from manticore.core.smtlib.operators import OR,AND,NOT


transiciones=[]

tchk = transition_checkerXX("CrowdfundingPredicates",outputspace="transicion_hecha_distinta")

tchk.constrainTo("D_predicate",1)
tchk.constrainTo("F_predicate",0)
tchk.constrainTo ("C_predicate",0)

tchk.callContractFunction("Donate")
blocks = tchk.advance_symbolic_ammount_of_blocks()

d = tchk.callContractFunction("D_predicate")
f = tchk.callContractFunction("F_predicate")
c = tchk.callContractFunction("C_predicate")

count = tchk.generateTestCases([d==0,f==1,c==0],testcaseName="transicion_hecha_distinta")
if count>0:
    print(f"transition D!F!C-->!DF!C , found {count} testcases for it")
else:
    print("no testcases found for transition D!F!C-->!DF!C")

sys.exit()
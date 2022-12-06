import sys,os
up_two_levels = os.path.dirname(os.path.dirname(sys.path[0]))
sys.path.append(up_two_levels)
from transition_checkerXX import transition_checkerXX
from manticore.core.smtlib import operators


tchk = transition_checkerXX("Simple",outputspace="simple_from_py_old")

tchk.constrainTo("count_pre",1)
tchk.constrainTo("reach_pre",0)
tchk.constrainTo ("reset_pre",0)

v = tchk.manticore.make_symbolic_value()
tchk.working_contract.count(v)

count_res = tchk.callContractFunction("count_pre")
reach_res = tchk.callContractFunction("reach_pre")
reset_res = tchk.callContractFunction("reset_pre")

condition = operators.AND(count_res==0,reach_res==1,reset_res==0)

result1 = tchk.generateTestCases(only_if=condition,testcaseName=f"transition{1}")
if(result1>0):
    print(f"found {result1} testcases for it")
else:
    print("no testcases")

tchk.safedelete()

sys.exit()
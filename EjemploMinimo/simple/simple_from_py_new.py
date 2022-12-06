import sys
sys.path.append('/home/daniel/BIIC/Pasar de un estado a otro/programaticamente')
from state_constrainer_YY import state_constrainer

tchk = state_constrainer("Simple",outputspace="quicker_simple_from_py")


tchk.constrainTo("count_pre",1)
tchk.constrainTo("reach_pre",0)
tchk.constrainTo ("reset_pre",0)

v = tchk.manticore.make_symbolic_value()
tchk.working_contract.count(v)

tchk.callContractFunction("count_pre")
tchk.callContractFunction("reach_pre")
tchk.callContractFunction("reset_pre")

result1 = tchk.generateTestCases(keys=["count_pre","reach_pre","reset_pre"],targets=[0,1,0],testcaseName=f"transition{1}")
if(result1>0):
    print(f"found {result1} testcases for it")
else:
    print("no testcases")

tchk.safedelete()

sys.exit()

#TODO:
#Traceback (most recent call last):
#  File "simple_from_py_no_constrain.py", line 18, in <module>
#    result1 = tchk.generateTestCases(keys=["count_pre","reach_pre","reset_pre"],targets=[0,1,0],testcaseName=f"transition{1}")
#  File "/home/daniel/BIIC/Pasar de un estado a otro/programaticamente/state_constrainer_YY.py", line 58, in generateTestCases
#    data = self.stateToTransactionResults[state.id][key]
#KeyError: 'count_pre'
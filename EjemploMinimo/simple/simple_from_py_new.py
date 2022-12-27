import sys,os
up_two_levels = os.path.dirname(os.path.dirname(sys.path[0]))
sys.path.append(up_two_levels)
from state_constrainer_YY import state_constrainer

def transition_name(start,end):
    textstart = ""
    textend = ""
    for s,e in zip (start,end):
        textstart += "T" if s else "F"
        textend += "T" if e else "F"
    return textstart+"--"+textend

tchk = state_constrainer("Simple",outputspace="simple_from_py_new")

ini_state = [0,0,1]

tchk.callContractFunction("reachFlag")

tchk.constrainTo("count_pre",ini_state[0])
tchk.constrainTo("reach_pre",ini_state[1])
tchk.constrainTo ("reset_pre",ini_state[2])

tchk.callContractFunction("reset")

tchk.callContractFunction("count_pre")
tchk.callContractFunction("reach_pre")
tchk.callContractFunction("reset_pre")

fin_states = [[0,0,0], [0,0,1], [0,1,1], [1,0,1], [1,1,1], [0,1,0], [1,1,0], [1,0,0]]

for fin_state in fin_states:
    result = tchk.generateTestCases(keys=["count_pre","reach_pre","reset_pre"],targets=fin_state,testcaseName=f"transition{transition_name(ini_state,fin_state)}")
    if(result>0):
        print(f"found {result} testcases for {transition_name(ini_state,fin_state)}")
    else:
        print(f"no testcases for {transition_name(ini_state,fin_state)}")

tchk.safedelete()

sys.exit()
import sys,os
up_one_level = os.path.dirname(sys.path[0])
sys.path.append(up_one_level)
from state_constrainer_YY import state_constrainer

tchk = state_constrainer("Simple.sol",outputspace="ouput",workspace="workspace")

ini_state = [0,0,1]

tchk.callContractFunction("reachFlag")

state = list(tchk.manticore.ready_states)[0]
backupid = int.from_bytes("backup".encode(),'little')
tchk.manticore._save(state,backupid)

tchk.constrainTo("count_pre",ini_state[0])
tchk.constrainTo("count_pre",ini_state[1])
tchk.constrainTo("count_pre",ini_state[2])

tchk.manticore._ready_states.append(backupid)

for state in tchk.manticore.ready_states:
    print(f"--{state.id}")
    print(state.platform.transactions)

tchk.safedelete()
sys.exit()
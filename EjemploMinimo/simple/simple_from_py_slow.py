import sys
sys.path.append('/home/daniel/BIIC/Pasar de un estado a otro/programaticamente')
from state_constrainer_YY import state_constrainer

count=0
for t1,t2,t3 in [(0,1,0),(1,0,0),(0,0,0),(1,1,0),(0,0,1),(1,1,1),(1,0,1),(0,1,1)]:
    print((t1,t2,t3))
    count+=1
    tchk = state_constrainer("Simple",outputspace="simple_from_py")

    tchk.constrainTo("count_pre",1)
    tchk.constrainTo("reach_pre",0)
    tchk.constrainTo ("reset_pre",0)

    v = tchk.manticore.make_symbolic_value()
    tchk.working_contract.count(v)

    tchk.constrainTo("count_pre",t1)
    tchk.constrainTo("reach_pre",t2)
    tchk.constrainTo("reset_pre",t3)

    result1 = tchk.generateTestCases(testcaseName=f"transition{count}")
    if(result1>0):
        print(f"found {result1} testcases for it")
    else:
        print("no testcases")
    tchk.safedelete()

sys.exit()
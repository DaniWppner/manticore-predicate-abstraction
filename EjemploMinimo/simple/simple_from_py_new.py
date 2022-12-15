import sys,os
up_two_levels = os.path.dirname(os.path.dirname(sys.path[0]))
sys.path.append(up_two_levels)
from state_constrainer_YY import state_constrainer

tchk = state_constrainer("Simple",outputspace="simple_from_py_new")


tchk.constrainTo("count_pre",1)
tchk.constrainTo("reach_pre",0)
tchk.constrainTo ("reset_pre",0)

v = tchk.manticore.make_symbolic_value()
tchk.working_contract.count(v)

tchk.callContractFunction("count_pre")
tchk.callContractFunction("reach_pre")
tchk.callContractFunction("reset_pre")

estados_finales = [[0,1,0], [1,0,0], [0,0,0], [1,1,0], [0,0,1], [1,1,1], [1,0,1], [0,1,1]]

for estado in estados_finales:
    result = tchk.generateTestCases(keys=["count_pre","reach_pre","reset_pre"],targets=estado,testcaseName=f"transition{1}")
    if(result>0):
        print(f"found {result} testcases for {estado}")
    else:
        print(f"no testcases for {estado}")

tchk.safedelete()

sys.exit()


#TODO:
#Key error: los estados vivos van cambiando las ids. No existe "count_pre" para el diccionario de los ultimos estados
#Idea: ¿Hacer un plugin de cuando se hace un estado nuevo?
#IMPORTANTE --> chequear que realmente sean  distintas las instancias del resultado para cada estado.
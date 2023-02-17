import sys
from transition_checkerXX import transition_checkerXX
from manticore.core.smtlib.operators import OR,AND,NOT


tchk = transition_checkerXX("CrowdfundingPredicates",outputspace="diff_between_C_y_C-python")

tchk.constrainTo("D_predicate",1)
tchk.constrainTo("F_predicate",0)
tchk.constrainTo ("C_predicate",0)

tchk.callContractFunction("Donate")
blocks = tchk.advance_symbolic_ammount_of_blocks()

tchk.constrainTo("D_predicate",0)
tchk.constrainTo("F_predicate",1)
#tchk.constrainTo("C_predicate",0)


c_1 = tchk.callContractFunction("C_1")
c_2 = tchk.callContractFunction("C_2")
c_3 = tchk.callContractFunction("C_3")
#c1_c2 = tchk.callContractFunction("C_1_C_2")
c = tchk.callContractFunction("C_predicate")
#c_prima = tchk.callContractFunction("C_prima")
c_python = AND(c_1==True,c_2==True,c_3==True)
c = (c == True)

result1 = tchk.generateTestCases([c==c_python],testcaseName="c == c_python")
if(result1>0):
    print(f"C_python can be equal to C, found {result1} testcases for it")
else:
    print("C_python can not be equal to C")
print("\n")

result2 = tchk.generateTestCases([NOT(c==c_python)],testcaseName="not (c == c_python)")
if(result2>0):
    print(f"C_python can be different to C, found {result2} testcases for it")
else:
    print("C_python can not be different to C")
print("\n")

c_result = tchk.generateTestCases([NOT(c)],testcaseName="not c)")
if(c_result>0):
    print(f"C can be False, found {c_result} testcases for it")
else:
    print("C can not be False")
print("\n")

c_python_result = tchk.generateTestCases([NOT(c_python)],testcaseName="not c_python")
if(c_python_result>0):
    print("\n\n")
    print(f"C_python can be False, found {c_python_result} testcases for it")
else:
    print("C_python can not be False")


sys.exit()
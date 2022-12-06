import sys
from transition_checkerXX import transition_checkerXX
from manticore.core.smtlib.operators import OR,AND,NOT

#### NO FUNCIONA ####

def expressions_equal_to(expressions,expected_values):
    expr = (expressions[0]==expected_values[0])
    for curr_expr,expected in zip(expressions[1:],expected_values[1:]):
        expr = AND(a=expr,b=(curr_expr==expected))
    return (expr)


tchk = transition_checkerXX("CrowdfundingPredicates")

d_1, f_1, c_1 = tchk.evaluate_all_properties()

tchk.callContractFunction("Donate",tx_value="symbolic")
tchk.advance_symbolic_ammount_of_blocks()

d_final, f_final, c_final = tchk.evaluate_all_properties()

initial_state = expressions_equal_to([d_1,f_1,c_1],[True,False,False])

final_state1 = expressions_equal_to([d_final,f_final,c_final],[False,True,False])
final_state2 = expressions_equal_to([d_final,f_final,c_final],[True,False,False])
final_state3 = expressions_equal_to([d_final,f_final,c_final],[False,False,False])
final_state4 = expressions_equal_to([d_final,f_final,c_final],[False,False,True])


if(tchk.can_all_be_true([initial_state,final_state1])):
    print("From D & !F & !C to !D & F & !C")
if(tchk.can_all_be_true([initial_state,final_state2])):
    print("From D & !F & !C to D & !F & !C")
if(tchk.can_all_be_true([initial_state,final_state3])):
    print("From D & !F & !C to !D & !F & !C")
if(tchk.can_all_be_true([initial_state,final_state4])):
    print("From D & !F & !C to !D & !F & C")


sys.exit()
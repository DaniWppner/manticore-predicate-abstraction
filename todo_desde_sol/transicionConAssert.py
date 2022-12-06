import sys
from transition_checkerXX import transition_checkerXX
from manticore.core.smtlib.operators import OR,AND,NOT
from manticore.core.smtlib.expression import BoolConstant


tchk = transition_checkerXX("CrowdfundingAssert",outputspace="transicion_hecha_entera_por_codigo")

tchk.callContractFunction("ifEstadoInicialTFFDonate")
blocks = tchk.advance_symbolic_ammount_of_blocks()
tchk.callContractFunction("estadoFinalFTF")
tchk.generateTestCases(only_if=BoolConstant(value=True),testcaseName="TFF--FTF--POSIBLE")

sys.exit()
tchk.machine.kill()
tchk.machine.remove_all()

tchk = transition_checkerXX("CrowdfundingAssert",outputspace="transicion_hecha_entera_por_codigo")

tchk.callContractFunction("ifEstadoInicialTFFDonate")
blocks = tchk.advance_symbolic_ammount_of_blocks()
tchk.callContractFunction("estadoFinalFTT")
tchk.generateTestCases(only_if=BoolConstant(value=True),testcaseName="TFF--FTT--IMPOSIBLE")
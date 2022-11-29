from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import expression
from manticore.core.smtlib import operators

ETHER = 10**18

m = ManticoreEVM(outputspace_url="fs:"+"ResultadosThermostat")
deployer = m.create_account(balance=1*ETHER)

with open("RoomThermostat.sol",'r') as file:
    source_code = file.read() 

#Hardcodeamos args=None para que use argumentos simbolicos por defecto
print("--create contract")
contract = m.solidity_create_contract(source_code,owner=deployer,args=None)
assert(contract is not None), "Problemas en el creado del contrato"

caller_symb = m.make_symbolic_address()
next_caller_symb = m.make_symbolic_address()
print("-- call function")
contract.checkStartThermostatTransition(next_caller_symb,caller=caller_symb)

m.finalize()
from state_constrainer_YY import state_constrainer
import sys
from manticore.ethereum import ABI 
from AbstractionConstructor import state_abstraction_constructor

stateAbsConstructor = state_abstraction_constructor('Contracts/RoomThermostat.sol','graph/RoomThermostatStates')

stateAbsConstructor.construct_abstraction()
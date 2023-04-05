from state_constrainer_YY import state_constrainer
import sys
from manticore.ethereum import ABI 
from AbstractionConstructor import epa_constructor
#corrieron []
#rapidas ["BasicProvenance","DefectiveComponentCounter","SimpleMarketplace","RoomThermostat","HelloBlockchain"]
#lentas ["DigitalLocker","AssetTransfer","FrequentFlyerRewardsCalculator"]
contracts = ["BasicProvenance","DefectiveComponentCounter","SimpleMarketplace","RoomThermostat","HelloBlockchain"]
for contract in contracts:
    print(contract)
    epaCOnst = epa_constructor(f"Contracts/{contract}.sol",f"graph/{contract}Metrics")
    epaCOnst.construct_abstraction()
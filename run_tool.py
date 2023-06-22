from manticore_handler import manticore_handler
import sys
from manticore.ethereum import ABI 
from epa_classic import epa_classic_constructor


#%%%%%%%%%  benchmark 1
'''

#corrieron [["BasicProvenance","DefectiveComponentCounter","SimpleMarketplace","RoomThermostat","HelloBlockchain"]
#rapidas ["BasicProvenance","DefectiveComponentCounter","SimpleMarketplace","RoomThermostat","HelloBlockchain"]
#lentas ["DigitalLocker","AssetTransfer","FrequentFlyerRewardsCalculator"]
contracts = ["DigitalLocker","AssetTransfer","FrequentFlyerRewardsCalculator"]
for contract in contracts:
    for i in range(5):
        print(contract)
        epaCOnst = epa_constructor(f"Contracts/{contract}.sol",f"graph/TwoAccountsYicesAverages/{contract}Metrics{i}")
        epaCOnst.construct_abstraction()

        
'''
#%%%%%%%%%  diferencias contra verisol

'''
epaCrowdFunding = epa_constructor("Scripts/Crowdfunding/CrowdfundingTruco.sol","graph/vs_verisol/CrowdfundingTrucoBalance",advanceBlocks=False)
epaCrowdFunding.construct_abstraction()
'''
#%%%%%%%%   epa classic

epaThermostat = epa_classic_constructor("Contracts/RoomThermostat.sol","graph/epaClassic/RoomThermostat",advanceBlocks=False)
epaThermostat.construct_abstraction()
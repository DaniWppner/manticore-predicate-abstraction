from main import construct_epa
#ya corrieron ["DefectiveComponentCounter","RoomThermostat","HelloBlockchain","SimpleMarketplace"]

for contract in ["FrequentFlyerRewardsCalculator","RefrigeratedTransportation","BasicProvenance","DigitalLocker","AssetTransfer"]:
    print(contract)
    construct_epa(path=f"Contracts/{contract}.sol",output=f"graph/{contract}")
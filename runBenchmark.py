from main import construct_epa
#ya corrieron ["DefectiveComponentCounter","RoomThermostat","HelloBlockchain"]

for contract in ["SimpleMarketplace","FrequentFlyerRewardsCalculator","RefrigeratedTransportation","BasicProvenance","DigitalLocker","AssetTransfer"]:
    print(contract)
    construct_epa(path=f"Contracts/{contract}.sol",output=f"graph/{contract}")
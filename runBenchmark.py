from main import construct_epa

for contract in ["DefectiveComponentCounter","RoomThermostat","HelloBlockchain","DigitalLocker","SimpleMarketPlace","FrequentFlyerRewardsCalculator","RefrigeratedTransportation","BasicProvenance","AssetTransfer"]:
    print(contract)
    construct_epa(path=f"Contracts/{contract}.sol",output=f"graph/{contract}")
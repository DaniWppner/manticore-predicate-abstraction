from AbstractionConstructor import epa_constructor
#ya corrieron ["DefectiveComponentCounter","RoomThermostat","HelloBlockchain","SimpleMarketplace"]

for contract in ["FrequentFlyerRewardsCalculator","RefrigeratedTransportation","BasicProvenance","DigitalLocker","AssetTransfer"]:
    print(contract)
    epaC = epa_constructor(path=f"Contracts/{contract}.sol",output=f"graph/{contract}")
    epaC.construct_abstraction()
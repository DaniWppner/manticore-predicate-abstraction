from manticore.ethereum import ManticoreEVM
ETHER = 10**18
for fun in ["sixth","seventh","eigth"]:
    m = ManticoreEVM(outputspace_url="fs:"+f"Resultados{fun}Transition")
    deployer = m.create_account(balance=1*ETHER)

    with open("Simple.sol",'r') as file:
        source_code = file.read() 

    #Hardcodeamos args=None para que use argumentos simbolicos por defecto
    print("--create contract")
    contract = m.solidity_create_contract(source_code,owner=deployer,args=None)
    assert(contract is not None), "Problemas en el creado del contrato"

    value = m.make_symbolic_value()
    print(f"-- call function")
    f = getattr(contract,fun+"_transition")
    f(value)

    m.finalize()
pragma solidity >=0.4.25 <0.6.0;

contract BasicProvenance {

    //Set of States
    enum StateType { Created, InTransit, Completed}
    
    //List of properties
    StateType public  State;
    address public  InitiatingCounterparty;
    address public  Counterparty;
    address public  PreviousCounterparty;
    address public  SupplyChainOwner;
    address public  SupplyChainObserver;
    
    constructor(address supplyChainOwner, address supplyChainObserver) public
    {
        InitiatingCounterparty = msg.sender;
        Counterparty = InitiatingCounterparty;
        SupplyChainOwner = supplyChainOwner;
        SupplyChainObserver = supplyChainObserver;
        State = StateType.Created;
    }

    function TransferResponsibility(address newCounterparty) public
    {
        if (Counterparty != msg.sender || State == StateType.Completed)
        {
            revert();
        }

        if (State == StateType.Created)
        {
            State = StateType.InTransit;
        }

        PreviousCounterparty = Counterparty;
        Counterparty = newCounterparty;
    }

    function Complete() public
    {
        if (SupplyChainOwner != msg.sender || State == StateType.Completed)
        {
            revert();
        }

        State = StateType.Completed;
        PreviousCounterparty = Counterparty;
        Counterparty = address(0x0000000000000000000000000000000000000000);
    }

    function TransferResponsibility_precondition(address newCounterparty) public returns(bool){
        return (State != StateType.Completed);
    } 
    function Complete_precondition() public returns(bool){
        return (State != StateType.Completed);
    }

    function EnumStateType() public returns(string memory){
        return ("Created,InTransit,Completed");
    }

}
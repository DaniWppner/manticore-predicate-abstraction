pragma solidity >=0.4.25 <0.9.0;

contract AssetTransfer {

    enum StateType { Active, OfferPlaced, PendingInspection, Inspected, Appraised, NotionalAcceptance, BuyerAccepted, SellerAccepted, Accepted, Terminated }
    address public InstanceOwner;
    string public Description;
    uint public AskingPrice;
    StateType public State;

    address public InstanceBuyer;
    uint public OfferPrice;
    address public InstanceInspector;
    address public InstanceAppraiser;

    constructor(string memory description, uint256 price) public
    {
        InstanceOwner = msg.sender;
        AskingPrice = price;
        Description = description;
        State = StateType.Active;
        // ContractCreated();
    }

    function Terminate() public
    {
        if (InstanceOwner != msg.sender)
        {
            revert();
        }

        State = StateType.Terminated;
        // ContractUpdated('Terminate');
    }

    function Modify(string memory description, uint256 price) public
    {
        if (State != StateType.Active)
        {
            revert();
        }
        if (InstanceOwner != msg.sender)
        {
            revert();
        }

        Description = description;
        AskingPrice = price;
        // ContractUpdated('Modify');
    }

    

    function MakeOffer(address inspector, address appraiser, uint256 offerPrice) public
    {
        if (inspector == address(0x0) || appraiser == address(0x0) || offerPrice == 0)
        {
            revert();
        }
        if (State != StateType.Active)
        {
            revert();
        }
        // Cannot enforce "AllowedRoles":["Buyer"] because Role information is unavailable
        if (InstanceOwner == msg.sender) // not expressible in the current specification language
        {
            revert();
        }

        InstanceBuyer = msg.sender;
        InstanceInspector = inspector;
        InstanceAppraiser = appraiser;
        OfferPrice = offerPrice;
        State = StateType.OfferPlaced;
        // ContractUpdated('MakeOffer');
    }

    function AcceptOffer() public
    {
        if (State != StateType.OfferPlaced)
        {
            revert();
        }
        if (InstanceOwner != msg.sender)
        {
            revert();
        }

        State = StateType.PendingInspection;
        // ContractUpdated('AcceptOffer');
    }

    function Reject() public
    {
        if (State != StateType.OfferPlaced && State != StateType.PendingInspection && State != StateType.Inspected && State != StateType.Appraised && State != StateType.NotionalAcceptance && State != StateType.BuyerAccepted)
        {
            revert();
        }
        if (InstanceOwner != msg.sender)
        {
            revert();
        }

        InstanceBuyer = address(0x0);
        State = StateType.Active;
        // ContractUpdated('Reject');
    }

    function Accept() public
    {
        if (msg.sender != InstanceBuyer && msg.sender != InstanceOwner)
        {
            revert();
        }

        if (msg.sender == InstanceOwner &&
            State != StateType.NotionalAcceptance &&
            State != StateType.BuyerAccepted)
        {
            revert();
        }

        if (msg.sender == InstanceBuyer &&
            State != StateType.NotionalAcceptance &&
            State != StateType.SellerAccepted)
        {
            revert();
        }

        if (msg.sender == InstanceBuyer)
        {
            if (State == StateType.NotionalAcceptance)
            {
                State = StateType.BuyerAccepted;
            }
            else if (State == StateType.SellerAccepted)
            {
                State = StateType.Accepted;
            }
        }
        else
        {
            if (State == StateType.NotionalAcceptance)
            {
                State = StateType.SellerAccepted;
            }
            else if (State == StateType.BuyerAccepted)
            {
                State = StateType.Accepted;
            }
        }
        // ContractUpdated('Accept');
    }

    function ModifyOffer(uint256 offerPrice) public
    {
        if (State != StateType.OfferPlaced)
        {
            revert();
        }
        if (InstanceBuyer != msg.sender || offerPrice == 0)
        {
            revert();
        }

        OfferPrice = offerPrice;
        // ContractUpdated('ModifyOffer');
    }

    function RescindOffer() public
    {
        if (State != StateType.OfferPlaced && State != StateType.PendingInspection && State != StateType.Inspected && State != StateType.Appraised && State != StateType.NotionalAcceptance && State != StateType.SellerAccepted)
        {
            revert();
        }
        if (InstanceBuyer != msg.sender)
        {
            revert();
        }

        InstanceBuyer = address(0x0);
        OfferPrice = 0;
        State = StateType.Active;
        // ContractUpdated('RescindOffer');
    }

    function MarkAppraised() public
    {
        if (InstanceAppraiser != msg.sender)
        {
            revert();
        }

        if (State == StateType.PendingInspection)
        {
            State = StateType.Appraised;
        }
        else if (State == StateType.Inspected)
        {
            State = StateType.NotionalAcceptance;
        }
        else
        {
            revert();
        }
        // ContractUpdated('MarkAppraised');
    }

    function MarkInspected() public
    {
        if (InstanceInspector != msg.sender)
        {
            revert();
        }

        if (State == StateType.PendingInspection)
        {
            State = StateType.Inspected;
        }
        else if (State == StateType.Appraised)
        {
            State = StateType.NotionalAcceptance;
        }
        else
        {
            revert();
        }
        // ContractUpdated('MarkInspected');
    }

    function Terminate_precondition() public returns(bool){
        return (true);
    }
    function Modify_precondition() public returns(bool){
        return (State == StateType.Active);
    }
    function MakeOffer_precondition() public returns(bool){
        return (State == StateType.Active);
    }
    function AcceptOffer_precondition() public returns(bool){
        return (State == StateType.OfferPlaced);
    }
    function Reject_precondition() public returns(bool){
        return (State == StateType.OfferPlaced || State == StateType.PendingInspection || State == StateType.Inspected || State == StateType.Appraised && State == StateType.NotionalAcceptance || State == StateType.BuyerAccepted);
    }
    function Accept_precondition() public returns(bool){
        return ((State == StateType.NotionalAcceptance || State == StateType.BuyerAccepted) && (State == StateType.NotionalAcceptance || State == StateType.SellerAccepted));
    }
    function ModifyOffer_precondition(uint256 offerPrice) public returns(bool){
        return (State == StateType.OfferPlaced);
    }
    function RescindOffer_precondition() public returns(bool){
        return (State == StateType.OfferPlaced || State == StateType.PendingInspection || State == StateType.Inspected || State == StateType.Appraised || State == StateType.NotionalAcceptance || State == StateType.SellerAccepted);
    }
    function MarkAppraised_precondition() public returns(bool){
        return (State != StateType.PendingInspection || State != StateType.Inspected);
    }
    function MarkInspected_precondition() public returns(bool){
        return (State != StateType.PendingInspection || State != StateType.Appraised);
    }

    function EnumStateType() public returns(string memory) {
        return ("Active,OfferPlaced,PendingInspection,Inspected,Appraised,NotionalAcceptance,BuyerAccepted,SellerAccepted,Accepted,Terminated"); 
    }
}
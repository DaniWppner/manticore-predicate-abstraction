pragma solidity >=0.4.25 <0.9.0;
pragma experimental ABIEncoderV2;

contract SimpleMarketplace {

    enum StateType { 
      ItemAvailable,
      OfferPlaced,
      Accepted
    }

    address public InstanceOwner;
    string public Description;
    int public AskingPrice;
    StateType public StateEnum;
    int256[][] result;

    address public InstanceBuyer;
    int public OfferPrice;

    constructor(string memory description, int price, address sender) public
    {
        InstanceOwner = sender;
        AskingPrice = price;
        Description = description;
        StateEnum = StateType.ItemAvailable;
    }

    function MakeOffer(int offerPrice) public
    {
        if (offerPrice == 0)
        {
            revert();
        }

        if (StateEnum != StateType.ItemAvailable)
        {
            revert();
        }
        
        if (InstanceOwner == msg.sender)
        {
            revert();
        }

        InstanceBuyer = msg.sender;
        OfferPrice = offerPrice;
        StateEnum = StateType.OfferPlaced;
    }

    function Reject() public
    {
        if ( StateEnum != StateType.OfferPlaced )
        {
            revert();
        }

        if (InstanceOwner != msg.sender)
        {
            revert();
        }

       //InstanceBuyer = 0x0;
        StateEnum = StateType.ItemAvailable;
    }

    function AcceptOffer() public
    {
        if ( StateEnum != StateType.OfferPlaced )
        {
            revert();
        }

        if ( msg.sender != InstanceOwner )
        {
            revert();
        }

        StateEnum = StateType.Accepted;
    }

    function MakeOffer_precondition() public returns(bool){
        return (StateEnum == StateType.ItemAvailable);
    }
    function Reject_precondition() public returns(bool){
        return (StateEnum == StateType.OfferPlaced);
    }
    function AcceptOffer_precondition() public returns(bool){
        return (StateEnum == StateType.OfferPlaced);
    }

    function EnumStateType() public returns(string memory)  { 
      return ("ItemAvailable,OfferPlaced,Accepted");
    }
}
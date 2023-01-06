pragma solidity >=0.4.25 <0.9.0;
pragma experimental ABIEncoderV2;

contract Sender {

    bool public offered;
    bool public accepted;
    address public InstanceOwner;
    address public InstanceBuyer;

    constructor(address sender) public
    {   
        offered = false;
        accepted = false;
        InstanceOwner = sender;
    }

    function MakeOffer() public
    {        
        if (InstanceOwner == msg.sender)
        {
            revert();
        }

        InstanceBuyer = msg.sender;
        offered = true;
    }

    function AcceptOffer() public
    {
        if ( msg.sender != InstanceOwner || !(offered) )
        {
            revert();
        }

        accepted = true;
    }
 
    function Redeem() public
    {
        if (!(accepted))
        {
            revert();
        }
        offered = false;
        InstanceOwner = InstanceBuyer;
    }

    function MakeOffer_precondition() public returns(bool){
        return true;
    }
    function AcceptOffer_precondition() public returns(bool){
        return offered;
    }
    function Redeem_precondition() public returns(bool){
        return accepted;
    }
}
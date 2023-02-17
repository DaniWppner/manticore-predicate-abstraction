// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 < 0.5.0; 

contract PreconditionsOnSender{
    address public owner;
    uint public counter;

    constructor(address _owner, uint _initial_count) {
        owner = _owner;
        counter = _initial_count;
    }

    function countRequiresOwnership() public payable returns(uint){
        if(msg.sender != owner){
            revert();
        }
        counter += 1;
        return counter;
    }

    function senderIsOwner() public payable returns(bool){
        result = (msg.sender == owner)
        address(msg.sender).transfer(msg.value)
        return result
    }

}
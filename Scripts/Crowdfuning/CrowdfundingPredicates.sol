// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 < 0.5.0; 

contract Crowdfunding {
    address owner;
    uint max_block;
    uint goal;

    mapping(address => uint) backers;
    bool funded = false;

    constructor(address _owner, uint _max_block, uint _goal) {
        owner = _owner;
        max_block = _max_block;
        goal = _goal;
    }

    function Donate() public payable {
        if(max_block <= block.number) {
            revert();
        }
        else {
            if(backers[msg.sender] == 0) {
                backers[msg.sender] = msg.value;
            }
            else {
                revert();
            }
        }
    }

    function GetFunds() public {
        if(max_block < block.number && msg.sender == owner) {
            if(goal <= address(this).balance) {
                funded = true;
                owner.transfer(address(this).balance);
            }
            else {
                revert();
            }
        }
        else {
            revert();
        }
    }

    function Claim() public {
        if(block.number <= max_block) {
            revert();
        }
        else {
            if(backers[msg.sender] == 0 || funded || goal <= address(this).balance) {
                revert();
            }
            else {
                uint val = backers[msg.sender];
                backers[msg.sender] = 0;
                (msg.sender).transfer(val);
            }
        }
    }

    function Donate_precondition() public returns (bool){
        return(max_block > block.number);
    }

    function GetFunds_precondition() public returns (bool){
        return(goal <= address(this).balance && max_block < block.number);
    }

    function Claim_precondition() public returns (bool){
       return(block.number > max_block && goal > address(this).balance && !funded);
    }

    function blockNumber() public returns (uint){
        return (block.number);
    }
    
    function balanceGTZero_precondition() public returns (bool){
        return (address(this).balance > 0);
    }



}
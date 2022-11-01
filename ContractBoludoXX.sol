// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 < 0.5.0; 

contract XXX{
    uint target_Block;
    uint public counter;
    uint goal;

    constructor (uint _blockNumber, uint _initial_count, uint _initial_goal) public{
        target_Block = _blockNumber;
        counter = _initial_count;
        goal = _initial_goal;
    }

    function count() public payable returns(uint){
        counter += 1;
        return counter;
    }

    function balance() public view returns(uint){
        return address(this).balance;
    }

    function twoToBlockNumber() public returns(bool){
        return target_Block == block.number + 2;
    }

    function nextIsBlockNumber() public returns(bool){
        return target_Block == block.number + 1;
    }

    function isBlockNumber() public returns(bool){
        return target_Block == block.number;
    }

    function blockNumber() public returns(uint){
        return block.number;
    } 
    
    function reachedGoal() public returns(bool){
        return counter >= goal;
    }

}
// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 < 0.5.0; 

contract XXX{
    uint target_Block;
    uint public counter;

    constructor (uint _blockNumber, uint _initial_count) public{
        target_Block = _blockNumber;
        counter = _initial_count;
    }

    function count() public payable returns(uint){
        counter += 1;
        return counter;
    }

    function balance() public view returns(uint){
        return address(this).balance;
    }

    function nextIsBlockNumber() public view returns(bool){
        return target_Block == block.number + 1;
    }

    function isBlockNumber() public view returns(bool){
        return target_Block == block.number ;
    }

    function blockNumber() public view returns(uint){
        return block.number;
    } 

}
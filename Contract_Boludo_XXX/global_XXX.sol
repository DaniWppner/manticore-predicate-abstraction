// SPDX-License-Identifier: MIT
pragma solidity >=0.8.13;

contract XXX{
    uint target_Block;
    uint counter;

    constructor(uint _blockNumber, uint _initial_count){
        target_Block = _blockNumber;
        counter = _initial_count;
    }

    function count() public returns(uint){
        counter += 1;
        return counter;
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

    function get_counter() public view returns(uint){
        return counter;
    }

}
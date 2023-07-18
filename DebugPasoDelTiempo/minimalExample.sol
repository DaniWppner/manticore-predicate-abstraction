// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 < 0.5.0; 

contract A {
    uint b;

    constructor(uint initial) {
        b = initial;
    }

    function increase_b() public returns (uint){
        require(if_block() == 67);
        b += 1;
        return b;
    }

    function if_block() public returns (uint){
         if(block.number > 10 && block.number < 100){
            return 67;
        }else{
            return 101;
        }
    }
    
    function increase_b_precondition() public returns(bool){
        return if_block() == 67;
    }
}
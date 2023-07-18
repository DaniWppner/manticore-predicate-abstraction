// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 < 0.5.0; 

contract A {
    uint b;

    constructor() {
        b = 3;
    }
    function get_block() public returns (uint){
        return(block.number);
    }

    function if_block() public returns (uint){
        if(block.number > 10){
            return 100;
        }else{
            return 67;
        }
    }

}
//SPDX-License-Identifier: Unlicense
pragma solidity >= 0.4.0 < 0.5.0; 

contract arrayContract {
    uint256 public num;

    constructor() public {
        num = 0;
    }

    function sumArr(uint[5] memory arr) public returns(uint){
        uint sum = 0;
        for(uint i=0;i<arr.length;i++){
            sum += arr[i];
        }
        return sum;
    }

    function undefLengthSumArr(uint[] memory arr) public returns(uint){
        uint sum = 0;
        for(uint i=0;i<arr.length;i++){
            sum += arr[i];
        }
        return sum;
    }
}

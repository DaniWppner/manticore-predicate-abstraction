//SPDX-License-Identifier: Unlicense
pragma solidity >= 0.4.0 < 0.5.0; 

contract arrayContract {
    uint256[10] public sizedArr;
    uint256[] public undefSizeArr;

    constructor() public {
        for(uint i=0;i<sizedArr.length;i++){
            sizedArr[i] = 0;
        }
        undefSizeArr.push(0);
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

    function setArrFor(uint[10] memory arr) public{
        for(uint i=0;i<arr.length;i++){
            sizedArr[i] = arr[i];
        }
    }
    
    function setArrAssign(uint[10] memory arr) public{
        sizedArr = arr;
    }

    function unsizedSetArrFor(uint[] memory arr) public{
        delete undefSizeArr;
        for(uint i=0;i<arr.length;i++){
            undefSizeArr.push(arr[i]);
        }        
    }

    function unsizedSetArrAssign(uint[] memory arr) public{
        undefSizeArr = arr;
    }

}

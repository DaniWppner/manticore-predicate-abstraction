//SPDX-License-Identifier: Unlicense
pragma solidity ^0.5.17;

contract SizedStack {
    uint256 public size;
    uint256 public maxSize;
    uint256[] internal_arr;

    constructor(uint128 _maxSize) public {
        maxSize = _maxSize;
        size = 0;
    }

    function isEmpty() public view returns(bool){
        return size == 0;
    }

    function top() public view returns(uint256){
        require(!isEmpty());
        return internal_arr[size-1];
    }

    function push(uint256 new_elem) public{
        require(size < maxSize);
        internal_arr.push(new_elem);
        size += 1;
    }

    function pop() public returns(uint256){
        require(!isEmpty());
        uint256 was = top();
        internal_arr.pop();
        return was;
    }

    function setter(uint256 sizeNew, uint256 maxSizeNew, uint256[] memory newArr) public {
        size = sizeNew;
        maxSize = maxSizeNew;
        internal_arr = newArr;
    }

    function invariant() public returns(bool){
        bool result = (size >= 0) && (size <= maxSize);
        result = result && (internal_arr.length == size);
        return result;
    }
 
    function push_precondition() public view returns(bool){
        return size < maxSize;
    }
    function pop_precondition() public view returns(bool){
        return !isEmpty();
    } 


}

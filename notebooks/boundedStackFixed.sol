//SPDX-License-Identifier: Unlicense
pragma solidity ^0.6.4;

contract SizedStack {
    uint256 public size;
    uint256 public maxSize;
    uint256[] internal_arr;

    constructor(uint128 _maxSize) public {
        maxSize = _maxSize;
        size = 0;
    }

    function isEmpty() public view returns (bool) {
        return size == 0;
    }

    function top() public view returns (uint256) {
        require(!isEmpty());
        return internal_arr[size - 1];
    }

    function push(uint256 new_elem) public {
        require(size < maxSize);
        internal_arr.push(new_elem);
        size += 1;
    }

    function pop() public returns (uint256) {
        require(!isEmpty());
        uint256 was = top();
        internal_arr.pop();
        size = size - 1;
        return was;
    }

    function push_precondition() public view returns (bool) {
        return size < maxSize;
    }

    function pop_precondition() public view returns (bool) {
        return !isEmpty();
    }
}

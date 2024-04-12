// SPDX-License-Identifier: MIT
pragma solidity 0.6.0;

contract OwnerContract {
    event Receive(uint256 ammount, address sender);

    receive() external payable {
        require(msg.value > 0);
        emit Receive(msg.value, msg.sender);
    }
}

contract Token {
    mapping(address => uint256) balances;
    uint256 public totalSupply;
    OwnerContract owner;

    constructor(uint256 _initialSupply) public payable {
        balances[msg.sender] = totalSupply = _initialSupply;
        owner = OwnerContract(msg.sender);
    }

    function transfer_tokens(
        address _to,
        uint256 _value
    ) public returns (bool) {
        require(balances[msg.sender] - _value >= 0);
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        return true;
    }

    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }

    function withdraw_all() public {
        require(msg.sender == address(owner));
        payable(address(owner)).transfer(balances[address(owner)] * 10);
    }

    function breakme() public {
        assert(false);
    }
}

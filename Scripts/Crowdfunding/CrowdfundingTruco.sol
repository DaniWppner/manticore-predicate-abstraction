// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 < 0.5.0; 

contract Crowdfunding {
    address owner;
    uint max_block;
    uint goal;
    uint blockNumber;
    mapping(address => uint) backers;
    bool funded = false;

    constructor(address _owner, uint _max_block, uint _goal, uint iniBlock) {
        owner = _owner;
        max_block = _max_block;
        goal = _goal;
        blockNumber = iniBlock;
    }

    function Donate() public payable {
        if(max_block <= blockNumber) {
            revert();
        }
        else {
            if(backers[msg.sender] == 0) {
                backers[msg.sender] = msg.value;
            }
            else {
                revert();
            }
        }
    }

    function GetFunds() public {
        if(max_block < blockNumber && msg.sender == owner) {
            if(goal <= address(this).balance) {
                funded = true;
                owner.transfer(address(this).balance);
            }
            else {
                revert();
            }
        }
        else {
            revert();
        }
    }

    function Claim() public {
        if(blockNumber <= max_block) {
            revert();
        }
        else {
            if(backers[msg.sender] == 0 || funded || goal <= address(this).balance) {
                revert();
            }
            else {
                uint val = backers[msg.sender];
                backers[msg.sender] = 0;
                (msg.sender).transfer(val);
            }
        }
    }

    function tau(uint blocksAdvanced) public {
        uint res = blockNumber + blocksAdvanced;
        assert(res >= blockNumber); //no agreguemos un bug de overflow 
        blockNumber = res;
    }

    function Donate_precondition() public returns (bool){
        return(max_block > blockNumber);
    }

    function GetFunds_precondition() public returns (bool){
        return(goal <= address(this).balance && max_block < blockNumber);
    }

    function Claim_precondition() public returns (bool){
       return(blockNumber > max_block && goal > address(this).balance && !funded);
    }

    function tau_precondition() public returns (bool){
        return true;
    }

    function balanceGTZero_precondition() public returns (bool){
        return (address(this).balance > 0);
    }

}
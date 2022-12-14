// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 < 0.5.0; 

contract Crowdfunding {
    address owner;
    uint max_block;
    uint goal;

    mapping(address => uint) backers;
    bool funded = false;

    constructor(address _owner, uint _max_block, uint _goal) {
        owner = _owner;
        max_block = _max_block;
        goal = _goal;
    }

    function Donate() public payable {
        if(max_block <= block.number) {
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
        if(max_block < block.number && msg.sender == owner) {
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
        if(block.number <= max_block) {
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

    function estadoInicialTFF() public returns (bool){
        return(D_predicate() && !F_predicate() && !C_predicate());
    }

    function estadoFinalFTF() public returns (bool){
        assert(!D_predicate() && F_predicate() && !C_predicate());
        return true;
    }

    function estadoFinalFTT() public returns (bool){
        require( ! (!D_predicate() && F_predicate() && !C_predicate()) );
    }

    function ifEstadoInicialTFFDonate() public payable{
        if(estadoInicialTFF()){
        //Donate() inlineado
            if(max_block <= block.number) {
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
        //End Donate    
        }
    }

    function estadoFinalImposible() public returns (bool){
        require (true);
    }

    function D_predicate() public returns (bool){
        return(max_block > block.number);
    }

    function F_predicate() public returns (bool){
        return(goal <= address(this).balance && max_block < block.number);
    }

    function C_predicate() public returns (bool){
       return(block.number > max_block && goal > address(this).balance && !funded);
    }

}
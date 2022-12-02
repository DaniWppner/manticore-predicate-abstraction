// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 < 0.5.0; 

contract Flag{
    uint public counter;
    uint public goal;
    bool public finished;

    constructor (uint _initial_count, uint _initial_goal) public{
        counter = _initial_count;
        goal = _initial_goal;
        finished = false;
    }

    function count(uint ammount) public returns(uint){
        if (counter < goal && !finished){
            counter += ammount;
            return counter;
        }
        else{
            revert();
        }
    }

    function reachFlag() public returns(bool){
        if(counter > goal && !finished){
            finished = true;
            return true;
        }else{
            revert();
        }

    }

    function reset() public{
        if(finished){
            counter = 0;
            finished = false;
        }else{
            revert();
        }
    }

    function count_pre() public returns(bool){
        return (counter < goal && !finished);
    }

    function reach_pre() public returns(bool){
        return (counter > goal && !finished); 
    }

    function reset_pre() public returns(bool){
        return finished;
    }

    function sixth_transition(uint ammount) public returns(bool){
        if(count_pre() && !reach_pre() && !reset_pre()){
            count(ammount);
            return (count_pre() && reach_pre() && reset_pre());
        }else{
            return false;
        }
    }

    function seventh_transition(uint ammount) public returns(bool){
        if(count_pre() && !reach_pre() && !reset_pre()){
            count(ammount);
            return (count_pre() && !reach_pre() && reset_pre());
        }else{
            return false;
        }
    }

    function eigth_transition(uint ammount) public returns(bool){
        if(count_pre() && !reach_pre() && !reset_pre()){
            count(ammount);
            return (!count_pre() && reach_pre() && reset_pre());
        }else{
            return false;
        }
    }

}
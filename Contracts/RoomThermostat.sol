pragma solidity >=0.4.25 <0.9.0;

contract RoomThermostat {
    //Set of States
    enum StateType { Created, InUse}
    
    //List of properties
    StateType public State;
    address public Installer;
    address public User;
    int public TargetTemperature;
    enum ModeEnum {Off, Cool, Heat, Auto}
    ModeEnum public  Mode;
    
    constructor(address thermostatInstaller, address thermostatUser) public
    {
        Installer = thermostatInstaller;
        User = thermostatUser;
        TargetTemperature = 70;
        State = StateType.Created;
    }

    function StartThermostat() public
    {
        if (Installer != msg.sender || State != StateType.Created)
        {
            revert();
        }

        State = StateType.InUse;
    }

    function SetTargetTemperature(int targetTemperature) public
    {
        if (User != msg.sender || State != StateType.InUse)
        {
            revert();
        }
        TargetTemperature = targetTemperature;
    }

    function SetMode(ModeEnum mode) public
    {
        if (User != msg.sender || State != StateType.InUse)
        {
            revert();
        }
        Mode = mode;
    }

    function StartThermostat_precondition() public returns(bool){
        return (State == StateType.Created && Installer == msg.sender);
    }
    function SetTargetTemperature_precondition(int targetTemperature) public returns(bool){
        return (State == StateType.InUse && User == msg.sender);
    }
    function SetMode_precondition(ModeEnum mode) public returns(bool){
        return (State == StateType.InUse && User == msg.sender);
    }

}
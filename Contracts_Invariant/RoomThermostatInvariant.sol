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
    ModeEnum public Mode;
    
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

    function setter(StateType stateNew, address installerNew, address userNew, int targetTemperatureNew, ModeEnum modeNew) public {
        require(invariant(stateNew,installerNew,userNew,targetTemperatureNew,modeNew));
        State = stateNew;
        Installer = installerNew;
        User = userNew;
        TargetTemperature = targetTemperatureNew;
        Mode = modeNew;
    }

    function invariant(StateType stateNew, address installerNew, address userNew, int targetTemperatureNew, ModeEnum modeNew) public returns(bool){
        bool result = (stateNew == StateType.Created || stateNew == StateType.InUse);
        result = result && (modeNew == ModeEnum.Auto || modeNew == ModeEnum.Cool || modeNew == ModeEnum.Heat || modeNew == ModeEnum.Off);
        if(stateNew == StateType.Created){
            result = (targetTemperatureNew == 70) && (modeNew == ModeEnum.Off);
        }
        return result;
    }
 

    function StartThermostat_precondition() public returns(bool){
        return (State == StateType.Created);
    }
    function SetTargetTemperature_precondition() public returns(bool){
        return (State == StateType.InUse);
    }
    function SetMode_precondition() public returns(bool){
        return (State == StateType.InUse);
    }

}
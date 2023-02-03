pragma solidity >=0.4.25 <0.6.0;

contract RoomThermostat
{
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

    function ST(address sender) public returns(bool){
        return(!(Installer != sender || State != StateType.Created) );
    }

    function STT(address sender) public returns(bool){
        return(!(User != sender || State != StateType.InUse));
    }
    
    function SM(address sender) public returns(bool){
        return(!(User != sender || State != StateType.InUse) );
    }

    function StartThermostatTransition(address senderOfSecondTransaction) public returns(bool){
        bool success = false;
        if (ST(msg.sender) && !STT(msg.sender) && !SM(msg.sender)){
            //Inline por cuestiones de msg.sender
            if (Installer != msg.sender || State != StateType.Created)
            {
                revert();
            }

            State = StateType.InUse;
            //Fin inline
            
            success = !ST(senderOfSecondTransaction) && STT(senderOfSecondTransaction) && SM(senderOfSecondTransaction);
        }
        return success;
    }   
}


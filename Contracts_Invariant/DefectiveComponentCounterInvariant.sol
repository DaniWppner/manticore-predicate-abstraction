pragma solidity >=0.4.25 <0.6.0;

contract DefectiveComponentCounter {

     //Set of States
    enum StateType {Create, ComputeTotal}

    //List of properties
    StateType public  State;
    address public  Manufacturer;
    int[12] public DefectiveComponentsCount;
    int public Total;

    // constructor function
    constructor(int[12] memory defectiveComponentsCount) public
    {
        Manufacturer = msg.sender;
        DefectiveComponentsCount = defectiveComponentsCount;
        Total = 0;
        State = StateType.Create;
    }

    // call this function to send a request
    function ComputeTotal() public
    {
        if (Manufacturer != msg.sender)
        {
            revert();
        }

        // calculate total for only the first 12 values, in case more than 12 are entered
        for (uint i = 0; i < 3; i++)
        {
            Total += DefectiveComponentsCount[i];
        }

        State = StateType.ComputeTotal;
    }

    // add the required getter function for array DefectiveComponentsCount
    function GetDefectiveComponentsCount() public view returns (int[12] memory) {
        return DefectiveComponentsCount;
    }

    function ComputeTotal_precondition() public returns (bool){
        return true;
    }
    function GetDefectiveComponentsCount_precondition() public returns (bool){
        return true;
    }
    function EnumStateType() public returns (string memory){
        return ("Create,ComputeTotal");
    }

    function setter(StateType stateNew, address manufacturerNew, int[12] memory defectiveComponentsCountNew, int totalNew) public {
        require(invariant(stateNew,manufacturerNew,defectiveComponentsCountNew,totalNew));
        State = stateNew;
        Manufacturer = manufacturerNew;
        DefectiveComponentsCount = defectiveComponentsCountNew;
        Total = totalNew;
    }

    function invariant(StateType stateNew, address manufacturerNew, int[12] memory defectiveComponentsCountNew, int totalNew) public returns(bool){
        bool result = (stateNew == StateType.Create || stateNew == StateType.ComputeTotal);
        if (stateNew == StateType.Create){
            result = result && Total == 0;
        }
        return result;
    }
}
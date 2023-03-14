pragma solidity >=0.4.25 <0.6.0;

contract DigitalLocker {
    enum StateType { Requested, DocumentReview, AvailableToShare, SharingRequestPending, SharingWithThirdParty, Terminated }
    address public Owner;
    address public BankAgent;
    string public LockerFriendlyName;
    string public LockerIdentifier;
    address public CurrentAuthorizedUser;
    string public ExpirationDate;
    string public Image;
    address public ThirdPartyRequestor;
    string public IntendedPurpose;
    string public LockerStatus;
    string public RejectionReason;
    StateType public State;

    constructor(string memory lockerFriendlyName, address bankAgent) public
    {
        Owner = msg.sender;
        LockerFriendlyName = lockerFriendlyName;

        State = StateType.DocumentReview; //////////////// should be StateType.Requested?

        BankAgent = bankAgent;
    }

    function BeginReviewProcess() public
    {
        /* Need to update, likely with registry to confirm sender is agent
        Also need to add a function to re-assign the agent.
        */
        if (Owner == msg.sender)
        {
            revert();
        }
        BankAgent = msg.sender;

        LockerStatus = "Pending";
        State = StateType.DocumentReview;
    }

    function RejectApplication(string memory rejectionReason) public
    {
        if (BankAgent != msg.sender)
        {
            revert();
        }

        RejectionReason = rejectionReason;
        LockerStatus = "Rejected";
        State = StateType.DocumentReview;
    }

    function UploadDocuments(string memory lockerIdentifier, string memory image) public
    {
        if (BankAgent != msg.sender)
        {
            revert();
        }
        LockerStatus = "Approved";
        Image = image;
        LockerIdentifier = lockerIdentifier;
        State = StateType.AvailableToShare;
    }

    function ShareWithThirdParty(address thirdPartyRequestor, string memory expirationDate, string memory intendedPurpose) public
    {
        if (Owner != msg.sender)
        {
            revert();
        }

        ThirdPartyRequestor = thirdPartyRequestor;
        CurrentAuthorizedUser = ThirdPartyRequestor;

        LockerStatus = "Shared";
        IntendedPurpose = intendedPurpose;
        ExpirationDate = expirationDate;
        State = StateType.SharingWithThirdParty;
    }

    function AcceptSharingRequest() public
    {
        if (Owner != msg.sender)
        {
            revert();
        }

        CurrentAuthorizedUser = ThirdPartyRequestor;
        State = StateType.SharingWithThirdParty;
    }

    function RejectSharingRequest() public
    {
        if (Owner != msg.sender)
        {
            revert();
        }
        LockerStatus = "Available";
        CurrentAuthorizedUser = address(0x0000000000000000000000000000000000000000);
        State = StateType.AvailableToShare;
    }

    function RequestLockerAccess(string memory intendedPurpose) public
    {
        if (Owner == msg.sender)
        {
            revert();
        }

        ThirdPartyRequestor = msg.sender;
        IntendedPurpose = intendedPurpose;
        State = StateType.SharingRequestPending;
    }

    function ReleaseLockerAccess() public
    {

        if (CurrentAuthorizedUser != msg.sender)
        {
            revert();
        }
        LockerStatus = "Available";
        ThirdPartyRequestor = address(0x0000000000000000000000000000000000000000);
        CurrentAuthorizedUser = address(0x0000000000000000000000000000000000000000);
        IntendedPurpose = "";
        State = StateType.AvailableToShare;
    }
    
    function RevokeAccessFromThirdParty() public
    {
        if (Owner != msg.sender)
        {
            revert();
        }
        LockerStatus = "Available";
        CurrentAuthorizedUser = address(0x0000000000000000000000000000000000000000);
        State = StateType.AvailableToShare;
    }

    function Terminate() public
    {
        if (Owner != msg.sender)
        {
            revert();
        }
        CurrentAuthorizedUser = address(0x0000000000000000000000000000000000000000);
        State = StateType.Terminated;
    }

    function BeginReviewProcess_precondition() public returns(bool){return true;}
    function RejectApplication_precondition(string memory rejectionReason) public returns(bool){return true;}
    function UploadDocuments_precondition() public returns(bool){return true;}
    function ShareWithThirdParty_precondition() public returns(bool){return true;}
    function AcceptSharingRequest_precondition() public returns(bool){return true;}
    function RejectSharingRequest_precondition() public returns(bool){return true;}
    function RequestLockerAccess_precondition(string memory intendedPurpose) public returns(bool){return true;}
    function ReleaseLockerAccess_precondition() public returns(bool){return true;}
    function RevokeAccessFromThirdParty_precondition() public returns(bool){return true;}
    function Terminate_precondition() public returns(bool){return true;}

    function EnumStateType() public returns(string memory){
        return ("Requested,DocumentReview,AvailableToShare,SharingRequestPending,SharingWithThirdParty,Terminated");
    }

}
import sys,os
up_two_levels = os.path.dirname(os.path.dirname(sys.path[0]))
sys.path.append(up_two_levels)
from state_constrainer_YY import state_constrainer

tchk = state_constrainer("Sender.sol",outputspace="graph")
account2 = tchk.manticore.create_account(balance=10**18)

tchk.callContractFunction("MakeOffer")
tchk.callContractFunction("AcceptOffer")

tchk.callContractFunction("Redeem_precondition")


result = tchk.generateTestCases(keys=["Redeem_precondition"],targets=[1],testcaseName=f"transition Redeem")
if(result>0):
    print(f"found {result} testcases for Redeem")
else:
    print(f"no testcases for Redeem")

tchk.safedelete()

sys.exit()
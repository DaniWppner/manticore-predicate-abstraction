from subclassed_epa_constructor import SubClassedEpaConstructor
from pathlib import Path

this_dir = Path(__file__).parent
ETHER = 10**18


epa_const = SubClassedEpaConstructor(str(
    this_dir / 'Token.sol'), str(this_dir / 'epa_on_token'), initial_balance=1*ETHER)
epa_const.construct_abstraction()

from pathlib import Path
from subclassed_manticore_handler import SubclassedManticoreHandler

ETHER = 10**18


this_dir = Path(__file__).parent
output = this_dir / 'single_contract_error2'
token_source_code_path = str(this_dir / 'Token.sol')

m_handler = SubclassedManticoreHandler(token_source_code_path, str(output))
# owner_contract = m_handler.add_contract(token_source_code_path, contract_name='OwnerContract')
m_handler.init_working_contract(
    token_source_code_path, contract_name='Token', balance=1*ETHER)

m_handler.callContractFunction(
    'transfer_tokens', call_args=(m_handler.witness_account, 10))
m_handler.callContractFunction('withdraw_all')
# m_handler.generateTestCases(testcaseName='CallToBreakMe')
m_handler.safedelete(generate_test_cases=True)

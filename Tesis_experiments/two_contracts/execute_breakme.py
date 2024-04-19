from manticore_handler import manticore_handler
from pathlib import Path
import sys
print("####PATH:")
base_dir = Path(__file__).parent.parent.parent
print(str(base_dir))
sys.path.append(str(base_dir))


this_dir = Path(__file__).parent
output = this_dir / 'breakme_result'

m_handler = manticore_handler(
    str(this_dir / 'Token.sol'), str(output), contract_name='Token')
m_handler.callContractFunction('breakme')
# m_handler.generateTestCases(testcaseName='CallToBreakMe')
m_handler.safedelete(generate_test_cases=True)

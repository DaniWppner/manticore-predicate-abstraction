from manticore import ManticoreEVM
import sys
from pathlib import Path

base_dir = Path(__file__).parent.parent.parent
sys.path.append(str(base_dir))

from manticore_handler import manticore_handler


# Now you can import the module in the parent directory


class SubclassedManticoreHandler(manticore_handler):

    def __init__(self, url, outputspace=None, workspace=None):
        if outputspace is None:
            outputspace = url + "_results"
        self.manticore = ManticoreEVM(
            workspace_url=workspace, outputspace_url="fs:"+outputspace)

        self._initAccounts()
        self._initBlockchain()
        self._snapshot_history = []
        self.outputspace = outputspace

    def init_working_contract(self, url, contract_name=None, args=None, owner=None, balance=None):
        self.working_contract = self.add_contract(url, contract_name, args=args, owner=owner, balance=balance)
        self._initContractSelectorsAndMetadata()

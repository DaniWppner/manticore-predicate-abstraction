from manticore import ManticoreEVM
import sys
from pathlib import Path

base_dir = Path(__file__).parent.parent.parent
sys.path.append(str(base_dir))
from AbstractionConstructor import epa_constructor
from subclassed_manticore_handler import SubclassedManticoreHandler

class SubClassedEpaConstructor(epa_constructor):
    def __init__(self, path, outputdir, advanceBlocks=False, initial_balance=0):
        self.path = path
        self.outputdir = outputdir
        Path(outputdir).mkdir(parents=True, exist_ok=True)
        self.manticore_handler = SubclassedManticoreHandler(
            self.path, outputspace=outputdir)
        self.manticore_handler.init_working_contract(self.path,balance=initial_balance)
        self.advanceBlocks = advanceBlocks
        self.__init_states_and_methods__()

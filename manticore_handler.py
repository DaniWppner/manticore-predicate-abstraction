import time
from manticore.core.smtlib import expression, operators
from manticore.ethereum import ManticoreEVM, ABI
import os

ETHER = 10**18
TAU = 'tau'


class manticore_handler:
    def __init__(self, url, outputspace=None, workspace=None, contract_name=None):
        if outputspace is None:
            outputspace = url + "_results"
        self.manticore = ManticoreEVM(
            workspace_url=workspace, outputspace_url="fs:"+outputspace)

        self._initAccountsAndContract(url, contract_name)
        self._initContractSelectorsAndMetadata()
        self._initBlockchain()
        self._snapshot_history = []
        self.outputspace = outputspace

    def _initAccountsAndContract(self, url, contract_name):
        self._initAccounts()
        print(f"# -- Deploying Contract {url}")
        self.working_contract = self.add_contract(url, contract_name)

    def _initAccounts(self):
        # Por ahora suponemos que tres cuentas es suficiente para la mayoria de los casos
        self.owner_account = self.manticore.create_account(balance=100*ETHER)
        # self.client_account = self.manticore.create_account(balance=100*ETHER)
        self.witness_account = self.manticore.create_account(
            balance=100*ETHER, name="witness")

    def _initContractSelectorsAndMetadata(self):
        self.nameToFuncId = {}
        self.precon_names = []
        self.contractfunc_names = []
        self.enumdescriptor_names = []
        self.predicate_names = []
        self.contract_metadata = self.manticore.get_metadata(
            self.working_contract)

        for func_hsh in self.contract_metadata.function_selectors:
            func_name = self.contract_metadata.get_func_name(func_hsh)
            # detect preconditions
            self.nameToFuncId[func_name] = func_hsh
            if func_name.endswith("_precondition"):
                self.precon_names.append(func_name)
            elif func_name.startswith("Enum"):
                self.enumdescriptor_names.append(func_name)
            elif func_name.endswith("_predicate"):
                self.predicate_names.append(func_name)
            else:
                self.contractfunc_names.append(func_name)

    def _initBlockchain(self):
        self.initial_symbolic_blockchain_vars = set()
        self.set_block_to_new_symbolic(name="initial_block")

    def callContractFunction(self, func_name, call_args=None, tx_value=None, tx_sender=None):
        if func_name == TAU:  # FIXME TAU
            self.tau()  # do we really need a class representing the methods if this is the only exception?
        else:
            func_id = self.nameToFuncId[func_name]

            print(f"# -- Calling {func_name}")

            call_args, tx_value, tx_sender = self.make_transaction_parameters(
                func_id, call_args, tx_value, tx_sender)

            # __getattr__ is overriden to construct the function object.
            fun = getattr(self.working_contract, func_name)
            fun(*call_args, value=tx_value, caller=tx_sender)

    def make_transaction_parameters(self, func_id, call_args=None, tx_value=None, tx_sender=None):
        # construct the arguments passed to the contract method
        if call_args is None:
            arg_types = self.contract_metadata.get_func_argument_types(func_id)
            call_args = self.manticore.make_symbolic_arguments(arg_types)

        # make a symbolic (or zero) value for the transaction
        if tx_value is None:
            if self.contract_metadata.get_abi(func_id)['stateMutability'] == 'payable':
                tx_value = self.manticore.make_symbolic_value()
            else:
                tx_value = 0

        # construct a sender for the transaction
        # if it is symbollic it will concretize to one of the existing accounts in the manticore ethereum world
        if tx_sender is None:
            tx_sender = self.manticore.make_symbolic_address()
        return call_args, tx_value, tx_sender

    def constrainTo(self, func_name, expectedResult):
        self.callContractFunction(func_name)
        func_id = self.nameToFuncId[func_name]

        for state in self.manticore.ready_states:
            tx = state.platform.last_human_transaction
            if (tx.data[:4] == func_id):
                result = self.result_of_tx(tx, func_id)
                assert result is not None
                # Constrain for each state
                print(
                    f"# -- Constrain {func_name} in state #{state.id} to {repr(expectedResult)}")
                if isinstance(expectedResult, int):
                    expectedResult = expression.BitVecConstant(
                        size=result.size, value=expectedResult)
                state.constrain(result == expectedResult)

    def result_of_tx(self, transaction, func_id):
        if transaction.return_value == 1:
            return_types = self.contract_metadata.get_func_return_types(
                func_id)
            if (return_types != '()'):
                # FIXME transforma "(int)" -> "int"      (es un bug de manticore)
                # No funciona si la transaccion tuvo varios returns
                return_types = return_types[1:-1]
                result = ABI.deserialize(return_types, transaction.return_data)
                return result

    def last_return_of(self, func_name):
        # Se espera que sea constante el valor a retornar
        func_id = self.nameToFuncId[func_name]
        for state in self.manticore.ready_states:
            tx = state.platform.last_human_transaction
            if (tx.data[:4] == func_id):
                result = self.result_of_tx(tx, func_id)
                return state.solve_one(result)

    def getEnumInfo(self):
        # deberia hacerse para que devuelva el diccionario si ya existe
        self.enums = {}

        for func_hsh in self.contract_metadata.function_selectors:
            func_name = self.contract_metadata.get_func_name(func_hsh)
            for output in self.contract_metadata.get_abi(func_hsh)['outputs']:
                internalReturnType = output['internalType']
                # Esta solucion podria ser muy mala si hay otros metodos que tambien devuelven algo de tipo enum
                if internalReturnType.startswith('enum'):
                    enumTypeName = internalReturnType.replace(
                        'enum ', '').split('.')[-1]
                    # En respuesta al otro comentario:
                    # igual estamos filtrando que el nombre del metodo arranque con "Enum".
                    if ("Enum"+enumTypeName in self.enumdescriptor_names):
                        self.callContractFunction(
                            "Enum"+enumTypeName, tx_sender=self.witness_account)
                        self.enums[func_name] = self.last_return_of(
                            "Enum"+enumTypeName).decode().split(',')
        return self.enums

    def generateTestCases(self, testcaseName, keys=None, targets=None, ammount=1):
        '''pre: testcaseName is different than each other previous testcaseName.
        pos:generate a testcase where the function in keys has the result in targets. Print it on file named testcaseName.'''
        func_ids_of_keys = list(
            map(lambda name: self.nameToFuncId[name], keys))
        if not (0 < ammount <= self.manticore.count_ready_states()):
            ammount = self.manticore.count_ready_states()
        found = False
        for state in self.manticore.ready_states:
            if found:
                break
            # find the result of each function in func_ids
            results = []
            temp_ids = func_ids_of_keys.copy()
            # human_transactions is in chronological order
            for tx in reversed(state.platform.human_transactions):
                if not temp_ids:
                    break
                if tx.data[:4] == temp_ids[-1]:
                    results.append(self.result_of_tx(tx, temp_ids[-1]))
                    temp_ids.pop()
            # this makes it so their order is the same as the one in targets
            results = list(reversed(results))

            # generate condition to be tested. The condition needs to be constructed independantly for each state.
            condition = expression.BoolConstant(value=True)
            for data, target in zip(results, targets):
                if isinstance(target, int):  # pretty sure we need to do this for '==' to work
                    target = expression.BitVecConstant(
                        size=data.size, value=target)
                condition = operators.AND(condition, data == target)

            can_be_true = state.can_be_true(condition)
            if can_be_true:
                found = True
                with state as temp_state:
                    temp_state.constrain(condition)
                    self.manticore.generate_testcase(
                        state=temp_state, name=testcaseName+f"")
                    # Also generate concrete values for variables that part of the blockchain itself
                    to_concretize = state.input_symbols + \
                        list(self.initial_symbolic_blockchain_vars)
                    values = temp_state.solve_one_n_batched(to_concretize)
                    outputfile = [filename for filename in os.listdir(self.outputspace) if filename.startswith(
                        testcaseName) and filename.endswith('.tx')][0]  # previous call to manticore generated this file.

                    migration_map = temp_state.context.get("migration_map")
                    for concrete, symbolic in zip(values, to_concretize):
                        # Puede no ser agregada al migration_map si no es simbolica.
                        if symbolic.name in migration_map:
                            del migration_map[symbolic.name]
                        with open(self.outputspace+"/"+outputfile, 'a') as output:
                            output.write(
                                f"-Concrete value for {symbolic.name} : {concrete}\n")
                    temp_state.context["migration_map"] = migration_map

                    # FIXME Even though temp_state is supposed to be a CoW version of state, both share the same reference to the attribute called "context".
                    # This makes it so when the variables in "to_concretize" are migrated into "temp_state"'s set of constraints,
                    # the variables remain named in the original state's migration_map, even though the variables themselves are properly deleted.
                    # This is why we need to delete them manually from the migration_map.

        return found

    def advance_symbolic_ammount_of_blocks(self):
        for state in self.manticore.ready_states:
            # we are creating a new symbolic variable for each manticore state.
            index = len([var for var in state.input_symbols if var.name.startswith(
                "blocks_advanced")]) + 1
            ammount = state.new_symbolic_value(
                nbits=256, label=f"blocks_advanced{index}")
            state.constrain(ammount >= 0)
            world = state.platform
            world.advance_block_number(ammount)

    def tau(self):
        self.advance_symbolic_ammount_of_blocks()

    def set_block_to_new_symbolic(self, name):
        initial_block = self.manticore.make_symbolic_value(name=name)
        self.manticore.constrain(initial_block > 0)
        self.initial_symbolic_blockchain_vars.add(initial_block)
        self.manticore.start_block(blocknumber=initial_block,
                                   # current unix timestamp, #FIXME?
                                   timestamp=int(time.time()),
                                   # FIXME as well. It has to be set to _something_ for manticore.end_block() not to throw.
                                   coinbase=self.owner_account,
                                   difficulty=0x200,  # default
                                   gaslimit=0x7FFFFFFF)  # default

    def add_contract(self, url, contract_name=None, args=None, owner=None, balance=0):
        print(f"# -- Deploying Contract {url}")
        with open(url, 'r') as file:
            source_code = file.read()
        start = time.time()
        if owner is None:
            owner = self.owner_account
        # Hardcodeamos args=None para que use argumentos simbolicos por defecto
        new_contract = self.manticore.solidity_create_contract(
            source_code, owner=owner, args=args, contract_name=contract_name, balance=balance)
        end = time.time()
        assert (
            new_contract is not None), "Problemas en el creado del contrato"
        print(f"# -- Contract Deployed      (took {end-start} seconds)")
        return new_contract

    def take_snapshot(self):
        self.manticore.take_snapshot()
        self._snapshot_history.append(
            self.initial_symbolic_blockchain_vars.copy())

    def goto_snapshot(self):
        self.manticore.goto_snapshot()
        self.initial_symbolic_blockchain_vars = self._snapshot_history.pop()

    def can_be_true(self, expr):
        count = 0
        for state in self.manticore.ready_states:
            if state.can_be_true(expr):
                count += 1
        return count

    def isallive(self):
        return (self.manticore.count_ready_states() > 0)

    def safedelete(self, generate_test_cases=False):
        if generate_test_cases:
            self.manticore.finalize()
        else:
            self.manticore.kill()
            self.manticore.remove_all()

from typing import Callable, List, Type

from .implementations.mct_base import MCTBase
from .implementations.mct_n_qubit_decomposition import MCTNQubitDecomposition
from .implementations.mct_no_ancilla import MCTNoAncilla
from .implementations.mct_no_ancilla_relative_phase import MCTNoAncillaRelativePhase
from .implementations.mct_parallel_decomposition import MCTParallelDecomposition
from .implementations.mct_vchain import MCTVChain


class Qumcat:
    def __init__(self):
        self._registered_methods: List[Type[MCTBase]] = [
            MCTNoAncilla,
            MCTNQubitDecomposition,
            MCTNoAncillaRelativePhase,
            MCTParallelDecomposition,
            MCTVChain,
        ]
        self._implementations: List[MCTBase] = []

    def register_method(self, mct_method: Type[MCTBase]):
        if mct_method not in self._registered_methods:
            self._registered_methods.append(mct_method)
        else:
            raise Warning("Method already registered")

    def unregister_method(self, mct_method: Type[MCTBase]):
        # TODO remove all occurences:
        pass

    # TODO replace kwargs below with the same arguments as the concrete implementations
    def generate_mct_cases(self, controls_no: int, max_ancilla: int, **kwargs):
        self._implementations = []
        for cls in self._registered_methods:
            self._implementations += cls.generate_mct_cases(controls_no, max_ancilla, **kwargs)

    def filter_mct_cases(self, filter_fun: Callable[[MCTBase], bool]):
        self._implementations = list(filter(filter_fun, self._implementations))

    def get_best(self, opt_fun: Callable[[MCTBase], int]) -> MCTBase:
        return min(self._implementations, key=opt_fun)

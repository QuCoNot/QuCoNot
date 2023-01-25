from typing import Callable, List, Type

from .implementations.mct_barenco_74_dirty import MCTBarenco74Dirty
from .implementations.mct_barenco_75_dirty import MCTBarenco75Dirty
from .implementations.mct_base import MCTBase
from .implementations.mct_n_qubit_decomposition import MCTNQubitDecomposition
from .implementations.mct_no_auxiliary import MCTNoAuxiliary
from .implementations.mct_no_auxiliary_relative import MCTNoAuxiliaryRelative
from .implementations.mct_parallel_decomposition import MCTParallelDecomposition
from .implementations.mct_recursion import MCTRecursion
from .implementations.mct_vchain import MCTVChain
from .implementations.mct_vchain_dirty import MCTVChainDirty


class QuCoNot:
    def __init__(self):
        self._registered_methods: List[Type[MCTBase]] = [
            MCTBarenco74Dirty,
            MCTBarenco75Dirty,
            MCTRecursion,
            MCTVChainDirty,
            MCTNQubitDecomposition,
            MCTNoAuxiliary,
            MCTNoAuxiliaryRelative,
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
    # def verify_mct_cases(self, controls_no: int, max_auxiliary: int, **kwargs):
    def verify_mct_cases(
        self,
        controls_no: int,
        max_auxiliary: int,
        relative_phase: bool = False,
        clean_auxiliary: bool = True,
        wasted_auxiliary: bool = False,
        separable_wasted_auxiliary: bool = False,
    ) -> List["MCTBase"]:

        self._implementations = []
        for cls in self._registered_methods:

            self._implementations += cls.verify_mct_cases(
                controls_no,
                max_auxiliary,
                relative_phase,
                clean_auxiliary,
                wasted_auxiliary,
                separable_wasted_auxiliary,
            )

        return self._implementations

    def filter_mct_cases(self, filter_fun: Callable[[MCTBase], bool]):
        self._implementations = list(filter(filter_fun, self._implementations))

    def get_best(self, opt_fun: Callable[[MCTBase], int]) -> MCTBase:
        return min(self._implementations, key=opt_fun)

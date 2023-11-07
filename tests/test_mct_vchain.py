from typing import Dict, Type

import numpy as np
import pytest

from quconot.implementations.mct_base import MCTBase
from quconot.implementations.mct_vchain import MCTVChain
from tests.test_mct_base import BaseTestMCT


class TestMCTVChain(BaseTestMCT):
    _matrix_dict: Dict[int, np.ndarray] = {}
    _ref_matrices: Dict[int, np.ndarray] = {}
    _controls_no_list = [5]

    _expected_classes: Dict[str, bool] = {
        "SCNW": True,
        "RCNW": True,
        "SDNW": False,
        "RDNW": False,
        "SCWE": True,
        "SCWS": True,
        "RCWS": True,
        "SDWE": False,
        "SDWS": False,
        "RDWS": False,
    }

    @property
    def _get_class_name(self) -> Type[MCTBase]:
        return MCTVChain

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be >= 2 for this implementation"
        ):
            MCTVChain(1)

        try:
            MCTVChain(5)
        except Exception:
            assert False, "object MCTVChain(5) was not created, but it should be"

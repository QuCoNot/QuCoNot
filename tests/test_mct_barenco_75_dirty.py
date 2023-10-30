from typing import Dict, Type

import numpy as np
import pytest

from quconot.implementations.mct_barenco_75_dirty import MCTBarenco75Dirty
from quconot.implementations.mct_base import MCTBase
from tests.test_mct_base import BaseTestMCT


class TestMCTBarenco75Dirty(BaseTestMCT):
    _matrix_dict: Dict[int, np.ndarray] = {}
    _ref_matrices: Dict[int, np.ndarray] = {}
    _controls_no_list = [5]

    _expected_classes: Dict[str, bool] = {
        "SCNW": True,
        "RCNW": True,
        "SDNW": True,
        "RDNW": True,
        "SCWE": True,
        "SCWS": True,
        "RCWS": True,
        "SDWE": True,
        "SDWS": True,
        "RDWS": True,
    }

    @property
    def _get_class_name(self) -> Type[MCTBase]:
        return MCTBarenco75Dirty

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be >= 2 for this implementation"
        ):
            MCTBarenco75Dirty(1)

        try:
            MCTBarenco75Dirty(2)
        except Exception:
            assert False, "object MCTBarenco75Dirty(2) was not created, but it should be"

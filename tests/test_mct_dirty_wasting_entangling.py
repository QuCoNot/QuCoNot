from typing import Dict, Type

import numpy as np
import pytest

from quconot.implementations.mct_base import MCTBase
from quconot.implementations.mct_dirty_wasting_entangling import (
    MCTDirtyWastingEntangling,
)
from tests.test_mct_base import BaseTestMCT


class TestMCTDirtyWastingEntangling(BaseTestMCT):
    _matrix_dict: Dict[int, np.ndarray] = {}
    _ref_matrices: Dict[int, np.ndarray] = {}
    _controls_no_list = [5]

    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
        "RCNW": False,
        "SDNW": False,
        "RDNW": False,
        "SCWE": True,
        "SCWS": False,
        "RCWS": False,
        "SDWE": True,
        "SDWS": False,
        "RDWS": False,
    }

    @property
    def _get_class_name(self) -> Type[MCTBase]:
        return MCTDirtyWastingEntangling

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be >= 3 for this implementation"
        ):
            MCTDirtyWastingEntangling(1)

        try:
            MCTDirtyWastingEntangling(3)
        except Exception:
            assert (
                False
            ), "object MCTDirtyWastingEntangling(3) was not created, but it should be"

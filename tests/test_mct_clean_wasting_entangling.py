from typing import Dict, Type

import numpy as np
import pytest

from quconot.implementations.mct_base import MCTBase
from quconot.implementations.mct_clean_wasted_entangling import (
    MCTCleanWastingEntangling,
)
from tests.test_mct_base import BaseTestMCT


class TestMCTCleanWastingEntangling(BaseTestMCT):
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
        "SDWE": False,
        "SDWS": False,
        "RDWS": False,
    }

    @property
    def _get_class_name(self) -> Type[MCTBase]:
        return MCTCleanWastingEntangling

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be >= 3 for this implementation"
        ):
            MCTCleanWastingEntangling(1)

        try:
            MCTCleanWastingEntangling(3)
        except Exception:
            assert (
                False
            ), "object MCTCleanWastingEntangling(3) was not created, but it should be"

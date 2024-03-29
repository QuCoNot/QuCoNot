from typing import Dict, Type

import numpy as np
import pytest

from quconot.implementations.mct_base import MCTBase
from quconot.implementations.mct_no_auxiliary import MCTNoAuxiliary
from tests.test_mct_base import BaseTestMCT


class TestMCTNoAuxiliary(BaseTestMCT):
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
        return MCTNoAuxiliary

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be >= 2 for this implementation"
        ):
            MCTNoAuxiliary(1)

        try:
            MCTNoAuxiliary(3)
        except Exception:
            assert (
                False
            ), "object MCTBarenco74Dirty(3) was not created, but it should be"

from typing import Dict, Type

import pytest

from quconot.implementations.mct_base import MCTBase
from quconot.implementations.mct_no_auxiliary_relative import MCTNoAuxiliaryRelative
from tests.test_mct_base import BaseTestMCT


class TestMCTNoAuxiliaryRelative(BaseTestMCT):
    _controls_no_list = [2, 3]

    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
        "RCNW": True,
        "SDNW": False,
        "RDNW": True,
        "SCWE": True,
        "SCWS": False,
        "RCWS": True,
        "SDWE": True,
        "SDWS": False,
        "RDWS": True,
    }

    @property
    def _get_class_name(self) -> Type[MCTBase]:
        return MCTNoAuxiliaryRelative

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be 2 or 3 for this implementation"
        ):
            MCTNoAuxiliaryRelative(1)

        try:
            MCTNoAuxiliaryRelative(2)
        except Exception:
            assert False, "object MCTNoAuxiliaryRelative(2) was not created, but it should be"

from typing import Dict, Type

import pytest

from quconot.implementations.mct_barenco_74_dirty import MCTBarenco74Dirty
from quconot.implementations.mct_base import MCTBase
from tests.test_mct_base import BaseTestMCT


class TestMCTBarenco74Dirty(BaseTestMCT):
    _controls_no_list = [5]

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
        return MCTBarenco74Dirty

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be >= 5 for this implementation"
        ):
            MCTBarenco74Dirty(2)

        try:
            MCTBarenco74Dirty(5)
        except Exception:
            assert (
                False
            ), "object MCTBarenco74Dirty(5) was not created, but it should be"

import numpy as np

from tests.test_mct_base import BaseTest


class BaseTestUnitary(BaseTest):
    def _ref_matrix(self, controls_no: int) -> np.ndarray:
        return np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])

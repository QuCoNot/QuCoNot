from abc import abstractmethod

import numpy as np

from tests.test_mct_base import BaseTest


class BaseTestUnitary(BaseTest):
    @abstractmethod
    def _take_matrix(self) -> np.ndarray:
        raise NotImplementedError

    def _ref_matrix(self):
        U = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]

        return U

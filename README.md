[![codecov](https://codecov.io/gh/QuCoNot/QuCoNot/branch/main/graph/badge.svg?token=DQFY9E763T)](https://codecov.io/gh/QuCoNot/QuCoNot)
[![Documentation Status](https://readthedocs.org/projects/quconot/badge/?version=latest)](https://quconot.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# QuCoNot 🥥

**QuCoNoT** contains an implementations of the verifications procedures for implementation of permutation matrices from the paper `Classification and transformations of quantum circuit decompositions for  permutation operations' available at [arXiv](). The details on how to use the verifications methods can be found in the jupyter notebook quconot.ipynb in the repository, where we try this for a few existing and implemented by us decomposition of Multi-Controlled Toffoli

## Installation details

To start with QuCoNot, you just need to `git clone` and install with `pip`

```
git clone https://github.com/QuCoNot/QuCoNot.git
cd QuCoNot
pip install .
```

## Example

You just need to import it, and you can start use it

```
from quconot.implementations import MCTVChainDirty

mct = MCTVChain(5)
circ = mct.generate_circuit()
```

With `generate_circuit`, you will get the MCT based on the implementation that you choose.

See [Jupyter Notebook file](https://github.com/QuCoNot/QuCoNot/blob/main/quconot.ipynb) for more in detail examples.

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

## Authors
## Authors

The first version of QuCoNot was developed under the remote internship program QIntern 2022. Extended from the program, we continue to create the module.

- Ankit Khandelwal<sup>1</sup>
- Handy Kurniawan<sup>2</sup>
- Shraddha Aangiras<sup>3</sup>
- ¨Ozlem Salehi<sup>4,5,6</sup>
- Adam Glos<sup>4,6</sup>

<sup>1</sup> TCS Research, Tata Consultancy Services, India  
<sup>2</sup> Facultad de Inform ́atica, Universidad Complutense de Madrid, Spain  
<sup>3</sup> Rashtreeya Vidyalaya Preuniversity College, India  
<sup>4</sup> Institute of Theoretical and Applied Informatics, Polish Academy of Sciences, Poland  
<sup>5</sup> QWorld Association, Tallinn, Estonia  
<sup>6</sup> Algorithmiq Ltd, Kanavakatu 3C 00160 Helsinki, Finland  

**Corresponding Author:** Adam Glos



If you are doing research using QuConot, please cite our project.
We use a [CITATION.cff](https://citation-file-format.github.io/) file, so you can easily copy the citation information from the repository landing page.

## License
QuCoNot is **free** and **open source**, released under the Apache License, Version 2.0.

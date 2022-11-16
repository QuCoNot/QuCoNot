# Qumcat Development Guide

> **Note**
> Before running the pre-commit, test the implementation with PyTest first. 
> See [here](https://github.com/QIntern-2022/qumcat/tree/main/test) for PyTest testing guide

This is the documentation to install the requirement for pre-commiting the project.

## :rocket:&nbsp; Getting started 

To rocket right in, download  qumcat with [git](https://git-scm.com/) at the terminal
```bash
git clone https://github.com/QIntern-2022/OpenQASM2-Compiler.git
cd qumcat
```

Then you need to check the version of the related libraries (whether you have installed or not), it should be the same version with the `.pre-commit-config.yaml`.

```bash
pip install isort==5.10.1
pip install black==22.6.0
pip install flake8==5.0.4
pip install mypy==0.971
pip install pylint==2.14.5
pip install pre-commit-hooks==4.3.0
```
After installing the required libraries, now you need to install the `pre-commit` library itself

```bash
pip install pre-commit
```

## Run pre-commit

At this point, you already have the required parts, then you can run the pre-commit on all the existing files to make sure if there is any error or not

```bash
pre-commit run --all-files
```

Below is the expected result if everything is **Passed**

```bash
isort....................................................................Passed
black....................................................................Passed
flake8...................................................................Passed
mypy.....................................................................Passed
pylint...................................................................Passed
file contents sorter.....................................................Passed
```

### Failed Example

This is the example of a failed of flake8 library.

```bash
flake8...................................................................Failed
- hook id: flake8
- exit code: 1

test/test_mct_clean_auxiliary.py:7:1: F401 'qumcat.mct_no_auxiliary.MCTNoAuxiliary' imported but unused
test/test_mct_clean_auxiliary.py:10:1: F401 'qumcat.mct_vchain_dirty.MCTVChainDirty' imported but unused
```

For the error message, it will be clear which part of the code that we need to manually fix it.

## Commiting the code

> **Warning**
> Before commiting the code, make sure the validation from PyTest and pre-commit has been **SUCCESSFULL**.

After passing all the requirements, then you can commit the changes with these code

```bash
git add .
git commit -am "<commit_title>"
git push
```






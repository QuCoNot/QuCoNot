# Unit Testing with PyTest

This unit testing is made to make sure all the implementation is accurate. 

## PyTest Installation

Before running the unit testing, PyTest needs to be installed

```console
python -m pip install pytest
```

## Testing

To run all the test, go to root project and run below command

```console
python -m pytest
```

## Creating new Test file

For PyTest to automatically execute and test the file, we need to add "test\_" or "\_test" in the file name. Usually, we use "test\_" + "python_file_name".py. Also, the test function name usually is the same with the tested function, e,g. "test_function_name"

## Adding Testing Scenario

There are a couple of ways to add test case for PyTest, one of them is using the parametrize.

```python
@pytest.mark.parametrize(
    "controls_no, max_ancilla, expected_cases",
    [
        pytest.param(
            5, 1, 0, id="not-enough-ancilla"
        ),
        pytest.param(
            5, 3, 1, id="one-case"
        )
    ],
)
def test_generate_mct_cases(controls_no, max_ancilla, expected_cases):
```

For the above example, it means that the "test_generate_mct_cases" will be executed twice with the given parameters. 

The first one is controls_no = 5, max_ancilla = 1, expected_cases = 0 and with the label "not-enough-ancilla". 

The second one is controls_no = 5, max_ancilla = 3, expected_cases = 1 and with the label "one-case".



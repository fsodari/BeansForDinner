## Set up a python virtualenvironment

    python3 -m venv vbeans

## Install all requirements

    pip install -r requirements.txt

## Run the tests
    # Run all tests
    pytest

    # Run individual tests
    pytest tests/test_atomic.py --log-file=logs/tests/atomic.log

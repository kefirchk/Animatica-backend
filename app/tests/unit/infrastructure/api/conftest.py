import json
import os

import pytest

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")


@pytest.fixture
def file_data():
    with open(TEST_DATA_DIR + "/some_file.json") as file:
        return json.load(file)

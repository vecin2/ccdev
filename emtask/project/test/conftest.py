import pytest

from emtasktest.testutils import sample_project


@pytest.fixture
def emproject():
    emproject = sample_project()
    yield emproject

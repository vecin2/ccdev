import pytest

from emtask.ced.tool import CED
from emtasktest.testutils import sample_project


@pytest.fixture
def ced():
    ced = CED(sample_project().get_repo())
    yield ced

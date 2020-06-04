import pytest

from emtask.ced.tool import CED, MultiRootCED
from emtasktest.testutils import sample_product, sample_project


@pytest.fixture
def ced():
    ced = MultiRootCED(sample_project().get_repo(), sample_project().get_product_repo())
    yield ced


@pytest.fixture
def product_ced():
    ced = CED(sample_product().get_repo())
    yield ced

import pytest


@pytest.fixture(scope="session")
def data_path(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data")
    return fn

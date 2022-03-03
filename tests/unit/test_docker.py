import pytest

# TODO: what do we even want to check here?
@pytest.mark.skip(reason="needs a mechanism to target scm tagged images")
@pytest.mark.docker_required
def test_one(docker_client):
    docker_client.images.list()

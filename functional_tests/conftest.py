import os

import pytest

# Solution from playwright-pytest issues: https://github.com/microsoft/playwright-pytest/issues/29
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


# This pytest fixture is currently not required. From my current understanding
# the live_server fixture from pytest-django can be passed directly as a test function
# arguement.
@pytest.fixture(scope="session", name="server_url")
def get_server_url(live_server):
    """Start a django server to test against and return the url of the server."""
    if staging_server := os.environ.get("STAGING_SERVER"):
        yield f"http://{staging_server}"
    else:
        yield live_server.url

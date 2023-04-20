import os

import pytest

# Solution from playwright-pytest issues: https://github.com/microsoft/playwright-pytest/issues/29
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture(scope="session", name="server_url")
def get_server_url(live_server):
    """Start a django server to test against and return the url of the server."""
    yield live_server.url

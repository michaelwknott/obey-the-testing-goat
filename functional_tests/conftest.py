import os

import pytest
from playwright.sync_api import Page

# Solution from playwright-pytest issues: https://github.com/microsoft/playwright-pytest/issues/29
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture(scope="session", name="server_url")
def get_server_url(live_server):
    """Start a server to test against and return the url of the server.

    Return a server url to test against. If the environment variable
    STAGING_SERVER is set, then the url will be the staging server. Otherwise
    the url will be the live_server.url.
    """

    staging_server = os.environ.get("STAGING_SERVER")
    if staging_server:
        yield f"http://{staging_server}"
    else:
        yield live_server.url

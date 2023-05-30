import pytest
from playwright.sync_api import Browser
from playwright.sync_api import Page
from playwright.sync_api import expect


def test_cannot_add_empty_list_items():
    # Edith goes to the home page and accidently tries to submit an empty list item.
    # She hits Enter on the empty input box

    # The home page refreshes, and there is an error message saying that list items
    # cannot be blank

    # She tries again with some text for the item, which now workss

    # Perversely, she now decides to submit another blank list item

    # She recieves a similar warning on the list page

    # And she can correct it by filling some text in

    pytest.fail("write the test!")

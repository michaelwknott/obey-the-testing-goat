import pytest
from playwright.sync_api import Browser
from playwright.sync_api import Page
from playwright.sync_api import expect


def test_cannot_add_empty_list_items(server_url: str, page: Page):
    # Edith goes to the home page and accidently tries to submit an empty list item.
    # She hits Enter on the empty input box
    page.goto(server_url)
    inputbox = page.locator("#id_new_item")
    inputbox.press("Enter")

    # The home page refreshes, and there is an error message saying that list items
    # cannot be blank
    page.wait_for_load_state("domcontentloaded")
    error_text = page.locator(".has-error")
    expect(error_text).to_contain_text("You can't have an empty list item!")

    # She tries again with some text for the item, which now workss
    inputbox.fill("Buy milk")
    inputbox.press("Enter")

    table = page.locator("#id_list_table")
    expect(table).to_be_visible()
    expect(table).to_contain_text("1: Buy milk")

    # Perversely, she now decides to submit another blank list item
    inputbox.press("Enter")
    # She recieves a similar warning on the list page
    page.wait_for_load_state("domcontentloaded")
    error_text = page.locator(".is-valid")
    expect(error_text).to_contain_text("You can't have an empty list item!")

    # And she can correct it by filling some text in
    inputbox.fill("Buy tea")
    inputbox.press("Enter")
    expect(table).to_contain_text("1: Buy milk")
    expect(table).to_contain_text("2: Buy tea")

    pytest.fail("Finish writing the test!")

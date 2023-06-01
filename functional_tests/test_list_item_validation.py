from playwright.sync_api import Page
from playwright.sync_api import expect


def test_cannot_add_empty_list_items(server_url: str, page: Page):
    # Edith goes to the home page and accidently tries to submit an empty list item.
    # She hits Enter on the empty input box
    page.goto(server_url)
    inputbox = page.locator("#id_text")
    inputbox.press("Enter")

    # The browser intercepts the request, and does not load the list page
    page.wait_for_selector("#id_text:invalid")

    # She starts typing some text for the new item and the error disappears
    inputbox.fill("Buy milk")
    page.wait_for_selector("#id_text:valid")

    # And she can submit it successfully
    inputbox.press("Enter")
    table = page.locator("#id_list_table")
    expect(table).to_be_visible()
    expect(table).to_contain_text("1: Buy milk")

    # Perversely, she now decides to submit another blank list item
    inputbox.press("Enter")

    # Again the browser will not comply
    expect(table).to_contain_text("1: Buy milk")
    page.wait_for_selector("#id_text:invalid")

    # And she can correct it by filling some text in
    inputbox.fill("Buy tea")
    page.wait_for_selector("#id_text:valid")
    inputbox.press("Enter")
    expect(table).to_contain_text("1: Buy milk")
    expect(table).to_contain_text("2: Buy tea")

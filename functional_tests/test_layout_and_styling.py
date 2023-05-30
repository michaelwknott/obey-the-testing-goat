from playwright.sync_api import Page
from playwright.sync_api import expect


def test_layout_and_styling(server_url: str, page: Page) -> None:
    # Edith goes to the home page
    page.goto(server_url)

    # She notices the input box is nicely centered
    inputbox = page.locator("h1")
    expect(inputbox).to_have_css("color", "rgb(65, 105, 225)")

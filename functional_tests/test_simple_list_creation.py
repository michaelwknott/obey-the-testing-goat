import re

import pytest
from playwright.sync_api import Browser
from playwright.sync_api import Page
from playwright.sync_api import expect


def test_can_start_a_list_for_one_user(server_url: str, page: Page) -> None:
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    page.goto(server_url)

    # She notices the page title and header mention to-do lists
    expect(page).to_have_title("To-Do lists")
    header_text = page.locator("h1")
    first_header_text = header_text.first
    expect(first_header_text).to_have_text("Start a new To-Do list")

    # She is invited to enter a to-do item straight away
    inputbox = page.locator("#id_text")
    expect(inputbox).to_have_attribute("placeholder", "Enter a to-do item")

    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
    inputbox.fill("Buy peacock feathers")

    # When she hits enter, the page updates, and now the page lists
    # "1: Buy peacock feathers to make a fly"
    inputbox.press("Enter")

    table = page.locator("#id_list_table")
    expect(table).to_be_visible()

    expect(table).to_contain_text("1: Buy peacock feathers")

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    inputbox.fill("Use peacock feathers to make a fly")
    inputbox.press("Enter")

    # The page updates again, and now shows both items on her list
    expect(table).to_contain_text("2: Use peacock feathers to make a fly")

    # Satisfied, she goes back to sleep
    page.close()


def test_multiple_users_can_start_lists_at_different_urls(
    server_url: str, browser: Browser
) -> None:
    # Edith starts a new to-do list
    edith_context = browser.new_context()
    # create a new page inside context.
    edith_page = edith_context.new_page()
    edith_page.goto(server_url)

    inputbox = edith_page.locator("#id_text")
    inputbox.fill("Buy peacock feathers")
    inputbox.press("Enter")

    table = edith_page.locator("#id_list_table")
    expect(table).to_contain_text("1: Buy peacock feathers")

    # She notices that her list has a unique URL
    expect(edith_page).to_have_url(re.compile(r"/lists/.+"))

    # Now a new user, Francis, comes along to the site.
    # We use a new browser session to make sure that no information of Edith's
    # is coming through from cookies etc
    francis_context = browser.new_context()
    francis_page = francis_context.new_page()

    # Francis visits the home page. There is no sign of Edith's list
    francis_page.goto(server_url)
    page_text = francis_page.locator("body")

    expect(page_text).not_to_contain_text("Buy peacock feathers")
    expect(page_text).not_to_contain_text("make a fly")

    # Francis starts a new list by entering a new item. He
    # is less interesting than Edith...
    inputbox = francis_page.locator("#id_text")
    inputbox.fill("Buy milk")
    inputbox.press("Enter")

    table = francis_page.locator("#id_list_table")
    expect(table).to_contain_text("1: Buy milk")

    # Francis gets his own unique URL
    expect(francis_page).to_have_url(re.compile(r"/lists/.+"))
    expect(francis_page).not_to_have_url(edith_page.url)

    # Again, there is no trace of Edith's list
    page_text = francis_page.locator("body")
    expect(page_text).not_to_contain_text("Buy peacock feathers")
    expect(page_text).not_to_contain_text("make a fly")

    # Satisfied, they both go back to sleep
    edith_context.close()
    francis_context.close()

    browser.close()

import pytest
from playwright.sync_api import Page
from playwright.sync_api import expect


def check_for_row_in_list_table(page: Page, row_text: str):
    table = page.locator("#id_list_table")
    rows = table.locator("tr > td")
    expect(rows).to_have_text(row_text)


def test_can_start_a_list_and_retrieve_it_later(page: Page):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage. She notices the page title and
    # header mention to-do lists
    page.goto("http://127.0.0.1:8000/")
    expect(page).to_have_title("To-Do lists")
    header_text = page.locator("h1")
    first_header_text = header_text.first
    expect(first_header_text).to_have_text("To-Do list")

    # She is invited to enter a to-do item straight away
    inputbox = page.locator("#id_new_item")
    expect(inputbox).to_have_attribute("placeholder", "Enter a to-do item")

    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
    inputbox.fill("Buy peacock feathers")

    # When she hits enter, the page updates, and now the page lists
    # "1: Buy peacock feathers to make a fly"
    inputbox.press("Enter")

    table = page.locator("#id_list_table")
    expect(table).to_be_visible()
    
    check_for_row_in_list_table(page, "1: Buy peacock feathers")

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    inputbox.fill("Use peacock feathers to make a fly")
    inputbox.press("Enter")

    # The page updates again, and now shows both items on her list
    check_for_row_in_list_table(page, "2: Use peacock feathers to make a fly")

    page.close()
    pytest.fail("Finish the test!")

    # Edith wonders whether the site will remember her list. Then she sees
    # htta the site has generated a unique url for her -- there is some
    # explanatory text to that effect.

    # She visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep

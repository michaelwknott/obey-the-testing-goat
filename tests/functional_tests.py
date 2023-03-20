from playwright.sync_api import Page, expect


# Edith has heard about a cool new online to-do app. She goes
# to check out its homepage. She notices the page title and
# header mention to-do lists

def test_homepage_has_correct_title(page: Page):
    page.goto("http://127.0.0.1:8000/")
    expect(page).to_have_title("To-Do")
    page.close()

# She is invited to enter a to-do item straight away

# She types "Buy peacock feathers" into a text box (Edith's hobby
# is tying fly-fishing lures)

# When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers to make a fly"

# There is still a text box inviting her to add another item. She
# enters "Use peacock feathers to make a fly" (Edith is very methodical)

# The page updates again, and now shows both items on her list

# Edith wonders whether the site will remember her list. Then she sees
# htta the site has generated a unique url for her -- there is some
# explanatory text to that effect.

# She visits that URL - her to-do list is still there.

# Satisfied, she goes back to sleep

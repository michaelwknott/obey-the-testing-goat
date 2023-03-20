import re
from playwright.sync_api import Page, expect

def test_homepage_has_Congratulations_in_title(page: Page):
    page.goto("http://127.0.0.1:8000/")

    expect(page).to_have_title(re.compile("Congratulations"))
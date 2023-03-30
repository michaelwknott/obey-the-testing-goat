
def test_home_page_returns_correct_html(client):
    response = client.get("/")
    html = response.content.decode("utf8")
    assert html.startswith("<html>")
    assert html.endswith("</html>")
    assert "<title>To-Do lists</title>" in html

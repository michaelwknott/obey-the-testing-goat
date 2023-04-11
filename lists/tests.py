
def test_uses_home_page_template(client):
    response = client.get("/")
    assert response.templates[0].name == "home.html"

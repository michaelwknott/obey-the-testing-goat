def test_uses_home_page_template(client):
    response = client.get("/")
    assert response.templates[0].name == "home.html"


def test_can_save_a_POST_request(client):
    response = client.post("/", data={"item_text": "A new list item"})
    assert "A new list item" in response.content.decode()

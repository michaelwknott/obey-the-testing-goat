import pytest

from lists.models import Item
from lists.models import List


@pytest.mark.django_db
def test_uses_home_page_template(client):
    response = client.get("/")

    assert response.templates[0].name == "home.html"


@pytest.mark.django_db
def test_can_save_a_POST_request(client):
    client.post("/lists/new", data={"item_text": "A new list item"})
    assert Item.objects.count() == 1

    new_item = Item.objects.first()
    assert new_item.text == "A new list item"


@pytest.mark.django_db
def test_redirects_after_POST(client):
    response = client.post("/lists/new", data={"item_text": "A new list item"})
    new_list = List.objects.first()
    assert response.status_code == 302
    assert response["location"] == f"/lists/{new_list.id}/"


@pytest.mark.django_db
def test_saving_and_retrieving_items(client):
    list_ = List()
    list_.save()

    first_item = Item()
    first_item.text = "The first (ever) list item"
    first_item.list = list_
    first_item.save()

    second_item = Item()
    second_item.text = "Item the second"
    second_item.list = list_
    second_item.save()

    saved_list = List.objects.first()
    assert saved_list == list_

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    assert first_saved_item.text == "The first (ever) list item"
    assert first_saved_item.list == list_
    assert second_saved_item.text == "Item the second"
    assert second_saved_item.list == list_


@pytest.mark.django_db
def test_only_saves_items_when_necessary(client):
    client.get("/")

    assert Item.objects.count() == 0


@pytest.mark.django_db
def test_uses_list_template(client):
    list_ = List.objects.create()
    response = client.get(f"/lists/{list_.id}/")

    assert response.templates[0].name == "list.html"


@pytest.mark.django_db
def test_displays_only_items_for_that_list(client):
    correct_list = List.objects.create()
    Item.objects.create(text="itemey 1", list=correct_list)
    Item.objects.create(text="itemey 2", list=correct_list)

    other_list = List.objects.create()
    Item.objects.create(text="other list item 1", list=other_list)
    Item.objects.create(text="other list item 2", list=other_list)

    response = client.get(f"/lists/{correct_list.id}/")

    assert "itemey 1" in response.content.decode()
    assert "itemey 2" in response.content.decode()
    assert "other list item 1" not in response.content.decode()
    assert "other list item 2" not in response.content.decode()


@pytest.mark.django_db
def test_can_save_a_POST_request_to_an_existing_list(client):
    other_list = List.objects.create()  # noqa: F841
    correct_list = List.objects.create()

    client.post(
        f"/lists/{correct_list.id}/add_item",
        data={"item_text": "A new item for an existing list"},
    )

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new item for an existing list"
    assert new_item.list == correct_list


@pytest.mark.django_db
def test_redirects_to_list_view(client):
    other_list = List.objects.create()  # noqa: F841
    correct_list = List.objects.create()

    response = client.post(
        f"/lists/{correct_list.id}/add_item",
        data={"item_text": "A new item for an existing list"},
    )

    assert response.status_code == 302
    assert response["location"] == f"/lists/{correct_list.id}/"


@pytest.mark.django_db
def test_passes_correct_list_to_template(client):
    other_list = List.objects.create()  # noqa: F841
    correct_list = List.objects.create()

    response = client.get(f"/lists/{correct_list.id}/")

    assert response.context["list"] == correct_list
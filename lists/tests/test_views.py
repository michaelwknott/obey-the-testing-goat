import pytest
from django.utils.html import escape

from lists.forms import DUPLICATE_ITEM_ERROR
from lists.forms import EMPTY_ITEM_ERROR
from lists.forms import ExistingListItemForm
from lists.forms import ItemForm
from lists.models import Item
from lists.models import List


@pytest.mark.django_db
def test_uses_home_page_template(client):
    response = client.get("/")

    assert response.templates[0].name == "home.html"


def test_home_page_uses_items_form(client):
    response = client.get("/")
    assert isinstance(response.context["form"], ItemForm)


@pytest.mark.django_db
def test_can_save_a_POST_request(client):
    client.post("/lists/new", data={"text": "A new list item"})
    assert Item.objects.count() == 1

    new_item = Item.objects.first()
    assert new_item.text == "A new list item"


@pytest.mark.django_db
def test_redirects_after_POST(client):
    response = client.post("/lists/new", data={"text": "A new list item"})
    new_list = List.objects.first()
    assert response.status_code == 302
    assert response["location"] == f"/lists/{new_list.id}/"


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
        f"/lists/{correct_list.id}/",
        data={"text": "A new item for an existing list"},
    )

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new item for an existing list"
    assert new_item.list == correct_list


@pytest.mark.django_db
def test_POST_redirects_to_list_view(client):
    other_list = List.objects.create()  # noqa: F841
    correct_list = List.objects.create()

    response = client.post(
        f"/lists/{correct_list.id}/",
        data={"text": "A new item for an existing list"},
    )

    assert response.status_code == 302
    assert response["location"] == f"/lists/{correct_list.id}/"


@pytest.mark.django_db
def test_passes_correct_list_to_template(client):
    other_list = List.objects.create()  # noqa: F841
    correct_list = List.objects.create()

    response = client.get(f"/lists/{correct_list.id}/")

    assert response.context["list"] == correct_list


@pytest.mark.django_db
def test_for_invalid_input_renders_home_template(client):
    response = client.post("/lists/new", data={"text": ""})

    assert response.status_code == 200
    assert response.templates[0].name == "home.html"


@pytest.mark.django_db
def test_validation_errors_are_shown_on_home_page(client):
    response = client.post("/lists/new", data={"text": ""})
    expected_error = escape(EMPTY_ITEM_ERROR)

    assert expected_error in response.content.decode()


@pytest.mark.django_db
def test_invalid_list_items_arent_saved(client):
    client.post("/lists/new", data={"text": ""})
    assert List.objects.count() == 0
    assert Item.objects.count() == 0


@pytest.mark.django_db
def test_validation_errors_end_up_on_lists_page(client):
    list_ = List.objects.create()
    response = client.post(f"/lists/{list_.id}/", data={"text": ""})

    assert response.status_code == 200
    assert response.templates[0].name == "list.html"

    expected_error = escape("You can't have an empty list item!")

    assert expected_error in response.content.decode()


@pytest.mark.django_db
def test_displays_item_form(client):
    list_ = List.objects.create()
    response = client.get(f"/lists/{list_.id}/")

    assert isinstance(response.context["form"], ExistingListItemForm)
    assert 'name="text"' in response.content.decode()


@pytest.mark.django_db
def test_for_invalid_input(client):
    list_ = List.objects.create()
    client.post(f"/lists/{list_.id}/", data={"text": ""})

    assert Item.objects.count() == 0


@pytest.mark.django_db
def test_for_invalid_input_renders_list_template(client):
    list_ = List.objects.create()
    response = client.post(f"/lists/{list_.id}/", data={"text": ""})

    assert response.status_code == 200
    assert response.templates[0].name == "list.html"
    

@pytest.mark.django_db
def test_for_invalid_input_passes_form_to_template(client):
    list_ = List.objects.create()
    response = client.post(f"/lists/{list_.id}/", data={"text": ""})

    assert isinstance(response.context["form"], ExistingListItemForm)


@pytest.mark.django_db
def test_for_invalid_input_shows_error_on_page(client):
    list_ = List.objects.create()
    response = client.post(f"/lists/{list_.id}/", data={"text": ""})

    assert escape(EMPTY_ITEM_ERROR) in response.content.decode()


@pytest.mark.django_db
def test_duplicate_item_validation_errors_end_up_on_lists_page(client):
    list_ = List.objects.create()
    item1 = Item.objects.create(list=list_, text="textey")
    response = client.post(f"/lists/{list_.id}/", data={"text": "textey"})

    expected_error = escape(DUPLICATE_ITEM_ERROR)

    assert expected_error in response.content.decode()
    assert response.templates[0].name == "list.html"
    assert Item.objects.all().count() == 1
    assert Item.objects.all().count() == 1

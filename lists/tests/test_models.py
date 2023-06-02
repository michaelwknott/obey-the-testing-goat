import pytest
from django.core.exceptions import ValidationError

from lists.models import Item
from lists.models import List


@pytest.mark.django_db
def test_default_text(client):
    item = Item()
    assert item.text == ""


@pytest.mark.django_db
def testitem_is_related_to_list(client):
    list_ = List.objects.create()
    item = Item()
    item.list = list_
    item.save()
    assert item in list_.items.all()


@pytest.mark.django_db
def test_cannot_save_empty_list_items(client):
    list_ = List.objects.create()
    item = Item(list=list_, text="")
    with pytest.raises(ValidationError):
        item.save()
        item.full_clean()


@pytest.mark.django_db
def test_duplicate_items_are_invalid(client):
    list_ = List.objects.create()
    Item.objects.create(list=list_, text="bla")

    with pytest.raises(ValidationError):
        item = Item(list=list_, text="bla")
        item.full_clean()


@pytest.mark.django_db
def test_can_save_same_item_to_different_list(client):
    list1 = List.objects.create()
    list2 = List.objects.create()
    Item.objects.create(list=list1, text="bla")
    item = Item(list=list2, text="bla")
    item.full_clean()  # should not raise


@pytest.mark.django_db
def test_list_ordering(client):
    list1 = List.objects.create()
    item1 = Item.objects.create(list=list1, text="i1")
    item2 = Item.objects.create(list=list1, text="item 2")
    item3 = Item.objects.create(list=list1, text="3")

    assert list(Item.objects.all()) == [item1, item2, item3]


@pytest.mark.django_db
def test_get_absolute_url(client):
    list_ = List.objects.create()
    assert list_.get_absolute_url() == f"/lists/{list_.id}/"

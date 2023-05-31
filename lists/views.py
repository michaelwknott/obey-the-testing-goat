from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.shortcuts import render

from lists.models import Item
from lists.models import List


def home_page(request):
    return render(request, "home.html")


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": list_})


def new_list(request):
    list_ = List.objects.create()
    new_item_text = request.POST["item_text"]
    item = Item.objects.create(text=new_item_text, list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item!"
        return render(request, "home.html", {"error": error})
    return redirect(f"/lists/{list_.id}/")


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/lists/{list_.id}/")

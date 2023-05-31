from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.shortcuts import render

from lists.models import Item
from lists.models import List


def home_page(request):
    return render(request, "home.html")


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == "POST":
        try:
            item = Item(text=request.POST["item_text"], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item!"

    return render(request, "list.html", {"list": list_, "error": error})


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
    return redirect(list_)

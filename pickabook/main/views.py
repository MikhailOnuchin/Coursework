from django.shortcuts import render
from .models import *
from .separated_views.auth_views import *


def main_page(request):
    tops = Top.objects.all()
    personal = []
    return render(request, 'main/main_page.html', {'tops': tops,
                                                   'personal': personal})


def top_page(request, top_id):
    top = Top.objects.get(id=top_id)
    return render(request, 'main/top_page.html', {'top': top})


def book_page(request, book_id):
    book = Book.objects.get(id=book_id)
    user = request.user
    is_recommended = False
    is_favourite = user.is_authenticated and (book in user.favourites())
    is_in_wish_list = user.is_authenticated and (book in user.wish_list())
    is_finished = user.is_authenticated and (book in user.finished())
    reviews = Review.objects.filter(book=book)
    return render(request, 'main/book_page.html', {'book': book,
                                                   'is_recommended': is_recommended,
                                                   'is_favourite': is_favourite,
                                                   'is_in_wish_list': is_in_wish_list,
                                                   'is_finished': is_finished,
                                                   'top_list': book.top_list(),
                                                   'reviews': reviews})


def test(request):
    return render(request, 'main/test.html', {'scripts': ['a', 'b']})

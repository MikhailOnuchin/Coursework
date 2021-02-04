from django.shortcuts import render
from .models import *


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
    is_recommended = False
    is_favourite = False
    is_in_wish_list = False
    is_finished = False
    reviews = Review.objects.filter(book=book)
    return render(request, 'main/book_page/html', {'book': book,
                                                   'is_recommended': is_recommended,
                                                   'is_favourite': is_favourite,
                                                   'is_in_wish_list': is_in_wish_list,
                                                   'is_finished': is_finished,
                                                   'top_list': book.top_list(),
                                                   'reviews': reviews})

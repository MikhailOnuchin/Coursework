# coding=windows-1251
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..complementary.recommendation_scripts.count_value import recommendation_positive, recommendation_negative, thread_recommendations
from ..decorators import xhr_required
from ..models import Book, RecommendationBinder, Review


def book_page(request, book_id):
    book = Book.objects.get(id=book_id)
    book.count_rating()
    user = request.user
    is_recommended = False
    if user.is_authenticated:
        try:
            b = RecommendationBinder.objects.get(user=user, book=book)
            is_recommended = b in RecommendationBinder.objects.filter(user=request.user).order_by('-value')[:100]
        except RecommendationBinder.DoesNotExist:
            pass
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
                                                   'reviews': reviews,
                                                   'scripts': ['book_script']})


def _get_parameters(request):
    user = request.user
    book_id = request.POST.get('book_id')
    book = Book.objects.get(id=book_id)
    return user, book


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def make_favourite(request):
    user, book = _get_parameters(request)
    if user.favourites.add(book):
        recommendation_positive(book, user)
    return HttpResponse('ok')


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def make_unfavourite(request):
    user, book = _get_parameters(request)
    if user.favourites.remove(book):
        recommendation_negative(book, user)
    return HttpResponse('ok')


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def make_finished(request):
    user, book = _get_parameters(request)
    user.wish_list.remove(book)
    user.finished.add(book)
    return HttpResponse('ok')


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def make_unfinished(request):
    user, book = _get_parameters(request)
    user.finished.remove(book)
    return HttpResponse('ok')


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def make_wanted(request):
    user, book = _get_parameters(request)
    user.finished.remove(book)
    user.wish_list.add(book)
    return HttpResponse('ok')


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def make_unwanted(request):
    user, book = _get_parameters(request)
    user.wish_list.remove(book)
    return HttpResponse('ok')


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def get_review(request):
    text = request.POST.get('text')
    rating = request.POST.get('rating')
    book_id = request.POST.get('book_id')
    book = Book.objects.get(id=book_id)
    r = Review()
    r.text = text
    r.rating = rating
    r.book = book
    r.author = request.user
    r.save()
    return HttpResponse('ok')


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def positive_recommendation(request):
    book_id = request.POST.get('book_id')
    book = Book.objects.get(id=book_id)
    recommendation_positive(book, request.user)
    thread_recommendations(request.user)
    return HttpResponse('ok')


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def negative_recommendation(request):
    book_id = request.POST.get('book_id')
    book = Book.objects.get(id=book_id)
    recommendation_negative(book, request.user)
    thread_recommendations(request.user)
    return HttpResponse('ok')

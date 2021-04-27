# coding=windows-1251
from threading import Thread
from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import xhr_required
from .models import *
from .separated_views.auth_views import *
from .complementary.recommendation_scripts.check_preferences import check_user
from .complementary.recommendation_scripts.count_value import recommendation_positive, update_recommendations
import json


def preferences_set(user):
    preferences = json.loads(user.preferences)
    for tag in preferences.keys():
        if preferences[tag][0] != 0:
            return True
    return False


def main_page(request):
    tops = Top.objects.all()
    personal = []
    can_recommend = False
    if request.user.is_authenticated:
        can_recommend = preferences_set(request.user)
        if can_recommend:
            personal = [binder.book for binder in RecommendationBinder.objects.filter(user=request.user).order_by('-value')[:100]]
    return render(request, 'main/main_page.html', {'tops': tops,
                                                   'personal': personal,
                                                   'can_recommend': can_recommend})


def top_page(request, top_id):
    top = Top.objects.get(id=top_id)
    return render(request, 'main/top_page.html', {'top': top})


def book_page(request, book_id):
    book = Book.objects.get(id=book_id)
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
                                                   'reviews': reviews})


def weights_list(weights):
    res = []
    for tag in weights.keys():
        res.append({'name': tag, 'status': weights[tag][0]})
    res.sort(key=lambda x: x['name'])
    return res


@login_required(login_url='login', redirect_field_name=None)
def profile_page(request):
    tags = weights_list(json.loads(request.user.preferences))
    return render(request, 'main/profile_page.html', {'tags': tags, 'scripts': ['profile_script']})


positive_base = 5
negative_base = -50


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def set_preferences(request):
    preferences = json.loads(request.POST.get('preferences'))
    print(preferences)
    user = request.user
    check_user(user)
    weights = json.loads(user.preferences)
    for tag in weights.keys():
        weights[tag] = [0, 0]
    for tag in preferences['positive']:
        weights[tag] = [1, positive_base]
    for tag in preferences['negative']:
        weights[tag] = [-1, negative_base]
    user.preferences = json.dumps(weights, ensure_ascii=False)
    user.save()
    for book in user.favourites():
        recommendation_positive(book, user)
    t = Thread(target=update_recommendations, args=(user,))
    t.start()
    return HttpResponse('ok')


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def clear_preferences(request):
    user = request.user
    check_user(user)
    weights = json.loads(user.preferences)
    for tag in weights.keys():
        weights[tag] = [0, 0]
    user.preferences = json.dumps(weights, ensure_ascii=False)
    user.save()
    return HttpResponse('ok')


def remove_weights(preferences):
    res = {}
    preferences = json.loads(preferences)
    for tag in preferences.keys():
        res[tag] = preferences[tag][0]
    res = json.dumps(res, ensure_ascii=False)
    return res


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def get_preferences(request):
    preferences = remove_weights(request.user.preferences)
    return HttpResponse(preferences)


def test(request):
    return render(request, 'main/test.html', {'scripts': ['a', 'b']})

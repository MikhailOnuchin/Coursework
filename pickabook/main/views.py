# coding=windows-1251
from django.shortcuts import render
from .models import Top
from django.contrib.auth.decorators import login_required
from .separated_views.auth_views import *
from .separated_views.book_views import *
from .separated_views.profile_views import *


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
    return render(request, 'main/top_page.html', {'top': top,
                                                  'scripts': ['top_script']})


@login_required(login_url='login', redirect_field_name=None)
def personal_page(request):
    personal = [binder.book for binder in
                RecommendationBinder.objects.filter(user=request.user).order_by('-value')[:100]]
    return render(request, 'main/personal_page.html', {'personal': personal,
                                                       'scripts': ['top_script', 'personal_script']})


@login_required(login_url='login', redirect_field_name=None)
def favourite_page(request):
    return render(request, 'main/top_page.html', {'top': {'title': "Избранное",
                                                          'books': request.user.favourites()},
                                                  'scripts': ['top_script']})


@login_required(login_url='login', redirect_field_name=None)
def wish_list_page(request):
    return render(request, 'main/top_page.html', {'top': {'title': "Список желаний",
                                                          'books': request.user.wish_list()},
                                                  'scripts': ['top_script']})


@login_required(login_url='login', redirect_field_name=None)
def finished_page(request):
    return render(request, 'main/top_page.html', {'top': {'title': "Прочитанное",
                                                          'books': request.user.finished()},
                                                  'scripts': ['top_script']})


def blank(request):
    return HttpResponse('WIP')


def test(request):
    return render(request, 'main/test.html', {'scripts': ['a', 'b']})

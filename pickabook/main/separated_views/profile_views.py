# coding=windows-1251
from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from ..decorators import xhr_required
from ..complementary.recommendation_scripts.check_preferences import check_user
from ..complementary.recommendation_scripts.count_value import recommendation_positive, thread_recommendations
from ..recomendation_configs import positive_base, negative_base
import json


def weights_list(weights):
    res = []
    for tag in weights.keys():
        res.append({'name': tag, 'status': weights[tag][0]})
    res.sort(key=lambda x: x['name'])
    return res


@login_required(login_url='login', redirect_field_name=None)
def profile_page(request):
    tags = weights_list(json.loads(request.user.preferences))
    return render(request, 'main/profile_page.html', {'tags': tags,
                                                      'scripts': ['profile_script']})


@login_required(login_url='login', redirect_field_name=None)
@xhr_required
def set_preferences(request):
    preferences = json.loads(request.POST.get('preferences'))
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
    thread_recommendations(user)
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

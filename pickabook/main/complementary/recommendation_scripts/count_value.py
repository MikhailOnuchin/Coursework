# coding=windows-1251
from ...models import BookUserBinder, Book, RecommendationBinder
import json
from django.db import transaction


def count_value(book, user):
    b = BookUserBinder.objects.filter(user=user, book=book)
    val = 0
    if not b:
        weights = json.loads(user.preferences)
        used_tags = book.tags.all()
        for tag in used_tags:
            val += weights[tag.name][1]
    return val


positive_delta = 0.05
negative_delta = 0.05


def recommendation_positive(book, user):
    weights = json.loads(user.preferences)
    used_tags = book.tags.all()
    for tag in used_tags:
        weights[tag.name][1] += positive_delta
    user.preferences = json.dumps(weights, ensure_ascii=False)
    user.save()


def recommendation_negative(book, user):
    weights = json.loads(user.preferences)
    used_tags = book.tags.all()
    for tag in used_tags:
        weights[tag.name][1] -= negative_delta
    user.preferences = json.dumps(weights, ensure_ascii=False)
    user.save()


@transaction.atomic
def update_recommendations(user):
    books = Book.objects.all()
    for book in books:
        val = count_value(book, user)
        try:
            b = RecommendationBinder.objects.get(book=book, user=user)
        except RecommendationBinder.DoesNotExist:
            b = RecommendationBinder(book=book, user=user)
        b.value = val
        b.save()

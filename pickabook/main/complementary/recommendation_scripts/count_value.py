# coding=windows-1251
from ...models import BookUserBinder, Book, RecommendationBinder, Tag, ThreadRecord
import json
import threading
from ...recomendation_configs import positive_delta, negative_delta


def count_value(book, user):
    b = BookUserBinder.objects.filter(user=user, book=book)
    val = 0
    if not b:
        weights = json.loads(user.preferences)
        used_tags = book.tags.all()
        for tag in used_tags:
            val += weights[tag.name][1]
    return val


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


def update_recommendations(user):
    t = threading.currentThread()
    tr = ThreadRecord(user=user, thread=t.ident)
    tr.save()
    preferences = json.loads(user.preferences)
    positive = [Tag.objects.get(name=val) for val in list(preferences) if preferences[val][0] == 1]
    negative = [Tag.objects.get(name=val) for val in list(preferences) if preferences[val][0] == -1]
    books = Book.objects.exclude(tags__in=negative).filter(tags__in=positive).distinct()
    for book in books:
        if not t.do_run:
            break
        val = count_value(book, user)
        try:
            b = RecommendationBinder.objects.get(book=book, user=user)
        except RecommendationBinder.DoesNotExist:
            b = RecommendationBinder(book=book, user=user)
        b.value = val
        b.save()
    tr.delete()


def thread_recommendations(user):
    trs = ThreadRecord.objects.filter(user=user)
    ts = {}
    for thread in threading.enumerate():
        ts[thread.ident] = thread
    for tr in trs:
        try:
            thread = ts[tr.thread]
            thread.do_run = False
        except KeyError:
            pass
    t = threading.Thread(target=update_recommendations, args=(user,))
    t.do_run = True
    t.start()

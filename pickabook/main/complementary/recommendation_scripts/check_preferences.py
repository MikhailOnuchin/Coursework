# coding=windows-1251
from ...models import User, Tag
import json


def check_user(user):
    weights = json.loads(user.preferences)
    known_tags = weights.keys()
    for tag in Tag.objects.all():
        if tag.name not in known_tags:
            weights[tag.name] = [0, 0]
    user.preferences = json.dumps(weights, ensure_ascii=False)
    user.save()


def check_all():
    for user in User.objects.all():
        check_user(user)
        print(user.username)

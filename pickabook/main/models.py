from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class UserBookOperator:
    def __init__(self, user, binder):
        self.user = user
        self.binder = binder

    def __call__(self):
        b = []
        binders = self.binder.objects.filter(user=self.user).order_by('-date')
        for binder in binders:
            b.append(binder.book)
        return b

    def add(self, book):
        binders = self.binder.objects.filter(book=book, user=self.user)
        if not binders:
            new_binder = self.binder(book=book, user=self.user, date=datetime.datetime.now())
            new_binder.save()
            return 1

    def remove(self, book):
        binders = self.binder.objects.filter(book=book, user=self.user)
        if binders:
            binders.delete()
            return 1


class Tag(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    cover = models.CharField(max_length=100, default='main/covers/default.png')
    tags = models.ManyToManyField(Tag)
    rating = models.FloatField(default=0)

    def top_list(self):
        t = []
        binders = BookTopBinder.objects.filter(book=self)
        for binder in binders:
            t.append(binder.top)
        return t

    def count_rating(self):
        reviews = Review.objects.filter(book=self)
        if reviews:
            s = 0
            for review in reviews:
                s += review.rating
            self.rating = round(s / len(reviews), 1)
        else:
            self.rating = 0
        self.save()

    def __str__(self):
        return self.author + ' - ' + self.title


class Top(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=100)
    show_on_main = models.BooleanField(default=False)

    def fix_order(self):
        binders = BookTopBinder.objects.filter(top=self).order_by('order')
        i = 0
        for binder in binders:
            if binder.order != i:
                binder.order = i
                binder.save()
            i += 1

    def add_book(self, book, place=None):
        binders = BookTopBinder.objects.filter(book=book, top=self)
        if not binders:
            binders = BookTopBinder.objects.filter(top=self).order_by('order')
            new_binder = BookTopBinder(book=book, top=self)
            if binders:
                if place is None or place > len(binders):
                    place = len(binders)
                else:
                    for binder in binders:
                        if binder.order >= place:
                            binder.order += 1
                            binder.save()
                new_binder.order = place
            new_binder.save()

    def remove_book(self, book):
        binders = BookTopBinder.objects.filter(book=book, top=self)
        if binders:
            binders.delete()
            self.fix_order()

    @property
    def books(self):
        b = []
        self.fix_order()
        binders = BookTopBinder.objects.filter(top=self).order_by('order')
        for binder in binders:
            b.append(binder.book)
        return b

    def __iter__(self):
        return iter(self.books)

    def __len__(self):
        return len(self.books)

    def __str__(self):
        return self.title


class BookTopBinder(models.Model):
    objects = models.Manager()

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    top = models.ForeignKey(Top, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.top) + "(" + str(self.order) + ") -- " + str(self.book)


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='default.png')
    preferences = models.TextField(default='{}')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.favourites = UserBookOperator(self, FavouriteBookBinder)
        self.wish_list = UserBookOperator(self, WishListBookBinder)
        self.finished = UserBookOperator(self, FinishedBookBinder)


class RecommendationBinder(models.Model):
    objects = models.Manager()

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return str(self.user) + ' -rec- ' + str(self.book) + ' --- ' + str(self.value)


class BookUserBinder(models.Model):
    objects = models.Manager()

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.user) + ' -@- ' + str(self.book)


class FavouriteBookBinder(BookUserBinder):
    def __str__(self):
        return str(self.user) + ' *favourite* ' + str(self.book)


class WishListBookBinder(BookUserBinder):
    def __str__(self):
        return str(self.book) + ' *wish list* ' + str(self.book)


class FinishedBookBinder(BookUserBinder):
    def __str__(self):
        return str(self.user) + ' *finished* ' + str(self.book)


class Review(models.Model):
    objects = models.Manager()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return str(self.author) + " @ " + str(self.book)


class ThreadRecord(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.IntegerField(null=True)

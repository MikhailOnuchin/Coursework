from django.db import models
from django.contrib.auth.models import AbstractUser


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
    cover = models.ImageField(upload_to='covers/', default='default.png')
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=10)

    def top_list(self):
        t = []
        binders = BookTopBinder.objects.filter(book=self)
        for binder in binders:
            t.append(binder.top)
        return t

    def __str__(self):
        return self.author + ' - ' + self.title


class Top(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=100)

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

    def books(self):
        b = []
        self.fix_order()
        binders = BookTopBinder.objects.filter(top=self).order_by('order')
        for binder in binders:
            b.append(binder.book)
        return b

    def __iter__(self):
        return iter(self.books())

    def __len__(self):
        return len(self.books())

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

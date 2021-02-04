from django.contrib import admin
from .models import *


admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(Top)
admin.site.register(BookTopBinder)
admin.site.register(User)
admin.site.register(BookUserBinder)
admin.site.register(FavouriteBookBinder)
admin.site.register(WishListBookBinder)
admin.site.register(FinishedBookBinder)
admin.site.register(Review)

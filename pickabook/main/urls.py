from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('top/<int:top_id>', views.top_page, name='top_url'),
    path('book/<int:book_id>', views.book_page, name='book_url')
]

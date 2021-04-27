from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', views.main_page, name='main'),
    path('top/<int:top_id>', views.top_page, name='top_url'),
    path('book/<int:book_id>', views.book_page, name='book_url'),
    path('profile', views.profile_page, name='profile'),
    path('set-preferences', views.set_preferences, name='set_preferences'),
    path('clear-preferences', views.clear_preferences, name='clear_preferences'),
    path('get-preferences', views.get_preferences, name='get_preferences'),
    path('test', views.test)
]

authentication_patterns = [
    path('login', auth_views.LoginView.as_view(template_name='main/login_form.html', form_class=LoginForm,
                                               redirect_authenticated_user=True), name='login'),
    path('do-logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', views.RegistrationView.as_view(), name='register'),
]

urlpatterns += authentication_patterns
'''
path('reset', auth_views.PasswordResetView.as_view(template_name='main/password_reset_form.html', )),
path('done', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'),
     name='password_reset_done'),
re_path(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(success_url='/main',
                                                    template_name='main/password_reset_confirm.html'),
        name='password_reset_confirm'),
'''


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from ..models import *
from ..forms import *


class RegistrationView(View):
    form_class = RegistrationForm
    template_name = 'main/registration_form.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            form = self.form_class(request.POST, instance=request.user)
            if form.is_valid():
                user = form.save()
                user.save()
                login(request, user)
                print(request.user)
                return redirect('/main')
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.save()

                '''    
                if NEED_EMAIL:
                    send_mail(request, user)
                    return render(request, 'main/email_conf.html', {'email': user.email})
                else:
                    user.is_active = True
                    user.save()
                    login(request, user)
                    return redirect('/main')
                '''
        errors = form.errors
        print(list(errors.as_data()))
        return render(request, self.template_name, {'form': form})

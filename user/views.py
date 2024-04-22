from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
import service.user
from user.forms import LoginForm, CreateUserForm


class User(View):
    def get(self, *args, **kwargs):
        form = CreateUserForm()

        return render(self.request, template_name='user/create_user.html', context={'form': form})

    def post(self, *args, **kwargs):
        form = CreateUserForm(self.request.POST)
        if form.is_valid():
            response = service.user.User().create_user(form)

            if response['success']:
                return HttpResponseRedirect('/user/login')

        return render(self.request, template_name='user/create_user.html', context={'form': form})


class Login(View):
    def get(self, *args, **kwargs):
        form = LoginForm()

        return render(self.request, template_name='user/login.html', context={'form': form})

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            response = (service.user.Authentication(
                username=form.cleaned_data.get('username'),
                raw_password=form.cleaned_data.get('password')
            ).login(request=self.request))

            if response['success']:
                return HttpResponseRedirect('/')

        return render(self.request, template_name='user/login.html', context={'form': form})


class Logout(View):
    def get(self, *args, **kwargs):
        response = service.user.Authentication().logout(self.request)

        return HttpResponseRedirect('/')

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User as UserModel


class Authentication:
    def __init__(self, username=None, raw_password=None):
        self.user = None
        self.username = username
        self.raw_password = raw_password

    def login(self, request):
        if not self.username or not self.raw_password:
            raise Exception('Please provide both username and password')

        self.user = authenticate(username=self.username, password=self.raw_password)
        if not self.user:
            return {'success': False, 'description': 'User or password not found!', 'redirect': ''}

        login(request, self.user)

        response = {
            'success': True,
        }

        return response

    def logout(self, request):
        logout(request)

        return {'success': True}


class User:
    def __init__(self):
        pass

    def create_user(self, form):
        user = UserModel()
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.username = user.first_name.lower() + '.' + user.last_name.lower()
        user.set_password(form.cleaned_data['password'])
        user.email = form.cleaned_data['first_name'] + '@' + form.cleaned_data['last_name'] + '.com'

        user.save()

        response = {
            'success': True,
        }

        return response

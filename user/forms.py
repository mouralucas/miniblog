from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CreateUserForm(forms.Form):
    # username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
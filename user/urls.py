from django.urls import re_path, path
from user import views

urlpatterns = [
    re_path('^login$', views.Login.as_view(), name='login'),
    re_path('^logout$', views.Logout.as_view(), name='logout'),
    re_path('^new$', views.User.as_view(), name='new'),
]

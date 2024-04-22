from django.urls import re_path
from blog import views

urlpatterns = [
    re_path('^$', views.Feed.as_view(), name='feed'),
    re_path('^post/new$', views.CreatePost.as_view(), name='post'),
    re_path('^post/publish/draft$', views.PublishDraftPost.as_view(), name='publish_draft'),
    re_path('^post/comment/new$', views.Comment.as_view(), name='comment'),
    re_path('^post/delete$', views.DeletePost.as_view(), name='post_delete')
]

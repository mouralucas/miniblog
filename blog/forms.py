from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'status')


class CommentForm(forms.Form):
    content = forms.CharField(label='Your comment', widget=forms.Textarea(attrs={'class': 'form-control'}))

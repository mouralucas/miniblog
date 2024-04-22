from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
import service.blog
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from blog.forms import PostForm, CommentForm


class Feed(View):
    def get(self, *args, **kwargs):
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        response = service.blog.Blog().get_posts(user_id=user_id)

        # Render the landing page (feed)
        return render(self.request, template_name='blog/landing_page.html', context=response)


class UserPage(View):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):

        response = service.blog.Blog().get_user_posts(user_id=self.request.user.id)

        return render(self.request, template_name='blog/user_page.html', context=response)


class CreatePost(View):
    def get(self, *args, **kwargs):
        # Get the form to create a new post
        form = PostForm()

        # Render the page for new post with the form
        return render(self.request, template_name='blog/new_post.html', context={'form': form})

    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        # Get and validate the post form
        form = PostForm(self.request.POST)
        if form.is_valid():
            response = service.blog.Blog().create_post(form, user=self.request.user)

            # Return to feed with the new post
            if response['success']:
                return HttpResponseRedirect('/')

        # If form not valid return to the page with the errors
        return render(self.request, template_name='blog/new_post.html', context={'form': form})


class PublishDraftPost(View):
    def post(self, *args, **kwargs):
        post_id = self.request.POST.get('post_id')

        # Call function to update status to 'published'
        service.blog.Blog().publish_draft(post_id=post_id)

        return HttpResponseRedirect('/')


class DeletePost(View):
    def post(self, *args, **kwargs):
        post_id = self.request.POST.get('post_id')

        # Delete the selected post
        service.blog.Blog().delete_post(post_id=post_id)

        return HttpResponseRedirect('/')


class Comment(View):
    def get(self, *args, **kwargs):
        # In this project I return all comments in the post object, but this is not a good approach
        #    In real scenarios I'd use something like this and fetch the comments on demand via Ajax ou something similar
        #    This function is just one use example
        post_id = self.request.POST.get('post_id')
        response = service.blog.Blog().get_comments(post_id=post_id)

        return JsonResponse(response, safe=False)

    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        # Get and validate the comment form
        form = CommentForm(self.request.POST)
        if form.is_valid():
            service.blog.Blog().create_comment(post_id=self.request.POST.get('post_id'),
                                               content=form.cleaned_data['content'],
                                               user=self.request.user)

        # Return to feed
        return HttpResponseRedirect('/')

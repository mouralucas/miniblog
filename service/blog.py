from blog.forms import CommentForm
from blog.models import Post, Comment


class Blog:
    def __init__(self, post_id=None, comment_id=None, author_id=None):
        self.post_id = post_id
        self.comment_id = comment_id
        self.author_id = author_id

    def get_posts(self, user_id):
        # Get all published posts, from every user
        posts = Post.objects.filter(status='published').all()
        # If user is logged, get its drafts
        if user_id is not None:
            # Get drafts for the user
            drafts = Post.objects.filter(status='draft', user=user_id).all()

            # Union to return published and draft in same list
            posts = posts.union(drafts)

        response = {
            'success': True,
            'posts': posts.order_by('-created_at'),
            'comment_form': CommentForm(),
        }

        return response

    def get_user_posts(self, user_id):
        posts = Post.objects.filter(user_id=user_id).order_by('-created_at')

        response = {
            'success': True,
            'posts': posts,
        }

        return response

    def create_post(self, form, user):
        new_post = Post(title=form.cleaned_data.get('title'), content=form.cleaned_data.get('content'), status=form.cleaned_data.get('status'))
        new_post.user_id = user.id
        new_post.save()

        response = {
            'success': True
        }
        return response

    def publish_draft(self, post_id):
        # Just update the status
        Post.objects.filter(id=post_id).update(status='published')

        response = {'success': True}

        return response

    def delete_post(self, post_id):
        Post.objects.get(id=post_id).delete()

        return {'success': True}

    def create_comment(self, content, post_id, user):
        comment = Comment(content=content, user_id=user.id, post_id=post_id)
        comment.save()

        return {'success': True}

    def get_comments(self, post_id):
        comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')

        response = {
            'success': True,
            'comments': comments
        }

        return response

    def delete_comment(self):
        pass

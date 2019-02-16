from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from django.utils import timezone
from forms import CommentForm


@login_required
def Feed(request):
    """
    Function to fetch posts made by people the requesting user is following
    :param request:
    :return:
    """

    user_profile = request.user.profile  # gets and saves the profile of the logged in user

    # all_posts_by_following = []  #creating a list to hold posts made by users the logged inuser is following
    # user_is_following = user_profile.follows.all() #gets and saves the profiles of the users the logged in user is following
    # for following in user_is_following: #looping over each follower and saving it in a variable called following
    #     for post_by_following in following.user.post_set.all().order_by('-date_posted'):
    #         all_posts_by_following.append(post_by_following)  #appending each post to the list all_posts_by_following to be looped over in the template

    all_posts = Post.objects.all().order_by('-date_posted')
    following = user_profile.follows.all()
    all_posts_by_following = []
    for post in all_posts:
        if post.author.profile in following or post.author.profile == user_profile:
            all_posts_by_following.append(post)
    no_of_posts = len(all_posts_by_following)

    context = {
        'posts': all_posts_by_following,
        'no_of_posts': no_of_posts
    }

    return render(request, 'Post/feed.html', context)


# class Feed(LoginRequiredMixin, ListView):
#     model = Post
#     template_name = 'Post/feed.html'
#     context_object_name = 'posts'
#     ordering = ['-date_posted']


class PostDetail(DetailView):
    model = Post
    template_name = 'Post/blog-detail.html'

    def __init__(self):
        super.__init__
        self.comment_form = CommentForm()

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comment_form'] = self.comment_form
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(PostDetail, self).get_context_data(**kwargs)
    #     context['comments'] = Post.comment_set.order_by('-date_commented')
    #     return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'Post/post-create.html'
    fields = ['title', 'image', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # url matching is in post/urls.py

    model = Post
    template_name = 'Post/post-create.html'
    fields = ['title', 'image', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # url matching is in post/urls.py

    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def PostLikeToggle(request):
    if request.method == 'GET':
        slug = request.GET.get("slug", None)
        user = request.GET.get("user", None)

        post_to_like = Post.objects.get(slug=slug)
        user_liking = User.objects.get(username=user)

        if user_liking in post_to_like.likes.all():
            # remove user from liking the post if already like by user
            post_to_like.likes.remove(user_liking)
        else:
            # adding user o liked people for the post
            post_to_like.likes.add(user_liking)

        no_of_likes = post_to_like.likes.count()

        data = {
            'likes': no_of_likes,
        }

        return JsonResponse(data)


@login_required
def PostComment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.comment_by = request.user
            new_comment.post = post
            new_comment.save()

    return redirect('/feed/article/' + post.slug + '#commentBox')






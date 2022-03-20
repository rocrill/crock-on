from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from .models import Post
from .forms import CommentForm, PostForm
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages


def search_recipes(request):
    if request.method == "POST":
        searched = request.POST['searched']
        recipes = Post.objects.filter(
            Q(content__icontains=searched) | Q(title__icontains=searched) | Q(author__username__icontains=searched)).filter(status=1)

        return render(request, 'search_recipes.html',
                      {'searched': searched,
                       'recipes': recipes})
    else:
        return render(request, 'search_recipes.html', {})


def add_recipe(request):
    form = None
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        form.instance.author = request.user
        if form.is_valid():

            form.save()
            messages.success(request, "Thanks for submitting your recipe! This will be published as soon as we review it :)" )
            return redirect ("home") 
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6

class RandomPostList(generic.ListView):
    model = Post
    queryset = Post.objects.all().filter(status=1).order_by('?')
    template_name = "random_recipe.html"

class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "update_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 0
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Thanks for your update! Your post will be re-published as soon as we review the changes :)" )
        return reverse('home')


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = "delete_post.html"

    def get(self, request, slug, *args, **kwargs):
        post = Post.objects.filter(slug=slug)
        msg=f"You have deleted your '{ post[0].title }' recipe!"
        post.delete()
        messages.success(self.request, msg)
        return HttpResponseRedirect(reverse('home'))

class about(View):
    template_name = "about.html"

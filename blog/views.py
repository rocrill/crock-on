"""File to create view functions and classes to
take web requests and return a web response."""


from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from .models import Post
from .forms import CommentForm, PostForm
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages


def search_recipes(request):
    """View for searching recipe posts for specific keywords."""
    if request.method == "POST":
        searched = request.POST['searched']
        if not searched:
            return redirect("/")
        post_list = Post.objects.filter(
            Q(content__icontains=searched) |
            Q(title__icontains=searched) |
            Q(author__username__icontains=searched)).filter(status=1)

        return render(request, 'index.html',
                      {'searched': searched,
                       'post_list': post_list})
    else:
        return render(request, 'index.html', {})


def add_recipe(request):
    """View for creating recipe posts."""

    if not request.user.is_authenticated:
        messages.error(request, "You must login before you can share a recipe!")
        return redirect("/accounts/login/")

    form = None
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        form.instance.author = request.user
        if form.is_valid():

            form.save()
            messages.success(request,
                             "Thanks for submitting your recipe!" +
                             " This will be published as soon as" +
                             " we review it :)")
            return redirect("home")
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


class PostList(generic.ListView):
    """View for displaying recipe post list."""
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class RandomPostList(generic.ListView):
    """View for displaying a random recipe post."""
    model = Post
    queryset = Post.objects.all().filter(status=1).order_by('?')
    template_name = "random_recipe.html"


class PostDetail(View):
    """View for displaying recipe post detail page."""
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
    """View to display number of likes on recipe posts."""
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class PostUpdateView(generic.UpdateView):
    """View for updating recipe posts."""
    model = Post
    form_class = PostForm
    template_name = "update_post.html"

    def get(self, request, slug, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must login before you can edit your recipes!")
            return redirect("/accounts/login/")
        post = Post.objects.get(slug=slug)
        if request.user != post.author:
            messages.error(request, "You are not authorised to edit this post as you are not the author!")
            return redirect("/")
        return super().get(request, slug, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 0
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request,
                         "Thanks for your update!" +
                         " Your post will be re-published" +
                         " as soon as we review the changes :)")
        return reverse('home')


class PostDeleteView(generic.DeleteView):
    """View for deleting recipe posts."""
    model = Post
    template_name = "delete_post.html"

    def get(self, request, slug, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must login before you can delete your recipes!")
            return redirect("/accounts/login/")
        post = Post.objects.get(slug=slug)
        if request.user != post.author:
            messages.error(request, "You are not authorised to delete this post as you are not the author!")
            return redirect("/")
        msg = f"You have deleted your '{ post.title }' recipe!"
        post.delete()
        messages.success(self.request, msg)
        return HttpResponseRedirect(reverse('home'))


class about(View):
    """View for displaying the 'About' page."""
    template_name = "about.html"

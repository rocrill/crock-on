from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from .models import Post
from .forms import CommentForm, PostForm
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.db.models import Q



def search_recipes(request):
    if request.method == "POST":
        searched = request.POST['searched']
       # recipes = Post.objects.filter(title__icontains=searched)
        recipes = Post.objects.filter(
            Q(content__icontains=searched) | Q(title__icontains=searched))

        return render(request, 'search_recipes.html', 
        {'searched' :searched,
        'recipes' :recipes})
    else:
        return render(request, 'search_recipes.html', {})

def add_recipe(request):
    form = None
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        form.instance.author = request.user
        if form.is_valid():
            # print(f'len of files={len(request.FILES)}')
            # file = request.FILES['featured_image']

            # upload_data = cloudinary.uploader.upload(file)
            # print(f'upload_data={upload_data}')

            form.save()
            return HttpResponseRedirect('/success/')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6

# class RandomPostList(generic.ListView):
#     model = Post
#     #queryset = Post.objects.filter(status=1).order_by("-created_on")
#     queryset = Post.objects.all().order_by('?')
#     template_name = "index.html"
#     paginate_by = 6
    

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

    def post (self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data = request.POST) 

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
        post=get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args =[slug]))


# class PostCreateView(generic.CreateView):
#     model = Post
#     fields = ['title', 'slug', 'content', 'header_image', 'featured_image']
#     template_name = "post_form.html"

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         #your_object.user = request.user
#         return super().form_valid(form) 

#         return render(request, 'upload.html', {'form': form})

      



class PostUpdateView(generic.UpdateView):
    model = Post
    template_name = "update_post.html"
    fields = ['title', 'slug', 'content', 'featured_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

        return render(request, 'upload.html', {'form': form})

    def get_success_url(self):
        return reverse('update_success')


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = "delete_post.html"
    fields = ['title', 'slug', 'content', 'featured_image']
    #success_url = reverse_lazy('home')
    
    def get_success_url(self):
        return reverse('delete_success')
  
class about(View):
    template_name = "about.html"
    

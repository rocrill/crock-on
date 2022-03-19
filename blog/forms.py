from .models import Post, Comment
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


#Writing form class as per django vid to enable image upload

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'featured_image', 'content')
        widgets = {
            #'content': SummernoteInplaceWidget(),
            #'content': forms.Textarea(attrs={'class': 'form-control'}),
            'content': SummernoteWidget(),
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',) 

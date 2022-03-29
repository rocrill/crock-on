"""File to include any forms used across the site."""

from .models import Post, Comment
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class PostForm(forms.ModelForm):
    """Form for recipe sharing post."""
    class Meta:
        model = Post
        fields = ('title', 'slug', 'featured_image', 'content')
        widgets = {
            'content': SummernoteWidget(),
        }


class CommentForm(forms.ModelForm):
    """Form for comments made on recipe posts."""
    class Meta:
        model = Comment
        fields = ('body',)


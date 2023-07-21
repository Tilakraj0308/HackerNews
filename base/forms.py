from django.forms import ModelForm
from .models import Post
from django import forms


class postForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'url', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom-input', 'size': '30'}),
            'body': forms.Textarea(attrs={'class': 'custom-textarea', 'rows': '5', 'cols': '30'}),
        }
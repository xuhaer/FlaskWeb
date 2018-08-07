from django import forms

from .models import Comment


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['name', 'email', 'url', 'text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '昵称',
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'email',
            }),
            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'http:(可选)',
                'required':False
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
        }

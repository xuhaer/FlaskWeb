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
                'placeholder': '请输入昵称',
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@gmail.com',
            }),
            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '我有话说',
                'rows': 4,
            }),
        }

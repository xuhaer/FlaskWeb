from django import forms

from captcha.fields import CaptchaField

from .models import Comment



class CommentForm(forms.ModelForm):
    captcha = CaptchaField()
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(必填)',
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(可选)',
                'required':False,
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
        }

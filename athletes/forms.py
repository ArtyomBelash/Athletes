from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddAthleteForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана',
                                      label='Категория')
    image = forms.ImageField(label='Фото')

    class Meta:
        model = Athlete
        fields = ['title', 'content', 'image', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5,
                                             'style': 'resize:none'}),
        }
        labels = {
            'content': 'Статья',
        }

        def clean_title(self):
            title = self.cleaned_data['title']
            if len(title) > 50:
                raise ValidationError('Заголовок слишком длинный')
            return title


class ShareAthleteEmailForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=25, label='Имя')
    sender = forms.EmailField(label='Ваш email')
    to = forms.EmailField(label='Кому')
    comment = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'cols': 25, 'rows': 5,
                                                                                           'style': 'resize:none'}),
                              label='Коментарий')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'cols': 80, 'rows': 8,
                                          'style': 'resize:none'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['body'].required = True

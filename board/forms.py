from django import forms
from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'heading',
            'text',
            'category',
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',

        ]


class AcceptCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AcceptCommentForm, self).__init__(*args, **kwargs)
        self.fields['status'].label = 'Статус'

    class Meta:
        model = Comment
        fields = [
            'status',
        ]

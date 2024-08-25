from django_filters import FilterSet
from .models import (
    Comment,
    Post,
)


class PostFilter(FilterSet):
    class Meta:
        model = Comment
        fields = [
            'post',
        ]

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(author=kwargs['request'])
        self.filters['post'].label = 'Объявление'

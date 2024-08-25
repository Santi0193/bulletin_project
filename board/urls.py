from django.urls import path

from .views import (
    PostsList,
    PostDetail,
    PostEdit,
    PostDelete,
    ReviewsList,
    ReviewDelete,
    AcceptReview,
    create_post,
    create_comment_to_post,
)

urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('create/', create_post, name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/comment_create', create_comment_to_post, name='comment_create'),
    path('reviews/', ReviewsList.as_view(), name='reviews_list'),
    path('reviews/<int:pk>/delete', ReviewDelete.as_view(), name='review_delete'),
    path('reviews/<int:pk>/accept', AcceptReview.as_view(), name='review_accept'),
]

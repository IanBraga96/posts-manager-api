from django.urls import path
from .views import (
    PostListCreateAPIView,
    PostDetailAPIView,
    PostLikeAPIView,
    PostCommentAPIView,
    RegisterAPIView,
    LoginAPIView,
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("", PostListCreateAPIView.as_view(), name="post-list-create"),
    path("<int:pk>/", PostDetailAPIView.as_view(), name="post-detail"),
    path("<int:pk>/like/", PostLikeAPIView.as_view(), name="post-like"),
    path("<int:pk>/comments/", PostCommentAPIView.as_view(), name="post-comments"),
]

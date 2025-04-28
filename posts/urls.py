from django.urls import path
from .views import PostListCreateAPIView, PostDetailAPIView, PostLikeAPIView

urlpatterns = [
    path("", PostListCreateAPIView.as_view(), name="post-list-create"),
    path("<int:pk>/", PostDetailAPIView.as_view(), name="post-detail"),
    path('<int:pk>/like/', PostLikeAPIView.as_view(), name='post-like'),
]

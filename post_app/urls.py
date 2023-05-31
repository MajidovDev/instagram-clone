from django.urls import path
from post_app.views import PostListApiView, PostCreateApiView

urlpatterns = [
    path('posts/', PostListApiView.as_view()),
    path('create/', PostCreateApiView.as_view()),
]
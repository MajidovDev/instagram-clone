from django.urls import path
from post_app.views import PostListApiView

urlpatterns = [
    path('posts/', PostListApiView.as_view()),
]
from django.urls import path
from post_app.views import PostListApiView, PostCreateApiView, PostRetrieveUpdateDestroyApiView,\
    PostCommentListView, PostCommentCreateView

urlpatterns = [
    path('posts/', PostListApiView.as_view()),
    path('create/', PostCreateApiView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyApiView.as_view()),
    path('<uuid:pk>/comments/list/', PostCommentListView.as_view()),
    path('<uuid:pk>/comments/create/', PostCommentCreateView.as_view()),
]
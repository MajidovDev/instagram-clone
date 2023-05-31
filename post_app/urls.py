from django.urls import path
from post_app.views import PostListApiView, PostCreateApiView, PostRetrieveUpdateDestroyApiView,\
    PostCommentListView, PostCommentCreateView, CommentsRetrieveView, PostLikesListView, CommentsListView, PostCommentLikesListView, \
    PostLikeView, PostCommentLikeView

urlpatterns = [
    path('list/', PostListApiView.as_view()),
    path('create/', PostCreateApiView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyApiView.as_view()),
    path('<uuid:pk>/comments/list/', PostCommentListView.as_view()),
    path('<uuid:pk>/comments/create/', PostCommentCreateView.as_view()),
    path('<uuid:pk>/likes/list/', PostLikesListView.as_view()),

    path('comments/list/', CommentsListView.as_view()),
    path('comments/<uuid:pk>/', CommentsRetrieveView.as_view()),
    path('comments/<uuid:pk>/likes/list/', PostCommentLikesListView.as_view()),
    path('comments/<uuid:pk>/likes/create-delete/', PostCommentLikeView.as_view()),

    path('<uuid:pk>/likes/create-delete/', PostLikeView.as_view()),
]
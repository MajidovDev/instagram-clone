from post_app.models import PostModel, PostLikeModel, PostCommentModel, CommentLikeModel
from post_app.serializers import PostSerializers, PostLikeSerializer, CommentSerializer, CommentLikeSerializer
from rest_framework.viewsets import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from shared_app.custom_pagination import CustomPagination


class PostListApiView(generics.ListAPIView):
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return PostModel.objects.all()


class PostCreateApiView(generics.CreateAPIView):
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


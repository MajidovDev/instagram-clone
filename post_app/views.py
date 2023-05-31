from rest_framework import status

from post_app.models import PostModel, PostLikeModel, PostCommentModel, CommentLikeModel
from post_app.serializers import PostSerializers, PostLikeSerializer, CommentSerializer, CommentLikeSerializer
from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
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


class PostRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "Post successfully UPDATED",
            "data": serializer.data
        })

    def delete(self, request, *args, **kwargs):
        return Response({
            "success": True,
            "status": status.HTTP_204_NO_CONTENT,
            "message": "Post successfully DELETED",
        })


class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostCommentModel.objects.filter(post__id=post_id)
        return queryset


class PostCommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)

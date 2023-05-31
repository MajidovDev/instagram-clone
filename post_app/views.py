from rest_framework import status
from rest_framework.views import APIView

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
    pagination_class = CustomPagination

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


class CommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]
    queryset = PostCommentModel.objects.all()


class CommentsRetrieveView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]
    queryset = PostCommentModel.objects.all()


class PostLikesListView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostLikeModel.objects.filter(post__id=post_id)
        return queryset


class PostLikeView(APIView):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        try:
            post_like = PostLikeModel.objects.create(
                author=self.request.user,
                post_id=pk
            )
            serializer = PostLikeSerializer(post_like)
            data = {
                "success": True,
                "message": "Post Successfully liked",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "success": False,
                "message": f"{str(e)}",
                "data": None
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            post_like = PostLikeModel.objects.get(
                author=self.request.user,
                post_id=pk
            )
            post_like.delete()
            data = {
                "success": True,
                "message": "Like successfully deleted"
            }
            return Response(data, status.HTTP_204_NO_CONTENT)
        except Exception as e:
            data = {
                "success": False,
                "message": f"{str(e)}"
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)


class PostCommentLikesListView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        queryset = CommentLikeModel.objects.filter(comment__id=comment_id)
        return queryset


class PostCommentLikeView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        try:
            comment_like = CommentLikeModel.objects.create(
                author=self.request.user,
                comment_id=pk
            )
            serializer = CommentLikeSerializer(comment_like)
            data = {
                "success": True,
                "message": "Comment successfully liked",
                "data": serializer.data
            }
            return Response(data, status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "success": False,
                "message": f"{e}",
                "data": None
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            comment_like = CommentLikeModel.objects.get(
                author=self.request.user,
                comment_id=pk
            )
            comment_like.delete()
            data={
                "success": True,
                "message": "Comment Like successfully DELETED"
            }
            return Response(data, status.HTTP_204_NO_CONTENT)
        except Exception as e:
            data = {
                "success": True,
                "message": f"{e}"
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)
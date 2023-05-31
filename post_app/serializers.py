from rest_framework import serializers

from post_app.models import PostModel, UserModel, PostLikeModel, PostCommentModel, CommentLikeModel


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'photo')


class PostSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    post_likes_count = serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count = serializers.SerializerMethodField('get_post_comments_count')
    me_liked = serializers.SerializerMethodField('get_me_liked')

    class Meta:
        model = PostModel
        fields = [
            "id",
            "author",
            "image",
            "caption",
            "post_likes_count",
            "post_comments_count",
            "created_time",
            "me_liked"
        ]

    @staticmethod
    def get_post_likes_count(obj):
        return obj.likes.count()

    @staticmethod
    def get_post_comments_count(obj):
        return obj.comments.count()

    def get_me_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                like = PostLikeModel.objects.get(post=obj, author=request.user)
                return True
            except PostLikeModel.DoesNotExist:
                return False
        return True


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField('get_replies')
    likes_count = serializers.SerializerMethodField('get_likes_count')
    me_liked = serializers.SerializerMethodField('get_me_liked')

    class Meta:
        model = PostCommentModel
        fields = ("id", "author", "comment", "parent", "created_time", "replies")

    def get_replies(self, obj):
        if obj.child.exists():
            serializers = self.__class__(obj.child.all(), many=True, context=self.context)
            return serializers.data
        else:
            return None

    def get_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(author=user).exists()
        else:
            return False

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()


class CommentLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = CommentLikeModel
        fields = ("id", "author", "comment")


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = PostLikeModel
        fields = ("id", "author", "post")
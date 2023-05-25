from rest_framework import serializers

from post_app.models import PostModel, UserModel, PostLikeModel


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
        fields = ("id", "author", "image", "caption", "created_time", "get_post_likes_count", "get_post_comments_count", "me_liked")

    def get_post_likes_count(self, obj):
        return obj.likes.count()

    def get_post_comments_count(self, obj):
        return obj.comments.count()

    def get_me_liked(self, obj):
        request = self.context.get('request', None)
        if request and  request.user.is_authenticated:
            try:
                like = PostLikeModel.objects.get(post=obj, author=request.user)
                return True
            except PostLikeModel.DoesNotExist:
                return False
        return False

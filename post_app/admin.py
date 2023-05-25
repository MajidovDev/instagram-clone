from django.contrib import admin
from post_app.models import PostModel, PostLikeModel, PostCommentModel, CommentLikeModel


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'caption', 'created_time')
    search_fields = ('id', 'author__username', 'caption')


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created_time')
    search_fields = ('id', 'author__username', 'comment')


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created_time')
    search_fields = ('id', 'author__username')


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created_time')
    search_fields = ('id', 'author__username')


admin.site.register(PostModel, PostAdmin)
admin.site.register(PostCommentModel, PostCommentAdmin)
admin.site.register(PostLikeModel, PostLikeAdmin)
admin.site.register(CommentLikeModel, CommentLikeAdmin)

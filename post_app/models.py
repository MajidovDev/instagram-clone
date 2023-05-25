from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from shared_app.models import BaseModel
from django.core.validators import FileExtensionValidator, MaxLengthValidator

UserModel = get_user_model()


class PostModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images', validators=[
        FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])
    ])
    caption = models.TextField(validators=[MaxLengthValidator(2000)])

    class Meta:
        db_table = "post"
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return f"{self.author} post about {self.caption}"


class PostCommentModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.author} commented"


class PostLikeModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'post'],
                name="post-like"
            )
        ]

    def __str__(self):
        return f"{self.author} liked"


class CommentLikeModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostCommentModel, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'comment'],
                name="comment-like"
            )
        ]

    def __str__(self):
        return f"{self.author} liked the comment {self.comment}"
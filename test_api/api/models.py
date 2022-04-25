from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название статьи'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор статьи'
    )
    text = models.TextField()

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"    

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Родительский комментарий'
    )
    level = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Уровень вложенности'
    )
    text = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:30]

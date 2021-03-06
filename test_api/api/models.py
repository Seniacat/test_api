from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    """Модель статьи блога"""
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
    """Модель комментария к статье
    или другому комментарию"""
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
    main_parent = models.ForeignKey(
        'self',
        verbose_name='Корневой комментарий 3го уровня вложенности',
        blank=True,
        null=True,
        related_name='comment_children',
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительский комментарий',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
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
        return self.text[:20]

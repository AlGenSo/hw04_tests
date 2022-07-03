from django.db import models
from django.contrib.auth import get_user_model
from pytils.translit import slugify

from .constants import STRING_LENGHT_LIMIT

User = get_user_model()


class Post(models.Model):
    '''Объявляем класс Post, наследник класса Model из пакета models
    Описываем поля модели и их типы'''

    text = models.TextField(
        verbose_name='Текст публикации',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        'Group',
        verbose_name='Сообщество',
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
    )

    class Meta:

        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:STRING_LENGHT_LIMIT]


class Group(models.Model):
    '''Объявляем класс Group, наследник класса Model из пакета models
    Описываем поля модели и их типы'''

    title = models.CharField(
        verbose_name='Сообщество',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='URL - адрес',
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
    )

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)

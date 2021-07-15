from django.db import models
from django.urls import reverse_lazy
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey


class Women(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Url')
    content = models.TextField(blank=True, verbose_name='Текст')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes', verbose_name='Лайки')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('post', kwargs={'post_slug': self.slug})

    def get_comments(self):
        return self.comments.all()

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Url')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Comment(MPTTModel):
    post = models.ForeignKey(Women, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, db_index=True, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['time_create']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.author} - {self.post}"

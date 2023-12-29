from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
from athletes_config import settings


class Athlete(models.Model):
    title = models.CharField('Заголовок', max_length=140)
    content = models.TextField('Контент')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    time_create = models.DateTimeField('Создан', auto_now_add=True)
    time_update = models.DateTimeField('Обновлен', auto_now=True)
    image = models.ImageField('Картинка', upload_to='athletes_image', blank=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория',
                                 related_name='athletes')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='URL')
    is_published = models.BooleanField('Опубликован', default=False)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='athlete_liked',
                                        blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'athlete_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            title = translit(f'{self.title}', 'ru', reversed=True)
            self.slug = slugify(title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Спортсмен'
        verbose_name_plural = 'Спортсмены'
        ordering = ('-time_update',)
        indexes = [
            models.Index(fields=['time_update'])
        ]


class Category(models.Model):
    name = models.CharField('Категория', max_length=140)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Comment(models.Model):
    name = models.CharField(max_length=25, verbose_name="Имя")
    body = models.TextField(verbose_name="Коментарий")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='athletes')
    active = models.BooleanField(default=True, verbose_name='Активный коментарий')

    def __str__(self):
        return f'Автор: {self.name} - {self.athlete}'

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        indexes = [
            models.Index(fields=['created_on'])
        ]

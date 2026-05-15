from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field

from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.

class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Nigger.Status.PUBLISHED)

class Nigger(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255,verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, unique=True,validators=[
        MinLengthValidator(5),
        MaxLengthValidator(100),
    ])
    content = CKEditor5Field('Текст статьи', config_name='default') 
    time_create = models.DateTimeField(auto_now_add=True,verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True,verbose_name="Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT, verbose_name="Статус")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts',verbose_name="Категории")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags',verbose_name="Тэги")
    #gun = models.OneToOneField('Gun', on_delete=models.SET_NULL, null=True, blank=True, related_name='nigga',verbose_name="Оружие")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)
    
    objects = models.Manager()
    published = PublishedModel()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Известные негры'
        verbose_name_plural = 'Известные негры'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def __str__(self):  # noqa: F811
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    def get_edit_page(self):
        return reverse('edit_page', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})

class Gun(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name
    
class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
    

class Comments(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='comments', null=True, default=None)
    comment = models.TextField(verbose_name="Комментарий")
    post = models.ForeignKey('Nigger', on_delete=models.CASCADE, related_name='post_comments')
    # time_create = models.DateTimeField(auto_now_add=True,verbose_name="Время создания",blank=True)
    
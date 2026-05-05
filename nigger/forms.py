from django import forms
from .models import Category, Comments, Gun, Nigger
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана' , label="Категории")
    gun = forms.ModelChoiceField(queryset=Gun.objects.all(),empty_label='Нет ствола(', required=False, label="Оружие")

    class Meta:
        model = Nigger
        fields = ['title', 'content', 'photo', 'is_published', 'cat', 'gun', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")
    
    
class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Текст обращения')
    captcha = CaptchaField(label='Капча')
    

class AddComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        
        
# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255,min_length=5,error_messages={
#                                 'min_length': 'Слишком короткий заголовок',
#                                 'required': 'Без заголовка - никак',
#                             }, label="Заголовок")
#     # #slug = forms.SlugField(max_length=255, label="URL", validators=[
#     #     MinLengthValidator(5),
#     #     MaxLengthValidator(100),
#     # ])
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols':50, 'rows':5}), required=False, label="Контент")
#     is_published = forms.BooleanField(required=False,initial=True , label="Статус")
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана' , label="Категории")
#     gun = forms.ModelChoiceField(queryset=Gun.objects.all(),empty_label='Нет ствола(', required=False, label="Оружие")

#     def clean_title(self):
#         title = self.cleaned_data['title']
#         ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#         if not (set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError("Должны присутствовать только русские символы, дефис и пробел.")


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
        fields = ['title', 'content', 'photo', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'tags': forms.CheckboxSelectMultiple(),
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
        
class UpdatePost(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана' , label="Категории")
    
    class Meta:
        model = Nigger
        fields = ['title', 'content', 'photo', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'tags': forms.CheckboxSelectMultiple(),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title       
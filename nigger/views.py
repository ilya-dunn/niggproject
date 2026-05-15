# import os
# import uuid
from django.contrib.auth.decorators import login_required, permission_required  # noqa: F401
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect  # noqa: F401
from django.shortcuts import render, redirect, get_object_or_404  # noqa: F401
from django.urls import reverse, reverse_lazy  # noqa: F401
# from django.views import View 
# from django.urls import reverse
# from django.template.loader import render_to_string
# from django.template.defaultfilters import slugify

from nigger.models import Category, Comments, Nigger, TagPost, UploadFiles  # noqa: F401
from nigger.forms import AddComment, AddPostForm, ContactForm, UploadFileForm  # noqa: F401
# from sitenigger import settings
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView  # noqa: F401

from nigger.utils import DataMixin  # noqa: F401

# Create your views here.

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class NiggerHome(DataMixin, ListView):
    template_name='nigger/index.html'
    context_object_name='posts'
    title_page='Главная страница'
    cat_selected=0
    
    def get_queryset(self):
        return Nigger.published.filter(is_published=1).select_related('cat')
    
def test(request):
    return HttpResponse("OK")
    
@login_required
def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'nigger/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})


class ShowPost(DataMixin, DetailView):
    model = Nigger
    template_name = 'nigger/post.html'
    slug_url_kwarg='post_slug'
    context_object_name='post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddComment()
        return self.get_mixin_context(context, title=context['post'].title)
    
    def get_queryset(self):
        return Nigger.published.filter(is_published=1)
    
    def post(self, request, *args, **kwargs):
        form = AddComment(request.POST)
        if form.is_valid():
            w = form.save(commit=False)
            w.author = request.user
            w.post = self.get_object()  # Получаем текущий пост
            w.save()
            return redirect(request.path)  # Перезагружаем страницу, чтобы увидеть коммент
        return self.get(request, *args, **kwargs)
    

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'nigger/addpage.html'
    title_page = 'Добавление статьи'
    
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

    
class UpdatePage(LoginRequiredMixin, DataMixin, UpdateView):
    model = Nigger
    form_class = AddPostForm
    template_name = 'nigger/addpage.html'
    title_page = 'Редактирование статьи' 
    
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)
    

class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'nigger/contact.html'
    success_url = reverse_lazy('home')
    title_page = "Обратная связь"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


def login(request):
    return HttpResponse("Авторизация")


class NiggerCategory(DataMixin, ListView):
    template_name='nigger/index.html'
    context_object_name='posts'
    allow_empty=False
    
    def get_queryset(self):
        return Nigger.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected = cat.pk) 

    
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(DataMixin, ListView):
    template_name='nigger/index.html'
    context_object_name='posts'
    allow_empty=False
    
    def get_queryset(self):
        return Nigger.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тэг - ' + tag.tag)  


class ShowComments(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddComment
    template_name = 'nigger/post.html'
    
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        w.post = get_object_or_404(Nigger, slug=self.kwargs['post_slug']) 
        w.save()
        return super().form_valid(form) 
    

class DeleteComment(LoginRequiredMixin, DataMixin, DeleteView):
    model = Comments
    #permission_required = 'nigger.change_nigger'  # noqa: F811
    
    def get_success_url(self):
        return reverse('post', kwargs={'post_slug': self.object.post.slug})
    
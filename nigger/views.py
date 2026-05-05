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
            #handle_uploaded_file(form.cleaned_data['file'])
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
    
    # def get_object(self, queryset=None):
    #     return get_object_or_404(Nigger.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'nigger/addpage.html'
    title_page = 'Добавление статьи'
    # login_url = '/admin/'
    permission_required = 'nigger.add_nigger'  # noqa: F811
    
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

    
class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Nigger
    fields = ['title', 'content', 'photo', 'is_published', 'cat', 'tags']
    template_name = 'nigger/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи' 
    permission_required = 'nigger.change_nigger'  # noqa: F811
    

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


class ShowComments(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddComment
    template_name = 'nigger/post.html'
    
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        w.post = get_object_or_404(Nigger, slug=self.kwargs['post_slug']) 
        w.save()
        return super().form_valid(form) 
    

class DeleteComment(PermissionRequiredMixin, DataMixin, DeleteView):
    model = Comments
    permission_required = 'nigger.change_nigger'  # noqa: F811
    
    def get_success_url(self):
        return reverse('post', kwargs={'post_slug': self.object.post.slug})
    
    def get_queryset(self):
        return Nigger.published.filter()


# def index(request):
#     posts = Nigger.published.filter(is_published=1).select_related('cat')
#     # t = render_to_string('nigger/index.html')
#     # return HttpResponse(t)
#     data = {'title': 'Главная страница',
#             'menu': menu,
#             # 'float': 28.56,
#             # 'lst': [1, 2, 'abc', True],
#             # 'set': {1, 1, 2, 3, 2, 5},
#             # 'dict': {'key_1': 'value_1', 'key_2': 'value_2'},
#             # 'obj': MyClass(10, 20),
#             # 'url': slugify("The main page"),
#             'posts': posts,
#             'cat_selected':0
#             }
#     return render(request, 'nigger/index.html', context=data)


# @permission_required(perm='nigger.add_nigger', raise_exception=True)
# def contact(request):
#     return HttpResponse("Обратная связь")


# def handle_uploaded_file(f):
#     upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
#     os.makedirs(upload_dir, exist_ok=True)
#     new_id = uuid.uuid4()
#     file_path = os.path.join(upload_dir, f'{new_id}_{f.name}')
#     with open(file_path, "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


# def categories(request, cat_id):
#     return HttpResponse(f"<h1>Страница по категориям</h1><p>id: {cat_id}<p/>")


# def categories_by_slug(request, cat_slug):
#     if request.POST:
#         print(request.POST)
#     return HttpResponse(f"<h1>Страница по категориям</h1><p>slug: {cat_slug}<p/>")


# def archive(request, year):
#     if year > 2020:
#         # raise Http404()
#         # return redirect('/', permanent=True)
#         uri = reverse('cats', args=('music',))
#         # return redirect('cats', 'music') #имя маршрута, параметр (по желанию)
#         # return redirect(uri)
#         return HttpResponseRedirect('/')
#     return HttpResponse(f"<h1>Архив по годам</h1><p >{year}</p>")


# def show_post(request, post_slug):
#     post = get_object_or_404(Nigger, slug=post_slug)
#     data = {'title': post.title,
#             'menu': menu,
#             'post': post,
#             'cat_selected': 1,
#             }
#     return render(request, 'nigger/post.html', data)


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Nigger.objects.create(**form.cleaned_data)
#             #     return redirect('home')

#             # except:  # noqa: E722
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'nigger/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Nigger.Status.PUBLISHED).select_related('cat')
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#     return render(request, 'nigger/index.html', context=data)


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts=Nigger.published.filter(cat_id=category.pk).select_related('cat')
#     data = {'title': 'Рубрика: {category.name}',
#             'menu': menu,
#             'posts': posts,
#             'cat_selected':category.pk,
#             }
#     return render(request, 'nigger/index.html', context=data)


# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         return render(request, 'nigger/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})

#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         form = AddPostForm()
#         return render(request, 'nigger/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})

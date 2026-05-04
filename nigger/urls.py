from django.urls import path, register_converter, re_path  # noqa: F401
from nigger import views
from nigger import converters


register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.NiggerHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    # path('cats/<int:cat_id>/', views.categories, name='cats_id'),
    # path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
    # path('archive/<year4:year>/', views.archive, name='archive')
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.NiggerCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),
    path('comment/delete/<int:pk>/', views.DeleteComment.as_view(), name = 'delete_comment'),
]

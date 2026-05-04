from django.contrib import admin, messages
from .models import Category, Nigger
from django.utils.safestring import mark_safe
# Register your models here.


class GunFilter(admin.SimpleListFilter):
    title = 'Статус оружия'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('owned', 'Во владении'),
            ('single', 'Не во владении'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'owned':
            return queryset.filter(gun__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(gun__isnull=True)


@admin.register(Nigger)
class NiggerAdmin(admin.ModelAdmin):
    fields= ['title', 'content', 'slug', 'cat', 'gun', 'photo', 'post_photo']
    # exclude=[]
    # list_editable = []
    readonly_fields = ['slug', 'post_photo']
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('is_published',)
    #list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [GunFilter, 'cat__name', 'is_published']
    save_on_top=True


    # @admin.display(description="Краткое описание", ordering='content')
    # def brief_info(self, nigger: Nigger):
    #     return f"Описание {len(nigger.content)} символов."

    @admin.display(description="Photo", ordering='content')
    def post_photo(self, nigger: Nigger):
        if nigger.photo:
            return mark_safe(f'<img src= "{nigger.photo.url}" width=50>')  
        else:
            return 'no photo'
    


    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Nigger.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")


    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Nigger.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

# admin.site.register(Nigger, NiggerAdmin)
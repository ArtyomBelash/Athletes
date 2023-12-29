from django.contrib import admin
from .models import *


class AthleteAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'author', 'time_create', 'time_update', 'is_published', 'category')
    list_editable = ('is_published', 'category')
    list_display_links = ('title',)
    actions = ('set_published',)
    search_fields = ('title',)

    @admin.action(description='Опубликовать')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f'Измененно {count} записей')


class CatAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name')


admin.site.register(Athlete, AthleteAdmin)
admin.site.register(Category, CatAdmin)
admin.site.register(Comment)

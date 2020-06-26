from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Post)
# class Post(admin.ModelAdmin):
#     list_display = (
#         'email',
#         'created',
#         'author',
#         'category',
#         'tags',
#         'applicant',
#         'participants',
#     )
#     list_filter = (
#         'created',
#         'author',
#         'category',
#         'tags',
#     )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
admin.site.register(YoutubeUrl)
admin.site.register(SoundUrl)


@admin.register(RegForm)
class RegForm(admin.ModelAdmin):
    list_display = (
        'post',
        'check_agreement',
        'name',
        'email',
        'user_id',
        'user_mobile',
        'check_level',
        'check_thr',
        'check_status',
        'bank_account'
    )
    list_filter = (
        'post',
        'check_level',
        'check_thr',
        'check_status',
    )

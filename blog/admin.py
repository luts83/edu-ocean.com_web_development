from django.contrib import admin
from .models import *
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Post)
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
        'check_job',
        'bank_account',
        'created',
    )
    list_filter = (
        'post',
        'check_level',
        'check_thr',
        'check_status',
        'check_job',
        ('created', DateRangeFilter),
    )
    search_fields = ['name', 'user_id', 'user_mobile']


from django.contrib import admin
from .models import *
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

# admin.site.register(Card)
admin.site.register(CardSet)
# admin.site.register(TrySet)
admin.site.register(TryRecord)
admin.site.register(UploadFileModel)
admin.site.register(Notice)
# admin.site.register(Scomment)
# admin.site.register(CommentRoom)
admin.site.register(MissionImageModel)
admin.site.register(MissionSoundModel)
admin.site.register(UploadBase)

@admin.register(Card)
class Card(admin.ModelAdmin):
    list_display = (
        'card_set',
        'front',
        'back',
    )
    list_filter = (
        'card_set',
    )

@admin.register(TrySet)
class TrySet(admin.ModelAdmin):
    list_display = (
        'user',
        'cardset',
        'correct',
        'incorrect',
        'started_at',
        'last_updated_at',
        'is_finished',
    )
    list_filter = (
        'user',
        'cardset',
    )

@admin.register(Scomment)
class Scomment(admin.ModelAdmin):
    list_display = (
        'comment_room',
        'author',
        'created_at',
        'modified_at',
    )
    list_filter = (
        'comment_room',
        'author',
    )

@admin.register(CommentRoom)
class CommentRoom(admin.ModelAdmin):
    list_display = (
        'post',
        'participant',
    )
    list_filter = (
        'post',
        'participant',
    )




from django import forms
from .models import Comment
from .models import RegForm
from studyroom.models import Scomment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Scomment
        fields = ('text',)


class RegForm(forms.ModelForm):
    class Meta:
        model = RegForm
        fields = (
            'name',
            'email',
            'user_id',
            'check_level',
            'check_thr',
            'check_status',
            'bank_account'
        )
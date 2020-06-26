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
from django import forms
from .models import MissionImageModel, MissionSoundModel, Notice, UploadBase, Scomment


class UploadFileForm(forms.Form):
    file = forms.FileField()


class MissionSoundForm(forms.ModelForm):
    sfile = forms.FileField(
        label=' 소리 '
    )

    class Meta:
        model = MissionSoundModel
        fields = ['sfile']


class MissionImageForm(forms.ModelForm):
    ifile = forms.FileField(
        label=' 이미지 '
    )

    class Meta:
        model = MissionImageModel
        fields = ['ifile']


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']


class UploadBaseForm(forms.ModelForm):
    class Meta:
        model = UploadBase
        fields = ['title']
        # fields = ['sfile']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Scomment
        fields = ('text',)

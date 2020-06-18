from django import forms
from .models import MissionImageModel, MissionSoundModel, Notice, UploadBase, Scomment


class UploadFileForm(forms.Form):
    file = forms.FileField()

class MissionSoundForm(forms.ModelForm):
    class Meta:
        model = MissionSoundModel
        fields=['sfile']
        # fields = ['ifile']

class MissionImageForm(forms.ModelForm):
    class Meta:
        model = MissionImageModel
        fields=['ifile']
        # fields = ['sfile']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields=['title', 'content']
        # fields = ['sfile']

class UploadBaseForm(forms.ModelForm):
    class Meta:
        model = UploadBase
        fields=['title']
        # fields = ['sfile']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Scomment
        fields = ('text',)


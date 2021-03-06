import os
import csv
from django.shortcuts import get_list_or_404
from django.db import models
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdown


class CardSet(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="cardsets")
    name = models.CharField(max_length=512, default="default cardset name")
    limit = models.IntegerField(default=20)

    def __str__(self):
        return self.name


class Card(models.Model):
    card_set = models.ForeignKey(
        CardSet, on_delete=models.CASCADE, related_name="cards")
    front = models.CharField(max_length=512)
    back = models.CharField(max_length=512)

    def __str__(self):
        return "(" + self.front + ", " + self.back + ")"


class TrySet(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="trysets", null=True, blank=True)
    cardset = models.ForeignKey(
        CardSet, on_delete=models.SET_NULL, related_name="trysets", null=True, blank=True)
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)

    started_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        try:
            full_name = f"{self.user.username}::{self.cardset.name}"
        except:
            full_name = f"{self.user.username}::default cardset name"
        return full_name


class TryRecord(models.Model):
    tryset = models.ForeignKey(
        TrySet, on_delete=models.CASCADE, related_name="records", null=True, blank=True)
    card = models.ForeignKey(
        Card, on_delete=models.SET_NULL, related_name="records", null=True, blank=True)
    result = models.CharField(max_length=512)


class UploadFileModel(models.Model):
    file = models.FileField(null=True, upload_to='studyroom/%Y/%m/%d/')


class UploadBase(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="uploads")
    title = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)


class MissionImageModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="imgfiles", null=True, blank=True)
    ifile = models.FileField(null=True, upload_to='mission_images/%Y/%m/%d/')
    base = models.ForeignKey(UploadBase, on_delete=models.SET_NULL,
                             related_name="images", null=True, blank=True)


class MissionSoundModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             related_name="soundfiles", null=True, blank=True)
    sfile = models.FileField(null=True, upload_to='mission_sounds/%Y/%m/%d/')
    base = models.ForeignKey(UploadBase, on_delete=models.SET_NULL,
                             related_name="sounds", null=True, blank=True)


class Notice(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="notices", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="notices")

    def get_markdown_content(self):
        return markdown(self.content)

    def __str__(self):
        return self.title


class CommentRoom(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comment_rooms", null=True, blank=True)
    participant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='participate_comment_room', null=True, blank=True)


class Scomment(models.Model):
    comment_room = models.ForeignKey(
        CommentRoom, on_delete=models.CASCADE, related_name="scomments", null=True, blank=True)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_markdown_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return "/studyroom/study_room/" + str(self.comment_room.post.pk) + '#comment-id-{}'.format(self.pk)

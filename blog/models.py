from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)

    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/blog/category/{}/'.format(self.slug)

    class Meta:
        verbose_name_plural = 'categories'


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/blog/tag/{}/'.format(self.slug)


class Post(models.Model):
    content = MarkdownxField()
    title = models.CharField(max_length=100)
    head_image = models.ImageField(upload_to='head_images/%Y/%m/%d/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, default=1)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    applicant = models.ManyToManyField(
        User, related_name='applicate_posts', blank=True)
    participants = models.ManyToManyField(
        User, related_name='participate_posts', blank=True)

    is_activated = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created', ]

    def __str__(self):
        return '{} :: {}'.format(self.title, self.author)


    def get_absolute_url(self):
        return '/blog/{}/'.format(self.pk)

    def get_update_url(self):
        return self.get_absolute_url() + 'update/'

    def get_markdown_content(self):
        return markdown(self.content)

    def get_delete_url(self):
        return '/delete_post/{self.pk}/'


class YoutubeUrl(models.Model):
    video_url = models.URLField(default='')
    channel_url = models.URLField(default='')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="youtube_url", null=True, blank=True)


class SoundUrl(models.Model):
    title = models.CharField(
        max_length=255, default='default week', blank=True)
    sound_file = models.FileField(null=True, upload_to="%Y%m%d")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="sound_files", null=True, blank=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_markdown_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return self.post.get_absolute_url() + '#comment-id-{}'.format(self.pk)


class RegForm(models.Model):
    CHOICE_THR = (
        ("1", "블로그"),
        ("2", "유튜브"),
        ("3", "오픈채팅방"),
        ("4", "인터넷 검색"),
        ("5", "기타"),
    )

    CHOICE_JOB = (
        ("1", "중고등학생"),
        ("2", "대학/원생"),
        ("3", "직장인"),
        ("4", "취업준비중"),
        ("5", "기타"),
    )

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    check_agreement = models.BooleanField(
        default=False, help_text="이용약관, 개인정보 수집 및 이용 동의")
    name = models.CharField(
        max_length=10)
    email = models.EmailField(max_length=30)
    user_id = models.CharField(
        max_length=15)
    user_mobile = models.CharField(max_length=15)
    check_content = MarkdownxField()
    check_level = models.BooleanField(
        default=False, help_text="스터디 난이도를 확인하셨나요?")
    check_status = models.BooleanField(
        default=False, help_text="스터디에 참여해보신 적 있으신가요?")
    check_thr = models.CharField(
        max_length=1,
        choices=CHOICE_THR,
        blank=True,
        default='1',
        help_text="어떤 경로로 스터디를 알게되셨나요?"
    )
    check_job = models.CharField(
        max_length=1,
        choices=CHOICE_JOB,
        blank=True,
        default='1',
        help_text="현재 직업은 무엇인가요?"
    )
    bank_account = models.CharField(
        max_length=50, help_text="은행명과 계좌번호를 입력해 주세요 | 예시 : 3333-16-2308048 (카카오뱅크, 신은혜)")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

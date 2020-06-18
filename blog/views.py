from django.shortcuts import render, redirect
from .models import *
from .forms import CommentForm
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail

from studyroom.models import *

"""
    FBV
    -> Function Based View

    CBV
    -> Class Based View
"""

"""
    Default Django

    RESTful-API
    - Django-restframework
    React.js
    Android
    iOS
"""


class PostList(ListView):
    model = Post
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(is_activated=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(
            category=None).count()

        return context

class MyPostList(ListView):
    model = Post
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(Q(author=user)) | user.participate_posts.all()
        queryset = queryset.distinct()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyPostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(
            category=None).count()

        return context


class PostSearch(PostList):
    def get_queryset(self):
        q = self.kwargs['q']
        object_list = Post.objects.filter(
            Q(title__contains=q) | Q(content__contains=q))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostSearch, self).get_context_data()
        context['search_info'] = 'Search: "{}"'.format(self.kwargs['q'])
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        post = self.get_object()
        applicate_posts = user.applicate_posts.filter(pk=post.pk)
        participate_posts = user.participate_posts.filter(pk=post.pk)

        context = super(PostDetail, self).get_context_data(**kwargs)

        if applicate_posts:
            context['is_applicate'] = True
        else:
            context['is_applicate'] = False

        if participate_posts:
            context['is_participate'] = True
        else:
            context['is_participate'] = False

        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(
            category=None).count()
        context['comment_form'] = CommentForm()
        context['user'] = user

        return context

    def post(self, request, *args, **kwargs):
        user = request.user

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        user_id = request.POST.get('user_id', '')
        check_level = request.POST.get('check_level', '')
        check_status = request.POST.get('check_status', '')
        check_thr = request.POST.get('check_thr', '')
        bank_account = request.POST.get('bank_account', '')

        post = self.get_object()

        new_reg = RegForm.objects.create(
            post = post,
            name = name,
            email = email,
            user_id = user_id,
            check_level = check_level,
            check_status = check_status,
            check_thr = check_thr,
            bank_account = bank_account,
        )

        post.applicant.add(user)

        # send mail
        title = 'Hi, {}.'.format(user.username)
        message = 'Hi, {}.\nThis is email Test. \n환불 받을 계좌 주소 : {}'.format(user.username, bank_account)

        send_mail(
            title, # 제목
            message, # 내용
            'no-reply@example.com',     # 보내는 이메일  (settings에 설정해서 작성안해도 됨)
            [post.author.email, email],     # 받는 이메일 리스트
            fail_silently=False,
        )

        return redirect('/blog/')


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'title', 'content', 'head_image', 'category', 'tags'
    ]

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else:
            return redirect('/blog/')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = [
        'title', 'content', 'head_image', 'category', 'tags'
    ]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data(**kwargs)

        post = self.get_object()
        applicants = post.applicant.all()

        context['applicants'] = applicants
        context['is_activated'] = post.is_activated

        return context

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            applicant_confirm = list(
                map(int, self.request.POST.getlist('applicant_confirm', [])))
            applicant_cancel = list(
                map(int, self.request.POST.getlist('applicant_cancel', [])))
            participants_cancel = list(
                map(int, self.request.POST.getlist('participants_cancel', [])))

            target = self.get_object()
            # 지원자 삭제
            target.applicant.remove(*applicant_cancel)
            # 지원자 승인
            target.participants.add(*applicant_confirm)
            target.applicant.remove(*applicant_confirm)
            # 참여자 삭제
            target.participants.remove(*participants_cancel)

            # form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else:
            return redirect('/blog/')


class PostListByTag(ListView):
    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        tag = Tag.objects.get(slug=tag_slug)

        return tag.post_set.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(
            category=None).count()
        tag_slug = self.kwargs['slug']
        context['tag'] = Tag.objects.get(slug=tag_slug)

        return context


class PostListByCategory(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)
        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(
            category=None).count()

        slug = self.kwargs['slug']

        if slug == '_none':
            context['category'] = '기타'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        # context['title'] = 'Blog - {}'.format(category.name)
        return context


def new_comment(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.get_absolute_url())
        else:
            return redirect('/')


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Scomment
    form_class = CommentForm

    def get_object(self, queryset=None):
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')
        return comment


def delete_comment(request, pk, studyroom_pk):
    comment = Scomment.objects.get(pk=pk)
    post = comment.post
    if request.user == comment.author:
        comment.delete()
        return redirect('/studyroom/study_room/' + str(studyroom_pk) + '/')
    else:
        raise PermissionError('Comment 삭제 권한이 없습니다.')


def delete_post(request, pk):
    model = Post.objects.get(pk=pk)
    model.delete()
    return redirect('/blog/')


def confirm_applicant(request, post_pk, user_pk):

    post = Post.objects.get(pk=post_pk)
    user = User.objects.get(pk=user_pk)

    post.applicant.remove(user)
    post.participants.add(user)

    response = {
        "result": "confirm"
    }

    new_comment_room = CommentRoom.objects.create(
        post=post,
        participant=user
    )

    return JsonResponse(response)

def toggle_activate(request, pk):
    post = Post.objects.get(pk=pk)

    post.is_activated = not post.is_activated
    post.save()

    return JsonResponse({
        "result" : "toggle activate",
        "status" : post.is_activated
    })


# def post_detail(request, pk):
#     blog_post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'blog_post': blog_post,
#         }
#     )

# def index(request):
#     posts = Post.objects.all()
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts' : posts,
#         }
#     )

from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse, resolve_url
from .models import (
    CardSet, Card, TrySet,
    TryRecord, MissionSoundModel, MissionImageModel,
    Notice, UploadBase, CommentRoom, UploadFileModel
)
from django.urls import reverse
from blog.models import *
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Max, F
from django.utils import timezone
from .forms import *
import random
import csv
import io
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class CardSetList(ListView):
    model = CardSet
    paginate_by = 4
    template_name = 'studyroom/cardset_list.html'

    def dispatch(self, request, *args, **kwargs):
        pk = int(self.kwargs.get('pk', 0))
        post = get_object_or_404(Post, pk=pk)

        # 참여한 포스트일경우만 접근 가능
        if request.user != post.author and not post.participants.all().filter(pk=request.user.pk).exists():
            return HttpResponseRedirect("/")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        pk = int(self.kwargs.get('pk', 0))
        post = get_object_or_404(Post, pk=pk)
        return CardSet.objects.filter(post=post).order_by('post_id')

    def calc_my_average(self, cardset, user):
        # 자기 자신의 카드셋 별 평균
        # 스터디룸 아이디로 카드셋을 검색하고
        # 카드셋 별 마지막 트라이셋 검색
        cardsets = CardSet.objects.filter(post__id=cardset)
        trysets = []
        for cardset in cardsets:
            tryset = cardset.trysets.filter(user=user, is_finished=True).order_by(
                '-started_at').first()
            if tryset:
                trysets.append(tryset)

        total = []
        for ts in trysets:
            correct = ts.correct
            incorrect = ts.incorrect
            total_length = correct + incorrect
            total.append(correct/total_length *
                         100 if total_length > 0 else 0)

        if len(total) > 0:
            from functools import reduce
            return reduce(lambda x, y: x + y, total) / len(trysets)
        else:
            return 0

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CardSetList, self).get_context_data(**kwargs)
        post_id = int(self.kwargs.get('pk', 0))
        user = self.request.user

        context['comment_form'] = CommentForm()
        context['category_list'] = Category.objects.all()
        context['cardset_id'] = post_id
        context['posts_without_category'] = Post.objects.filter(
            category=None).count()
        context['my_average'] = self.calc_my_average(
            post_id, self.request.user)
        post = get_object_or_404(Post, pk=post_id)
        context['post'] = post
        if user == post.author:
            comment_room = post.comment_rooms.all()
        else:
            comment_room = CommentRoom.objects.filter(
                post=post, participant=user)
        context['comment_rooms'] = comment_room
        try:
            context['youtube_url'] = post.youtube_url.all()[0]
        except:
            context['youtube_url'] = None
        context['sound_files'] = post.sound_files.all()

        average = 0
        for p in post.participants.all():
            average += self.calc_my_average(post_id, p)
        participants_count = post.participants.all().count()

        participants = post.participants.all()
        for participant in participants:
            for cardset in post.cardsets.all():
                tryset = TrySet.objects.filter(
                    user=participant, cardset=cardset)
                if not tryset:
                    participants_count -= 1
                break

        if participants_count > 0:
            average /= participants_count
        else:
            average = 0

        context['average'] = average
        context['notice_form'] = NoticeForm()
        # 공지사항 가져오기
        context['notices'] = Notice.objects.filter(
            post=post).order_by('-created_at')

        # 업로드 리스트
        uploads = UploadBase.objects.filter(post=post)
        context['uploads'] = uploads.order_by('-created_at')
        context['upload_form'] = UploadBaseForm()

        # 업로드 통계
        upload_total = uploads.count()
        upload_detail = {}
        for p in post.participants.all():
            upload_detail[p.username] = {}
            upload_detail[p.username]['value'] = 0
            upload_detail[p.username]['background_color'] = 'rgba(0, 0, 0, 0.2)'
            upload_detail[p.username]['border_color'] = 'rgba(0, 0, 0, 1)'

            for u in uploads:
                imgs = MissionImageModel.objects.filter(base=u, user=p)
                snds = MissionSoundModel.objects.filter(base=u, user=p)

                if imgs.exists():
                    upload_detail[p.username]['value'] += 1
                    continue

                if snds.exists():
                    upload_detail[p.username]['value'] += 1
                    continue

            upload_detail[p.username]['value'] /= 4
            upload_detail[p.username]['value'] *= 100

            if p == user:
                upload_detail[p.username]['background_color'] = 'rgba(54, 162, 235, 0.2)'
                upload_detail[p.username]['border_color'] = 'rgba(54, 162, 235, 1)'

        context['upload_chart_data'] = upload_detail

        return context


def write_notice(request, pk):
    # form으로 처리
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        form = NoticeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post
            obj.author = request.user
            obj.save()
        else:
            pass
    return redirect(reverse('studyroom:study_room', args=[pk]))


def write_upload(request, pk):
    # form으로 처리
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        form = UploadBaseForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post
            obj.save()
        else:
            pass
    return redirect(reverse('studyroom:study_room', args=[pk]))


def get_card(tryset, cardset):
    card_ids = []
    for tr in tryset.records.all():
        card_ids.append(tr.card.id)

    available_cards = Card.objects.filter(
        card_set=cardset
    ).exclude(
        id__in=card_ids
    )

    if not available_cards.exists() or len(card_ids) >= cardset.limit:
        return None

    # random.seed(a=None)

    return available_cards[random.randint(0, available_cards.count() - 1)]


def get_random_card(card_id, samples=1):
    return list(Card.objects.exclude(id=card_id).order_by('?'))[:samples]


def try_view(request, pk):
    """ 카드셋의 pk를 입력받아 해당 카드셋에 포함된 문제 1개 반환 """

    cardset = get_object_or_404(CardSet, pk=pk)

    # 현재 진행중인 tryset이 있는지 확인
    # 현재 시각에서 제한시간(임시로 5분)을 빼고 그 시간보다 큰 tryset이 있는지 확인
    now = timezone.now()
    limit = timezone.timedelta(minutes=5)
    start_limit = now - limit

    tmp_trysets = TrySet.objects.filter(started_at__gte=start_limit, user=request.user, cardset=cardset,
                                        is_finished=False).order_by('-started_at')
    target_card = None

    if tmp_trysets.exists():
        # 시작된 후 종료되지 않은 풀이가 존재.
        # 이어서 문제 풀이 진행
        tryset = tmp_trysets.first()

    else:
        # 시작된 풀이가 없음
        # 새로 만듬 or 에러페이지로 이동
        tryset = TrySet(
            user=request.user,
            cardset=cardset
        )
        tryset.save()

    if request.method == 'GET':
        # cardset에 포함된 풀지 않은 문제들 중 하나를 선택하여 반환
        target_card = get_card(tryset, cardset)
        if target_card is None:
            tryset.is_finished = True
            tryset.save()
            return HttpResponseRedirect(f'/try/{tryset.id}/result/')

    elif request.method == 'POST':

        # 정답 저장
        # 선택된 카드가 없을경우에 대하여 생각해봐야함.
        cid = int(request.POST.get('cid', 0))
        cresult = request.POST.get('cresult', '-')

        selected_card = get_object_or_404(Card, pk=cid)

        new_record = TryRecord(
            tryset=tryset,
            card=selected_card,
            result=cresult
        )
        new_record.save()

        if cresult == selected_card.back:
            tryset.correct += 1
        else:
            tryset.incorrect += 1
        tryset.save()

        target_card = get_card(tryset, cardset)
        if target_card is None:
            tryset.is_finished = True
            tryset.save()

            tryset.records.all().delete()

            return HttpResponseRedirect(f'/studyroom/try/{tryset.id}/result/')

    incorrects = get_random_card(target_card.id, 3)
    incorrects += list(Card.objects.filter(pk=target_card.pk))
    incorrects = sorted(incorrects, key=lambda x: random.random())

    return render(request, 'studyroom/cardset_try.html', {
        'card': target_card,
        'cards': incorrects,
        'category_list': Category.objects.all(),
        'posts_without_category': Post.objects.filter(category=None).count()
    })

    # from django.db.models import F 를 이용하여 result와 card.back의 값을 비교한다


def tyr_result(request, pk):
    # tryset 가져오기
    tryset = get_object_or_404(TrySet, pk=pk)
    correct_count = tryset.correct
    incorrect_count = tryset.incorrect
    return render(request, 'studyroom/cardset_try_result.html', {
        'tryset': tryset,
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'total': correct_count + incorrect_count,
        'category_list': Category.objects.all(),
        'posts_without_category': Post.objects.filter(category=None).count()
    })


def tyr_result_total(request, pk):
    total = []
    # tryset 가져오기
    post = get_object_or_404(Post, pk=pk)
    now = timezone.now()
    limit = timezone.timedelta(minutes=5)
    start_limit = now - limit
    target_ts = TrySet.objects.filter(
        Q(user=request.user) & Q(cardset__post=post) & (
            Q(is_finished=True) | Q(started_at__lt=start_limit))
    ).distinct().order_by('-started_at')
    for ts in target_ts:
        correct = ts.records.all().filter(card__back=F('result'))
        incorrect = ts.records.all().exclude(card__back=F('result'))

        total.append({
            'tryset': ts,
            'correct': correct,
            'correct_count': len(correct),
            'incorrect': incorrect,
            'incorrect_count': len(incorrect),
            'total': len(correct) + len(incorrect),
        })

    return render(request, 'studyroom/cardset_try_result_total.html', {
        'total': total,
        'post': post,
        'category_list': Category.objects.all(),
        'posts_without_category': Post.objects.filter(category=None).count()
    })


def cardset_upload(request, pk):
    if request.method == "GET":
        return render(request, "studyroom/upload.html", {
            'form': UploadFileForm()
        })

    elif request.method == "POST":
        print(request.FILES)
        # data = csv.DictReader(request.FILES['cardset'])
        # data = csv.DictReader(request.FILES['file'])
        post = get_object_or_404(Post, pk=pk)

        name, ext = os.path.splitext(request.FILES['file'].name)

        cardset = CardSet(
            post=post,
            name=name
        )
        cardset.save()

        tmp = request.FILES['file'].read()
        decoded_file = tmp.decode('utf-8')
        io_string = io.StringIO(decoded_file)
        data = csv.reader(io_string)

        for row in data:
            new_card = Card(
                card_set=cardset,
                front=row[0],
                back=row[1]
            )
            new_card.save()
        return render(request, "studyroom/upload.html", {
            'form': UploadFileForm()
        })
    else:
        return HttpResponseRedirect("/")


def mission_upload(request, pk):
    # cardset = get_object_or_404(CardSet, pk=pk)
    base = get_object_or_404(UploadBase, pk=pk)
    my_img = MissionImageModel.objects.filter(base=base)
    my_snd = MissionSoundModel.objects.filter(base=base)

    if base.post.author != request.user:
        my_img = my_img.filter(user=request.user)
        my_snd = my_snd.filter(user=request.user)

    if request.method == "GET":
        return render(request, "studyroom/mission_upload.html", {
            'base': base,
            'iform': MissionImageForm(),
            'sform': MissionSoundForm(),
            'imgs': my_img,
            'snds': my_snd
        })

    elif request.method == "POST":
        # print(request.FIELS)
        t = request.POST.get('type', None)
        if t is not None:
            if t == 'img':
                form = MissionImageForm(request.POST, request.FILES)
            else:
                form = MissionSoundForm(request.POST, request.FILES)

            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.base = base
                obj.save()
            else:
                print("invalid form")

        return render(request, "studyroom/mission_upload.html", {
            'base': base,
            'iform': MissionImageForm(),
            'sform': MissionSoundForm(),
            'imgs': my_img,
            'snds': my_snd
        })
    else:
        return HttpResponseRedirect("/")


def study_room(request):
    return render(
        request,
        'study_room.html'
    )


def create_comment(request, pk, username):
    post = Post.objects.get(pk=pk)
    user = request.user

    if post.author != user:
        comment_room = CommentRoom.objects.get(post=post, participant=user)
    else:
        participant = User.objects.get(username=username)
        print(username, participant)
        comment_room = CommentRoom.objects.get(
            post=post, participant=participant)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.comment_room = comment_room
            comment.author = request.user
            comment.save()
            return redirect('/studyroom/study_room/' + str(pk) + '/')
        else:
            return redirect('/studyroom/study_room/' + str(pk) + '/')


@csrf_exempt
def change_youtube_url(request, pk):
    post = Post.objects.get(pk=pk)

    url = request.POST.get('url_text', '')
    url = url.replace('watch?v=', 'embed/')
    url = url.split("&")[0]

    try:
        youtube_url = post.youtube_url.all()[0]
        youtube_url.video_url = url
        youtube_url.save()
    except:
        youtube_url = YoutubeUrl.objects.create(
            post=post,
            video_url=url
        )

    return JsonResponse({"result": "change"})


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

    if request.user == comment.author:
        comment.delete()
        return redirect('/studyroom/study_room/' + str(studyroom_pk) + '/')
    else:
        raise PermissionError('Comment 삭제 권한이 없습니다.')


def delete_image(request, image_pk):
    image = MissionImageModel.objects.get(pk=image_pk)

    image.delete()

    return JsonResponse({
        "result": "image delete"
    })


def delete_sound(request, sound_pk):
    sound = MissionSoundModel.objects.get(pk=sound_pk)

    sound.delete()

    return JsonResponse({
        "result": "sound delete"
    })


def delete_notice(request, notice_pk):
    notice = Notice.objects.get(pk=notice_pk)

    notice.delete()

    return JsonResponse({
        "result": "notice delete"
    })


def create_vocatest(request, post_id):
    post = Post.objects.get(pk=post_id)

    name = request.POST.get('vocatest_name', 'default name')
    limit = request.POST.get('vocatest_limit', '20')

    new_cardset = CardSet.objects.create(
        post=post,
        name=name,
        limit=int(limit)
    )

    return redirect(reverse('studyroom:study_room', args=[post_id]))


def register_csv(request, post_id, cardset_id):
    post = Post.objects.get(pk=post_id)
    cardset = CardSet.objects.get(pk=cardset_id)

    csv_file = request.FILES.getlist('cardset_csv')

    upload_file = UploadFileModel.objects.create(
        file=csv_file[0]
    )

    with open(upload_file.file.path, 'r', encoding='UTF8') as f:
        reader = csv.reader(f)
        name, ext = os.path.splitext(os.path.basename(upload_file.file.path))

        for row in reader:
            new_card = Card(
                card_set=cardset,
                front=row[0],
                back=row[1]
            )
            new_card.save()

    return redirect(reverse('studyroom:study_room', args=[post_id]))


def register_sound(request, post_id):
    post = Post.objects.get(pk=post_id)

    title = request.POST.get('sound_file_title', '')
    sound_file = request.FILES.getlist('sound_file')

    new_sound = SoundUrl.objects.create(
        title=title,
        sound_file=sound_file[0],
        post=post
    )

    return redirect(reverse('studyroom:study_room', args=[post_id]))


def delete_week_sound(request, sound_id):
    sound_file = SoundUrl.objects.get(pk=sound_id)
    sound_file.delete()

    return JsonResponse({
        "result": "delete week sound"
    })
from django.views import View
from django.template import loader
from .forms import ArtistForm, UserForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import NewArtist, Scene, Voice
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


def get_ending(number, word):
    """
    Возвращает слово завка или музыкант с соответствующим числу окончанием.
    Например, 1 - заявКА, музыканТ
              2 - заявКИ, мазыканТА
              5 - заявОК, музыкантОВ
    word: 1 - заявка, 2 - музыкант
    """
    number = str(number)
    if number[-1] == '1' and number[-2:-1] != '11':
        return 'зявка' if word == 1 else 'музыкант'
    elif number[-1] in ['2', '3', '4'] and number[-2:-1] not in ['12', '13', '14']:
        return 'заявки' if word == 1 else 'музыканта'
    else:
        return 'заявок' if word == 1 else 'музыкантов'


class MainPage(View):

    def get(self, request, *args, **kwargs):
        template = loader.get_template('main_page.html')
        scenes = Scene.objects.all()
        artists_wait = NewArtist.objects.filter(status='under_consideration').count()
        artists_accepted = NewArtist.objects.filter(status='accepted')
        artists_accepted_number = artists_accepted.count()
        context = {'scenes': scenes,
                   'artists_wait': artists_wait,
                   'artists_accepted': artists_accepted,
                   'artists_accepted_number': artists_accepted_number,
                   'artists_wait_ending': get_ending(artists_wait, 1),
                   'artists_accepted_ending': get_ending(artists_accepted_number, 2)}
        return HttpResponse(template.render(context, request))


@login_required(login_url='/login_required/')
@permission_required('fest_app.can_create', login_url='/denied')
def new_artist_form(request):
    template = loader.get_template('artist_form.html')

    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user)

            new_artist = form.save(commit=False)
            new_artist.user = user
            new_artist.save()

            user.user_permissions.add(35)
            user.user_permissions.remove(34)
            user.save()

            return HttpResponseRedirect(reverse_lazy('status'))

    if request.method == 'GET':
        data = {'form': ArtistForm()}
        return HttpResponse(template.render(data, request))


@login_required(login_url='/login_required/')
@permission_required('fest_app.see_status', login_url='/denied')
def artist_form_done(request):
    template = loader.get_template('artist_form_done.html')
    return HttpResponse(template.render(request=request))


@login_required(login_url='/login_required/')
@permission_required('fest_app.can_vote', login_url='/denied')
def voting_page(request):
    template = loader.get_template('voting_page.html')
    context = {'artists': NewArtist.objects.filter(status='under_consideration').order_by('id')}
    if request.method == 'GET':
        return HttpResponse(template.render(context, request))

    if request.method == 'POST':
        artist = NewArtist.objects.get(id=request.POST['artist_id'])
        censor = User.objects.get(id=request.user.id)
        voice = request.POST['voice']

        saved_voice = Voice.objects.filter(censor=censor, artist=artist).first()

        if saved_voice:
            """
            Если голос уже был, значит он меняется (кнопка старого голоса неактивна)
            Вычитаем старый голос, добавляем новый в модели NewArtist
            Сохраняем запись о новом голосе в модели Voice
            """
            current_voice = saved_voice.voice                   # текщий (старый) голос, например 'voices_for'
            current_voices = getattr(artist, current_voice)     # текущее значение голосов 'voices_for'
            setattr(artist, current_voice, current_voices - 1)  # вычитаем голос

            current_voices = getattr(artist, voice)             # теперь берем значение нового голоса
            setattr(artist, voice, current_voices + 1)          # увеличиваем его на 1
            artist.save()                                       # сохраняем изменения

            saved_voice.voice = voice                           # меняем значенеи голоса в модели Voice на новое
            saved_voice.save()                                  # сохраняем запись о новом голосе
        else:
            """
            Если голос - новый
            Создаем запись о том, какой голос произаедён в модели Voice
            (соответствующая клавиша голосования теперь заблокирована)
            Увеличиваем соответствующий счетчик в модели NewArtist
            """
            Voice.objects.create(censor=censor, artist=artist, voice=voice)
            current_voices = getattr(artist, voice)
            setattr(artist, voice, current_voices + 1)
            artist.save()

        return HttpResponse(template.render(context, request))


class Registration(View):

    def get(self, request, *args, **kwargs):
        template = loader.get_template('register.html')
        context = {'form': UserForm()}
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        template = loader.get_template('register.html')
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            new_user.user_permissions.add(34)  # 34 - can_create 35 - see_status
            new_user.save()
            login(request, user=new_user)

            return HttpResponseRedirect(reverse_lazy('main'))
        else:
            return HttpResponse(template.render({'form': form}, request))


def access_denied(request):
    template = loader.get_template('access_denied.html')
    return HttpResponse(template.render(request=request))


@login_required(login_url='/login_required/')
@permission_required('fest_app.see_status', login_url='/denied')
def status_page(request):
    template = loader.get_template('status_page.html')
    artist = NewArtist.objects.get(user=request.user)
    img_dict = {
        'under_consideration': 'voting.jpg',
        'accepted': 'happy.jpg',
        'denied': 'sorry.jpg'
    }
    context = {'artist': artist,
               'img': img_dict[artist.status]}
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login_required/')
@permission_required('fest_app.can_vote', login_url='/denied')
def scene_info(request):
    template = loader.get_template('scene_info.html')
    data = {'scenes': Scene.objects.all()}
    return HttpResponse(template.render(data, request))


class ArtistDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'fest_app.can_vote'
    model = NewArtist
    template_name = 'artist_info.html'


@login_required(login_url='/login_required/')
@permission_required('fest_app.can_vote', login_url='/denied')
def voting_decision(request):
    artist = NewArtist.objects.get(id=request.POST['artist_id'])
    decision = request.POST['status']

    if decision == 'accepted':
        template = loader.get_template('artist_success.html')
        context = {'scenes': Scene.objects.all(),
                   'artist': artist}
        return HttpResponse(template.render(context, request))

    elif decision == 'denied':
        artist.status = decision
        artist.save()
        return HttpResponseRedirect(reverse_lazy('voting_page'))


def correct_vacant_places(scene, day, time):
    """
    Увеличивает соответствующий счетчик занятых мест в моделе Scene.
    Возвращает True, если это возможно (есть свободные места)
    Возвращает False, если свободных мест нет
    """
    day_dict = {1: 'first_day_',
                2: 'second_day_'}

    day_time = day_dict[int(day)] + time
    counter_plan = getattr(scene, day_time + '_plan')
    counter_fact = getattr(scene, day_time + '_fact')

    print(scene.name)
    print(day)
    print(time)

    print(day_time)
    print(counter_plan)
    print(counter_fact)

    if counter_plan - counter_fact > 0:
        setattr(scene, day_time + '_fact', counter_fact + 1)
        scene.save()
        return True
    else:
        return False


@login_required(login_url='/login_required/')
@permission_required('fest_app.can_vote', login_url='/denied')
def voting_done(request):

    if request.method == 'POST':
        scene = Scene.objects.get(name=request.POST['scene'])
        artist = NewArtist.objects.get(id=request.POST['artist_id'])

        if artist.status == 'accepted':  # Если кто-то из других цензоров уже проголосовал
            return HttpResponseRedirect(reverse_lazy(voting_page))

        else:

            if correct_vacant_places(scene, request.POST['day'], request.POST['time']):
                artist.day = request.POST['day']
                artist.time_slot = request.POST['time']
                artist.scene = scene
                artist.status = 'accepted'
                artist.save()
                return HttpResponseRedirect(reverse_lazy(voting_page))

            else:
                template = loader.get_template('artist_success.html')
                context = {'scenes': Scene.objects.all(),
                           'artist': artist,
                           'scene_error': True}
                return HttpResponse(template.render(context, request))


@login_required(login_url='/login_required/')
@permission_required('fest_app.can_vote', login_url='/denied')
def accepted_list(request):
    template = loader.get_template('accepted_list.html')
    context = {'artists': NewArtist.objects.exclude(status='under_consideration')}
    return HttpResponse(template.render(context, request))

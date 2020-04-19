from django import template
from ..models import Voice, NewArtist
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page


register = template.Library()


@register.filter(name='humanread')
def humanread(value):
    """
    Переводит значение, схраненное в БД в удобочитаемое значение
    """

    humanreadable_values = {
        'red': 'Красная',
        'blue': 'Синяя',
        'green': 'Арбузик',
        'solo': 'Соло',
        'group': 'Группа',
        'under_consideration': 'Заявка на рассмотрении',
        'accepted': 'Участие подтверждено',
        'denied': 'Заяка отклонена',
        'day': 'День',
        'noon': 'День',
        'evening': 'Вечер',
        'night': 'Поздний вечер'
    }

    return humanreadable_values[value]


@register.filter(name='two_arguments')
def two_arguments(value, arg):
    """
    Функция - прослойка
    Позволяет применить template фильр к двум аргументам
    Необходима для be_voted
    """
    return value, arg


@register.filter(name='be_voted')
def be_voted(value, voice):
    """
    Фильтр необходим чтобы сделать кнопку текущего голоса (ранее сделанного) неактивной
    Возвращает True, если значение в модели Voice соответствует аргументу voice
    """
    artist, user = value
    current_voice = Voice.objects.filter(censor=user, artist=value).first()
    if current_voice:
        return current_voice.voice == voice


@cache_page(5)
@register.filter(name='can_be_accepted')
def can_be_accepted(artist_id):
    """
    Фильтр, проверяющий можно ли активировать кнопку "ПРИНЯТЬ" и "ОТКАЗАТЬ"
    """
    censors_number = User.objects.filter(groups__name='Censors').count()
    artist = NewArtist.objects.get(id=artist_id)

    if artist.total_voices == censors_number:

        if artist.voices_for > artist.voices_against:
            return 'accept'
        else:
            return 'deny'

    elif artist.voices_for - artist.voices_against >= 3:

        if artist.voices_against >= 5:
            return 'both_options'
        else:
            return 'accept'

    elif artist.voices_against >= 5:
        return 'deny'

from django.db import models
from django.contrib.auth.models import User


class Scene(models.Model):
    name = models.CharField(max_length=5,
                            unique=True,
                            choices=[
                                ('red', 'Красная'),
                                ('blue', 'Синяя'),
                                ('green', 'Арбузик')
                            ],
                            default='red')
    info = models.TextField()

    first_day_noon_plan = models.PositiveSmallIntegerField(default=0)
    first_day_evening_plan = models.PositiveSmallIntegerField(default=0)
    first_day_night_plan = models.PositiveSmallIntegerField(default=0)

    first_day_noon_fact = models.PositiveSmallIntegerField(default=0)
    first_day_evening_fact = models.PositiveSmallIntegerField(default=0)
    first_day_night_fact = models.PositiveSmallIntegerField(default=0)

    second_day_noon_plan = models.PositiveSmallIntegerField(default=0)
    second_day_evening_plan = models.PositiveSmallIntegerField(default=0)
    second_day_night_plan = models.PositiveSmallIntegerField(default=0)

    second_day_noon_fact = models.PositiveSmallIntegerField(default=0)
    second_day_evening_fact = models.PositiveSmallIntegerField(default=0)
    second_day_night_fact = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class NewArtist(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    alias = models.CharField(max_length=50)
    format = models.CharField(max_length=5,
                              choices=[
                                  ('solo', 'Я выстапую один'),
                                  ('group', 'Мы - группа')],
                              default='solo')
    scene = models.ForeignKey(Scene,
                              on_delete=models.SET_NULL,
                              null=True)
    day = models.SmallIntegerField(choices=[(1, 'Первый день'), (2, 'Второй день')],
                                   default=1)
    time_slot = models.CharField(max_length=7,
                                 choices=[('day', 'День'), ('evening', 'Вечер'), ('night', 'Поздний вечер')],
                                 default='evening')
    info = models.TextField()
    status = models.CharField(max_length=19,
                              choices=[
                                  ('under_consideration', 'Заявка на рассмотрении'),
                                  ('accepted', 'Участие подтверждено'),
                                  ('denied', 'Заяка отклонена')
                              ],
                              default='under_consideration')
    voices_for = models.SmallIntegerField(default=0)
    voices_against = models.SmallIntegerField(default=0)
    voices_abstain = models.SmallIntegerField(default=0)
    total_voices = models.SmallIntegerField()

    def get_total_voices(self):
        return self.voices_for + self.voices_against + self.voices_abstain

    def save(self, *args, **kwargs):
        self.total_voices = self.get_total_voices()
        super(NewArtist, self).save(*args, **kwargs)

    class Meta:
        permissions = [('can_vote', 'Может голосовать'),
                       ('can_create', 'Может создавать заявку'),
                       ('see_status', 'Просматривать статус')]


class Voice(models.Model):
    """
    Сохраняет голоса цензоров
    """
    censor = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    artist = models.ForeignKey(NewArtist,
                               on_delete=models.CASCADE)
    voice = models.CharField(max_length=14)

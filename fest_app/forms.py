from django import forms
from .models import NewArtist, Scene
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя',
                               help_text='Будет использоваться для входа в Ваш профиль')
    email = forms.EmailField(label='Электронная почта')
    first_name = forms.CharField(label='Ваше имя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    username.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})
    first_name.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})
    password2.widget.attrs.update({'class': 'form-control'})

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают! Повторите ввод.')
        return cd['password2']

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name']


class ArtistForm(forms.ModelForm, forms.ModelChoiceField):

    def __init__(self, *args, **kwargs):
        super(ArtistForm, self).__init__(*args, **kwargs)

        self.fields['scene'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        humanreadable_values = {
            'red': 'Красная',
            'blue': 'Синяя',
            'green': 'Арбузик'}
        return humanreadable_values[obj.name]

    alias = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Сценическое имя/название группы')
    format = forms.ChoiceField(choices=[
                                  ('solo', 'Я выстапую один'),
                                  ('group', 'Мы - группа')],
                               label='Выберите формат выступления')
    scene = forms.ModelChoiceField(queryset=Scene.objects.all(),
                                   label='Выберите сцену',
                                   empty_label=None,
                                   help_text='Сцена может быть изменена по усмотрению организаторов.')
    day = forms.ChoiceField(choices=[(1, 'Первый день'), (2, 'Второй день')],
                            label='Выберите день',
                            help_text='День может быть изменен организаторами. Время назначается организаторами.')
    info = forms.CharField(widget=forms.Textarea(attrs={'rows': 5,
                                                        'class': 'form-control'}),
                           label='Расскажите о себе')

    format.widget.attrs.update({'class': 'form-control'})
    scene.widget.attrs.update({'class': 'form-control'})
    day.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = NewArtist
        fields = ['alias',
                  'format',
                  'scene',
                  'day',
                  'info',
                  ]



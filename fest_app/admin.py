from django.contrib import admin
from . models import NewArtist, Scene


class SceneAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'info',
                    'first_day_noon_plan',
                    'first_day_evening_plan',
                    'first_day_night_plan',
                    'second_day_noon_plan',
                    'second_day_evening_plan',
                    'second_day_night_plan')
    readonly_fields = ('first_day_noon_fact',
                       'first_day_evening_fact',
                       'first_day_night_fact',
                       'second_day_noon_fact',
                       'second_day_evening_fact',
                       'second_day_night_fact')


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'alias', 'format', 'scene', 'day', 'info', 'status')
    readonly_fields = ('voices_for', 'voices_against', 'voices_abstain', 'total_voices')


admin.site.register(Scene, SceneAdmin)
admin.site.register(NewArtist, ArtistAdmin)

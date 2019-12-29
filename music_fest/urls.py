"""music_fest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fest_app import views as fest_view
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', fest_view.MainPage.as_view(), name='main'),
    path('new_artist/', fest_view.new_artist_form, name='new_artist_form'),
    path('status/', fest_view.artist_form_done, name='status'),
    path('my_status/', fest_view.status_page, name='artist_status'),
    path('voting/', fest_view.voting_page, name='voting_page'),
    path('voting/decision/', fest_view.voting_decision),
    path('voting/done/', fest_view.voting_done),
    path('accepted/', fest_view.accepted_list),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login_required/', LoginView.as_view(template_name='login_required.html'), name='login_required'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', fest_view.Registration.as_view(), name='registration'),
    path('denied/', fest_view.access_denied, name='access_denied'),
    path('scene_info/', fest_view.scene_info, name='scene_info'),
    path('artists/<int:pk>/', fest_view.ArtistDetail.as_view()),

    path('admin/', admin.site.urls),
]

# Todo: проверка статуса перед голосованием
"""my_site_prj URL Configuration

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
from django.urls import path, include
from . import views
# from django.contrib.auth.views import LoginView, LogoutView

app_name = 'studyroom'
urlpatterns = (
    path('study_room/', views.study_room, name='index'),
    path('study_room/<int:pk>/', views.CardSetList.as_view(), name='study_room'),
    path('study_room/<int:pk>/create_comment/<str:username>/',
         views.create_comment, name='create_comment'),
    path('upload/<int:pk>/', views.cardset_upload, name='upload'),
    path('upload-base/<int:pk>/', views.write_upload, name='upload-base'),
    path('mission_upload/<int:pk>/', views.mission_upload, name='mission-upload'),
    path('write_notice/<int:pk>/', views.write_notice, name='write_notice'),
    path('try/<int:pk>/', views.try_view, name='try'),
    path('try/<int:pk>/result/', views.tyr_result, name='try_result'),
    path('try/<int:pk>/total/', views.tyr_result_total, name='try_result_total'),
    path('change-url/<int:pk>/', views.change_youtube_url,
         name='change_youtube_url'),
    path('edit_comment/<int:pk>/<int:studyroom_pk>/',
         views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/<int:studyroom_pk>/', views.delete_comment),
    path('delete_image/<int:image_pk>/', views.delete_image),
    path('delete_sound/<int:sound_pk>/', views.delete_sound),
    path('delete_notice/<int:notice_pk>/', views.delete_notice),
    path('create_vocatest/<int:post_id>/', views.create_vocatest),
    path('register_csv/<int:post_id>/<int:cardset_id>/', views.register_csv),
    path('register_sound/<int:post_id>/', views.register_sound),
    path('delete_week_sound/<int:sound_id>/', views.delete_week_sound),
)

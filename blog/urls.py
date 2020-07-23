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
app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='index'),
    path('my/', views.MyPostList.as_view(), name="my_post"),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('tag/<str:slug>/', views.PostListByTag.as_view()),
    path('category/<str:slug>/', views.PostListByCategory.as_view()),
    path('edit_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/<int:studyroom_pk>/', views.delete_comment),
    path('<int:pk>/new_comment/', views.new_comment),
    path('<int:pk>/update/', views.PostUpdate.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('create/', views.PostCreate.as_view()),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post'),
    path('applicant/confirm/<int:post_pk>/<int:user_pk>/', views.confirm_applicant),
    path('applicant/cancel/<int:post_pk>/<int:user_pk>/', views.cancel_applicant),
    path('participant/cancel/<int:post_pk>/<int:user_pk>/',
         views.cancel_participant),
    path('toggle/<int:pk>/', views.toggle_activate)

]

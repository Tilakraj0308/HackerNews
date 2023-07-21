from django.urls import path
from . import views


urlpatterns=[
    path('', views.home, name='home'),
    path('new/', views.new, name='new'),
    path('thread/', views.thread, name='thread'),
    path('comment/', views.comment, name='comment'),
    path('submit/', views.submit, name='submit'),
    path('login/', views.logPage, name='login_form'),
    path('register/', views.registerPage, name='register_form'),
    path('upvote/<str:mod>/<str:pk>', views.upvote, name='upvote'),
    path('dvote/<str:mod>/<str:pk>', views.dvote, name='dvote'),
    path('item/', views.items, name='items'),
    path('user/', views.profile, name='user'),
    path('userItems/', views.getprofileItems, name='userItems'),
]
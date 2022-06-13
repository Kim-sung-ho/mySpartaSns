from django.urls import path
from . import views

#sign_up_view,sign_in_view를 연결하고 이걸sign-up,sgin-in 으로부르겠다.
urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user-list'),
    path('user/follow/<int:id>', views.user_follow, name='user-follow'),
]

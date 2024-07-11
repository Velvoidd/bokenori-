from django.urls import path
from . import views
from django.contrib import admin
from .views import apply, application_success
from django.views.generic import TemplateView
from .views import user_added

urlpatterns = [
    path('base/', views.base_view, name='base'),
    path('', views.index, name='index'),
    path('login/', views.login_site, name='login'),
    path('register/', views.registration_page, name= 'registration_page'),
    path('logout/', views.logout_site, name='logout'),
    path('apply/', views.apply, name='apply'),
    path('apply/', views.submit_application, name='apply'),
    path('apply/success/', application_success, name='application_success'),
    path('application_exists/', views.application_exists, name='application_exists'),
    path('application_list/', views.applications_list, name='applications_list'),
    path('application_detail/<int:pk>/', views.application_detail, name='application_detail'),
    path('update_application_status/<int:pk>/', views.update_application_status, name='update_application_status'),
    path('custom_user_created/', views.custom_user_created, name='custom_user_created'),
    path('players/', views.player_list, name='player_list'),
    path('info/', views.server_info, name='server_info'),
    path('rules/', views.rules_page, name='rules'),
    path('application/delete/<int:pk>/', views.delete_application, name='delete_application'),
    path('minecraftuser/add/', views.add_minecraft_user, name='add_minecraft_user'),
    path('user_added/', user_added, name='user_added'),
    path('edit/<int:player_id>/', views.edit_player, name='edit_player'),
    path('player_list_adm/<int:player_id>/delete_player/', views.delete_player, name='delete_player'),
    path('player_list_adm/<int:player_id>/confirm_delete/', views.confirm_delete, name='confirm_delete'),
    path('player_list_adm', views.player_list_adm, name='player_list_adm'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('news/add/', views.create_news, name='create_news'),
    path('welcome/', views.welcome, name='welcome'),
    path('event_list/', views.event_list, name='event_list'),
    path('add_event/', views.add_event, name='add_event'),
    path('edit_event/<int:pk>/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('event_delete/<int:pk>/', views.delete_event, name='delete_event'),
    path('map/', views.map_view, name='map'),
    path('chat/', views.chat, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
]




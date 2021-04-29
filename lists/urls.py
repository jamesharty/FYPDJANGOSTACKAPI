from django.urls import path
from . import views


urlpatterns = [
    path('savedLists', views.savedLists, name='savedLists'),
    path('<int:list_id>/', views.userList, name='userList'),
    path('removeList/<int:list_id>/', views.removeList, name='removeList'),
    path('removeUserList/<int:list_id>/', views.removeUserList, name='removeUserList'),

]


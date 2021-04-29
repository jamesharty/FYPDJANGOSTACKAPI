from django.urls import path
from . import views
urlpatterns = [
    path('searchResults', views.results, name='results'),
    path('moreInfo', views.moreInfo, name='moreInfo')
]

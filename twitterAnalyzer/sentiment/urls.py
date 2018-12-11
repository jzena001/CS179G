from django.urls import path

from . import views

app_name = 'sentiment'

urlpatterns = [
    path('', views.index, name='index'),
    # /sentiment/detail
    path('hashtag/detail/<str:tag>/', views.detail, name='tag-detail'),
    # /sentiment/results
    #path('search/results/?page=<int:page>', views.results, name='search-results'),
]

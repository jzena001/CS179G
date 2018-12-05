from django.urls import path

from . import views

app_name = 'sentiment'

urlpatterns = [
    path('', views.index, name='index'),
    # /sentiment/detail
    path('<str:tag>/', views.detail, name='tag-detail'),
    # /sentiment/results
    path(r'^/page/(?P<page>\d+/$', views.results, name='search-results'),
]
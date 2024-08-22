from django.urls import path

from . import views

urlpatterns = [
    path('test', views.test),
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('lecture', views.lecture, name='lecture')
]
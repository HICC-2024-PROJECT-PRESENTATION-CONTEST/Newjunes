from django.urls import path

from . import views

urlpatterns = [
    path('test', views.test),
    path('', views.index, name='index'),
    path('select', views.select, name='select'),
    path('lecture', views.lecture, name='lecture'),
    path('break', views.set_break, name='break')
]
from django.urls import path

from . import views

urlpatterns = [
    path('test', views.test),
    path('', views.index, name='index'),
    path('select', views.select, name='select'),
    path('break', views.set_break, name='break'),
    path('result', views.result, name='result'),
    path('lecture', views.lecture, name='lecture'),
    path('generate', views.generate, name='generate'),
    path('generate-table-html', views.generate_table_html)
]
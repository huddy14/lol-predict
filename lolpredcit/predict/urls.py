from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search', views.search, name='search'),
    url(r'^about', views.about, name='about'),
    url(r'^statistics$', views.statistics, name='statistics'),
    url(r'^statistics/simple.png$', views.accuracy_grid, name='accuracy_grid'),
]

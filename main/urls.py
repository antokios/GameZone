from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^games/(?P<filter>[\w|\W]+)/$', views.games, name='games'),
    url(r'^reviews/$', views.reviews, name='reviews'),
    url(r'^videos/(?P<filter>[\w|\W]+)/$', views.videos, name='videos'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^game/(?P<pk>\w+)/$', views.game_single, name='game_single'),
    url(r'^review/(?P<rev>\w+)/$', views.review_single, name='review_single'),
    url(r'^game_videos/(?P<vid>\w+)/$', views.video_single, name='video_single'),
    url(r'^404/$', views.error404, name='404'),
    url(r'^search_results/(?P<filter>[\w|\W]+)/$', views.search_results, name='search_results'),
]
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views


app_name = 'cricket'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^matchstatistics/(?P<matchid>[0-9]+)/$', views.matchstatitics, name='matchstatistics'),
    url(r'^clubapproval/(?P<tournamentid>[0-9]+)/$', views.teamapproval, name='clubapproval'),
    url(r'^approval/$', views.approvaltry, name="approval"),
    url(r'^rejection/$', views.rejectiontry, name="rejection"),
    url(r'^mmmm/(?P<tournamentid>[0-9]+)/$', views.matchschedule, name="mmmm"),
    url(r'^matchentry/$', views.matchentry, name="matchentry"),
    url(r'^eventdisplay/$', views.eventdisplay, name="eventdisplay"),
    url(r'^editevent/$', views.editevent, name="editevent"),
    url(r'^updatematch/$', views.updatematch, name="updatematch"),
    url(r'^updateevent/$', views.updateevent, name="updateevent"),
    url(r'^tournament/(?P<tournamentid>[0-9]+)/$', views.tournament, name='tournament'),
    url(r'^ballbyball/(?P<matchid>[0-9]+)/$', views.ballbyball, name='ballbyball'),
    url(r'^ballentry/$', views.ballentry, name='ballentry'),
    url(r'^tossupdate/$', views.tossupdate, name='tossupdate'),
    url(r'^finishinnings/$', views.finishinnings, name='finishinnings'),
    url(r'^noticedisplay/$', views.noticedisplay, name='noticedisplay'),
    url(r'^searchevent/$', views.searchevent, name='searchevent'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

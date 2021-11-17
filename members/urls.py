from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'members'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^cricketteamsignup/$', views.signupofcricketteam.as_view(),name='cricketteamsignup'),
    url(r'^trainingsignup/$', views.training_signup, name='trainingsignup'),
    url(r'^listtrainingrequests/$', views.training_requests, name='listtrainingrequests'),
    url(r'^scorersignup/$', views.scorersignup, name='scorersignup'),
    url(r'^createevent/$', views.createvent, name='createevent'),
    url(r'^evententry/$', views.evententry, name='evententry'),
    url(r'^teamprofile/$', views.teamprofile, name='teamprofile'),
    url(r'^registerforevent/$', views.registerforevent, name='registerforevent'),
    url(r'^login/$', views.loginuser, name='login'),
    url(r'^logout/$', views.logoutuser, name='logout'),
    url(r'^registered/$', views.registered, name='registered'),
    url(r'^ajax/validate_username/$', views.ajaxvalidation, name='ajaxvalidation'),
    url(r'^profileupdate/$', views.updateprofile, name='profileupdate'),
    url(r'^askquery/$', views.askquery, name='askquery'),
    url(r'^notice/$', views.notice, name='notice'),
    url(r'^notifications/(?P<userid>[0-9]+)/$',views.notifications, name='notifications'),
    url(r'^queries/$', views.queries, name='queries'),
    url(r'^training/$', views.training, name='training'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

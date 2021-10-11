from members import views
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

handler404 = 'cricket.views.handler404'
handler500 = 'cricket.views.handler500'


urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^cricket/', include('cricket.urls')),
    url(r'^members/', include('members.urls')),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(),
        {
        'template_name': 'members/password_reset_form.html',
        'email_template_name': 'members/password_reset_email.html',
        'subject_template_name': 'members/password_reset_subject.txt'
    },
        name='password_reset'),


    url(r'^password_reset_done/$', auth_views.PasswordResetDoneView.as_view(),
        {
        'template_name': 'members/password_reset_done.html'
    },
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetCompleteView.as_view(), {
            'template_name': 'members/password_reset_confirm.html'
        },

        name='password_reset_confirm'),

    url(r'^reset_done/$', auth_views.PasswordResetCompleteView.as_view(),
        {'template_name': 'members/password_reset_complete.html'},
        name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

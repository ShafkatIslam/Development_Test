from django.conf.urls import url
from django.conf import settings
from Developments_Test import views
from django.conf.urls.static import static

app_name = 'Developments_Test'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^home/$', views.home, name='home'),
    url(r'^other-post/$', views.otherpost, name='other-post'),
    url(r'^(?P<id>[0-9]+)/post-details/$', views.postdetails, name='post-details' ),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'website.views.home', name='home'),
    url(r'^table/$', 'website.views.table', name='table'),
    url(r'^accounts/register/$', 'website.views.userregister', name='userregister'),
    url(r'^accounts/login/$', 'website.views.user_login', name='user_login'),
    url(r'^add/$', 'website.views.add_workshop', name='add_workshop'),
    url(r'^slot_details/(?P<slot_id>\d+)/$', 'website.views.slot_details', name='slot_details'),

    url(r'^book/(?P<workshop_id>\d+)/$', 'website.views.book_slot', name='book_slot'),
    url(r'^details/(?P<workshop_id>\d+)/$', 'website.views.details', name='details'),
    url(r'^edit/(?P<workshop_id>\d+)/$', 'website.views.edit_workshop', name='edit_workshop'),
    url(r'^delete/(?P<workshop_id>\d+)/$', 'website.views.delete', name='delete'),
    url(r'^slots/(?P<workshop_id>\d+)/$', 'website.views.slots', name='slots'),

    )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from .views import IndexView, CalendarView

urlpatterns = [
    url(r'^admin/rq/', include('django_rq.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social_django.urls', namespace='social')),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^cal/(?P<slug>\w+).ics$', CalendarView.as_view(), name='calendar'),
    url('^$', IndexView.as_view()),
]

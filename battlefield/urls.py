"""battlefield URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from home import views as views_home
from django.conf.urls.static import static
from world import init_views as world_views
from world import views as main_views 
from world import message_views as message_views
from django.contrib.auth import views as auth_views 
from world import update
from threading import Thread
import sys
#from djutils.decorators import async

urlpatterns = [
	url(r'^$', views_home.index, name = 'index'), #Works
	url(r'^about/$', views_home.about, name = 'about'), #Works
	url(r'^tutorial/$', views_home.tutorial, name = 'tutorial'), #Works
	url(r'^developers/$', views_home.developers, name = 'developers'), #Works
	url(r'^pricing/$', views_home.pricing, name = 'pricing'), #Works
	url(r'^sponsors/$', views_home.sponsors, name = 'sponsors'), #Works
	url(r'^private/$', views_home.private, name = 'private'), #Create template
	url(r'^register/$', world_views.register, name = 'register'), # Add mail
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',world_views.activate, name='activate'), #Works
	url(r'^login/$', auth_views.login, {'template_name': 'game/login.html'}, name='login'), #Works
	url(r'^fields/$', main_views.fields, name = 'fields'), # Works
	url(r'^center/$', main_views.center, name = 'center'), # Works
	url(r'^pop_ranking/$', main_views.pop_ranking, name = 'population ranking'), #Works
	url(r'^attack_ranking/$', main_views.attack_ranking, name = 'attack ranking'), #Works
	url(r'^defense_ranking/$', main_views.def_ranking, name = 'def ranking'), #Works
	url(r'^weekly/$', main_views.weekly_ranking, name = 'weekly ranking'), # Works
	url(r'^fields/(?P<pos>[0-9o-s_]+)/$', main_views.field, name = 'field'),
	url(r'^fields/(?P<pos>[0-9o-s_]+)/upgrade/$', main_views.upgrade_field, name = 'upfield'),
	url(r'^center/(?P<pos>[0-9o-s_]+)/$', main_views.get_building, name = 'building'),
	url(r'^center/(?P<pos>[0-9o-s_]+)/upgrade/$', main_views.upgrade_building, name = 'upbuilding'),
	url(r'^map/$', main_views.map_zero, name = 'map'),
	url(r'^map/x=(?P<x>[0-9-]+)y=(?P<y>[0-9-]+)/$', main_views.maps, name = 'map'),
	url(r'^village/x=(?P<x>[0-9-]+)y=(?P<y>[0-9-]+)/$', main_views.village_view, name = 'village'),
	url(r'^center/(?P<pos>[0-9o-s_]+)/(?P<bui>[0-9A-Za-z-]+)/$', main_views.build, name = 'build'),
	url(r'^gold/$', main_views.gold, name = 'gold'),
	url(r'^gold/(?P<arg>[0-9a-z]+)/$', main_views.buy, name = 'buy'),
	url(r'^messages/inbox/$', message_views.inbox, name ='inbox'),
	url(r'^messages/write/$', message_views.send, name ='write'),
	url(r'^messages/write/(?P<mes>[0-9]+)/$', message_views.reply, name ='write'),
	url(r'^messages/sent/$', message_views.sent, name ='sent'),
	url(r'^messages/(?P<mes>[0-9]+)/$', message_views.view_message, name ='view'),
	url(r'^admin/', admin.site.urls),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404='battlefield.views.handler404'
if sys.argv[1] == 'runserver':
	t = Thread(target = world_views.init_map(), args = (), kwargs = {})
	t.setDaemon(True)
	t.start()
	
	#@async
	t = Thread(target = update.queue, args = (), kwargs = {})
	t.setDaemon(True)
	t.start()

	t = Thread(target = update.population, args = (), kwargs = {})
	t.setDaemon(True)
	t.start()

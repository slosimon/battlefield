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
from world import views as world_views
from django.contrib.auth import views as auth_views 

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
	url(r'^login/$', auth_views.login, {'template_name': 'game/login.html'}, name='login'),
	url(r'^fields/$', world_views.fields, name = 'fields'),
	url(r'^map_init/$', world_views.init_map, name = 'map_init'),
    url(r'^admin/', admin.site.urls),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404='battlefield.views.handler404'

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

urlpatterns = [
	url(r'^$', views_home.index, name = 'index'), 
	url(r'^about/$', views_home.about, name = 'about'),
	url(r'^tutorial/$', views_home.tutorial, name = 'tutorial'),
	url(r'^developers/$', views_home.developers, name = 'developers'),
	url(r'^pricing/$', views_home.pricing, name = 'pricing'),
	url(r'^sponsors/$', views_home.sponsors, name = 'sponsors'),
	url(r'^private/$', views_home.private, name = 'private'),
    url(r'^admin/', admin.site.urls),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404='battlefield.views.handler404'

"""orchestrator URL Configuration

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
from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from django.contrib import admin
from django.views import generic
from material.frontend import urls as frontend_urls

from django.conf.urls import include, url, handler404, handler500

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = [

    url(r'^', include('visaweb.urls'), name='home'),

    url(r'^admin/', admin.site.urls),
    url(r'', include(frontend_urls)),


    # url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^assetadapter/', include('assetadapter.urls')),
    url(r'^processengine/', include('processengine.urls')),
    url(r'^rmd/', include('rmd.urls')),

]

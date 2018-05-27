"""airconditioning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from .import view

urlpatterns = [
    url(r'^login$', view.login),
    url(r'^logsubmit$', view.loginsubmit),
    url(r'^client$', view.initial),
    url(r'^onoff$', view.onoff),
    url(r'^wind0$', view.wind0),
    url(r'^wind1$', view.wind1),
    url(r'^wind2$', view.wind2),
    url(r'^up$', view.up),
    url(r'^down$', view.down),
]

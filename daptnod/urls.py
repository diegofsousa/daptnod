"""daptnod URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('daptnod.notes.urls', namespace='notes')),
    path('accounts/', include('daptnod.accounts.urls', namespace='accounts')),

    # debug toolbar
    path('__debug__/', include(debug_toolbar.urls)),
]

handler404 = 'daptnod.core.views.handler404'
handler403 = 'daptnod.core.views.handler403'
handler500 = 'daptnod.core.views.handler500'

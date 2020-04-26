"""HelloDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

import os
from django.views.generic.base import RedirectView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('comments.urls')),
    # path(r'favicon.ico', RedirectView.as_view(url=r'/static/favicon.ico')),
]



#
# from django.conf import settings
# from django.conf.urls.static import static
# if settings.DEBUG:
#     media_root = os.path.join(settings.BASE_DIR, '')
#     urlpatterns += static('/media2/', document_root=media_root)
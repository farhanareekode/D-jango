"""hospital_managment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

admin.site.site_header = "Hospital administator"
admin.site.site_title = "Life care administator"
admin.site.index_title = "Life care administator"

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('home.urls')),
                  path('accounts/', include('accounts.urls')),
                  path('payments/', include('payments.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

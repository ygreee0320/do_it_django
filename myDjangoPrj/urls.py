"""myDjangoPrj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ #IP주소/
    path('admin/', admin.site.urls),  # IP주소/admin이 온다면 url로 연결(admin.site.urls)
    path('blog/', include('blog.urls')), # IP주소/blog이 온다면 blog url로 연결
    path('', include('single_pages.urls')),   # IP주소/ admin,blog 제외한 모든것
    path('accounts/', include('allauth.urls'))  # 로그인 하는 url 연결
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
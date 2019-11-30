"""onehand URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path, re_path

from django_registration.backends.one_step.views import RegistrationView

from core.views import IndexTemplateView
from users.forms import CustomUserForm

from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls import url

# DEBUG 모드인 경우 핫스왑을 사용하기 위해 파일을 각각 나눔

if settings.DEBUG:
    index_url = 'index-dev.html'
else:
    index_url = 'index.html'
    
urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/register/',
        RegistrationView.as_view(
            form_class=CustomUserForm,
            success_url='/'
        ), name='django_registration_register'),
    

    path('accounts/',
        include('django_registration.backends.one_step.urls')),

    path('accounts/',
        include('django.contrib.auth.urls')),

    path('api/',
        include('users.api.urls')),

    path('api/',
        include('questions.api.urls')),

    path('api-auth/',
        include('rest_framework.urls')),

    path('api/rest-auth/',
        include('rest_auth.urls')),

    path('api/rest-auth/registration/',
        include('rest_auth.registration.urls')),
           
    re_path(r"^.*$", IndexTemplateView.as_view(), name='entry-point')
    # url(r'^$', TemplateView.as_view(template_name=index_url))    
]
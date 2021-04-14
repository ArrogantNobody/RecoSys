"""RecoSys URL Configuration

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
from django.urls import path
from RecoFramework import loginController, newuser_form

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginController.login_map),
    path('session_test/', loginController.login_success),
    path('login/', loginController.ccid_verify),
    path('popup/', newuser_form.pop),
    path('data_update/', newuser_form.form_process)


]

"""organizator_api URL Configuration

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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

base_path: str = "organizator-api"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{base_path}/events/", include("app.events.infrastructure.http.urls")),
    path(f"{base_path}/users/", include("app.users.infrastructure.http.urls")),
    path(
        f"{base_path}/applications/",
        include("app.applications.infrastructure.http.urls"),
    ),
    path(f"{base_path}/questions/", include("app.questions.infrastructure.http.urls")),
    path("api-auth/", include("rest_framework.urls")),
]

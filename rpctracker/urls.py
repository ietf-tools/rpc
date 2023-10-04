"""
URL configuration for rpc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path

from rpc import views
from rpc import api as rpc_api


urlpatterns = [
    path("admin/", admin.site.urls),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("login/", views.index),
    path("api/rpc/clusters/", rpc_api.clusters),
    path("api/rpc/clusters/<int:number>", rpc_api.cluster),
    path("api/rpc/profile", rpc_api.profile),
    path("api/rpc/rpc_person/", rpc_api.rpc_person),
    path("api/rpc/submissions/", rpc_api.submissions),
    path("api/rpc/queue/", rpc_api.queue),
]

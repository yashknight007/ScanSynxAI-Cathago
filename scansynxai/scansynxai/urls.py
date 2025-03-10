"""
URL configuration for scansynxai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import register_user, login_user, profile_view, scan_upload, get_uploaded_documents, request_credits, approve_credit_request, list_credit_requests,admin_analytics, landing_page,dashboard
from docs.views import  find_matches
from django.conf import settings    
from django.conf.urls.static import static

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("dashboard/", dashboard, name="dashboard"),
    path("admin/analytics/", admin_analytics, name="admin_analytics"),
    path("admin/", admin.site.urls),
    path("auth/register/", register_user, name="register"),
    path("auth/login/", login_user, name="login"),
    path("user/profile/", profile_view, name="profile"),
    path("scan/upload/", scan_upload, name="scan_upload"),
    path("matches/<int:doc_id>/",  find_matches, name="find_matches"),
    path("documents/", get_uploaded_documents, name="get_uploaded_documents"),
    path("credits/request", request_credits, name="request_credits"),
    path("credits/approve/<int:request_id>/", approve_credit_request, name="approve_credit_request"),
    path("credits/list/", list_credit_requests, name="list_credit_requests"),
    path("admin/analytics/", admin_analytics, name="admin_analytics"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from  django.conf.urls.static import static
from contentscour import settings

from . import views

urlpatterns = [
    path("get_csrf/", views.get_csrf),
    path("login/", views.login),
    path("logout/", views.logout),
    path("session/", views.session),
    path("whoami/", views.whoami),
]
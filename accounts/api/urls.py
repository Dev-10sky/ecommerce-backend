from django.urls import include, path
from django.contrib.auth import views
from .views import CustomRegisterView, CustomLoginView

urlpatterns = [
    path("login/",CustomLoginView.as_view(),name='login'),
    # path("", include("rest_auth.urls")),
    path("register/", include("rest_auth.registration.urls")),
]

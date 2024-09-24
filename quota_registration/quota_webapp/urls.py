from django.urls import path

from quota_webapp import views

urlpatterns = [
    path("", views.index),
    path("sign-in", views.sign_in, name="sign-in"),
    path("sign-out", views.sign_out),
    path("dashboard", views.dashboard, name="dashboard"),
]

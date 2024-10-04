from django.urls import path

from quota_webapp import views

urlpatterns = [
    path("", views.index),
    path("sign-up", views.sign_up, name="sign-up"),
    path("sign-in", views.sign_in, name="sign-in"),
    path("sign-out", views.sign_out),
    path("dashboard", views.dashboard, name="dashboard"),
    path("add/<course_ID>", views.add),
    path("delete/<course_ID>", views.delete)
]

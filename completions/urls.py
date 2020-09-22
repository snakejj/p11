from django.urls import path

from . import views


app_name = "completions"

urlpatterns = [
    path("", views.complete, name="complete")
]

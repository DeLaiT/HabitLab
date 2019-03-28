from django.urls import path
from server import views

urlpatterns = [
    path('gitlab_event/', views.GitlabEvents.as_view())
]

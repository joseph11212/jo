from django.urls import path
from .views import create_result, view_result

urlpatterns = [
    path("create/", create_result, name="create-result"),
    path('result/', view_result, name='view-result'),
]


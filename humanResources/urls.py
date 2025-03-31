from django.urls import path
from humanResources.views import HrRequestNewView

urlpatterns = [
    path('add/', HrRequestNewView.as_view(), name='add'),
]

from django.urls import path
from equipments.views import EquipmentView, EquipmentAddView


urlpatterns = [
    path('', EquipmentView.as_view(), name='equipments'),
    path('add/', EquipmentAddView.as_view(), name='add_equipment'),
]

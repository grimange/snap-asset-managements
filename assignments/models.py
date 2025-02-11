from django.db import models
from django.contrib.auth import get_user_model
from equipments.models import Equipment

class AssignCampaign(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class AssignEquipment(models.Model):
    assignee = models.ForeignKey(get_user_model(), related_name='assignee_user', on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    campaign = models.ForeignKey(AssignCampaign, on_delete=models.CASCADE)
    deployment = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)

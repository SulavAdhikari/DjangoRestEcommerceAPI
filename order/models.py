from django.db import models
from Users.models import User

# Create your models here.

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ordering_user")
    cloth = models.ForeignKey("cloths.Cloths", on_delete=models.CASCADE, related_name="ordered_cloth")
    is_accepted = models.BooleanField(default=False)
    shipping_addr = models.CharField(max_length=200,null=False, blank=False)
    
from datetime import datetime
from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from Users.models import User
# Create your models here.

class Notification(models.Model):
    date = models.DateTimeField(default=datetime.now())
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        data = {
            'date':self.date,
            'notification':str(self.text)
            }
        async_to_sync(channel_layer.group_send)(
            str(self.user.id), {
                'type':'send_notification',
                'value': json.dumps(data)
            }
        )

        super(Notification, self).save(*args,**kwargs)
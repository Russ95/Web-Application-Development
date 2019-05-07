from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Event(models.Model):
    MY_CHOICES = (
        ('Software_Development', 'Software_Development'),
        ('Reference', 'Reference'),
        ('Entertainment', 'Entertainment'),
        ('Social', 'Social'),
        ('Unknown', 'Unknown'),
    )
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)  #the user posting this twitter
    title = models.CharField(max_length=200)
    # description = models.TextField()
    category = models.CharField(max_length=200,choices=MY_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    #category = models.TextField()

    @property
    def get_html_url(self):
        url = reverse('time_manage:event_edit', args=(self.id,))
        # url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

class Item(models.Model):
    process_name = models.CharField(max_length=200)
    ip_addr = models.GenericIPAddressField()
    update_time = models.DateTimeField()
    create_time = models.DateTimeField()
    type = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    def __unicode__(self):
        return self.text


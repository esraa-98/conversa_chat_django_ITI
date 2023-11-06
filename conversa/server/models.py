from collections.abc import Iterable
from django.db import models
from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)  #required
    description = models.TextField(blank=True,null=True)  #not required
    
    def __str__(self):
        return self.name
    
class Server(models.Model):
    name = models.CharField(max_length=100)  #required
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="server_owner")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="server_category")
    description = models.CharField(max_length=250,blank=True,null=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
       return self.name

class Channel(models.Model):
    name = models.CharField(max_length=100)  #required
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="channel_owner")
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(Server,on_delete=models.CASCADE,related_name="channel_server")
    
    # customize save func -> turn name into lowercase before saving to db
    def save(self,*args,**kwargs):
        self.name = self.name.lower()
        return super(Channel,self).save(args,kwargs)

    def __str__(self):
        return self.name
    




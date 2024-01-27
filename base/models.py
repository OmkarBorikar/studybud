from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self): # Without this actual topic names will not be displayed on apge or form
        return str(self.name) 

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank = True) # empty value is acceptable , by defualt it is not allowed
    participants = models.ManyToManyField(User , related_name='participants',blank = True)
    updated = models.DateTimeField(auto_now=True) # timestamp every time row is updated
    created = models.DateTimeField(auto_now_add = True) # timestamp when created

    class Meta:
        ordering = ['-updated' , '-created'] # updated is ascending order , -updated is descending order . 

    def __str__(self):
        return str(self.name) 
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room , on_delete=models.CASCADE) # Room is parent table of message . If row from room is deleted cascade will delete all related rows from message table
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) # timestamp every time row is updated
    created = models.DateTimeField(auto_now_add = True) # timestamp when created
    class Meta:
        ordering = ['-updated' , '-created'] # updated is ascending order , -updated is descending order . 
    def __str__(self):
        return str(self.body[0:50])
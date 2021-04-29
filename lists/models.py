from django.db import models
from django.conf import settings

# Create your models here.
class List(models.Model):
    listID = models.AutoField(primary_key=True)
    userName = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listName = models.CharField(max_length=200)
    def __int__(self):
        return self.listID
        
class UserList(models.Model):
    id = models.AutoField(primary_key=True)
    listID = models.ForeignKey(List, on_delete=models.CASCADE)
    userDisplayName = models.CharField(max_length=200)
    profileImage = models.CharField(max_length=200)
    profileLink = models.CharField(max_length=200)
    reputation = models.IntegerField()
    location = models.CharField(max_length=200)
    tagName = models.CharField(max_length=200)
    answerScore = models.IntegerField()
    answerCount = models.IntegerField()
    bronzeCount = models.IntegerField()
    silverCount = models.IntegerField()
    goldCount = models.IntegerField()
    def __str__(self):
        return self.userDisplayName  
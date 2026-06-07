from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'
    
    
class InfoModel(models.Model):
    GENDER_TYPE = [
        ('male','male'),
        ('female','female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='user_info')
    name = models.CharField(null=True,max_length=100)
    age = models.PositiveIntegerField(null=True,blank=True)
    profile_image = models.ImageField(
        upload_to='profile_image/',
        blank=True,
        null=True,
        max_length=50
    )
    gender = models.CharField(null=True,blank=True, choices=GENDER_TYPE,max_length=100)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    bmr = models.FloatField(null=True)
    def __str__(self):
        return f'{self.name}'
    
class ConsumedCalModel(models.Model):
    item_name = models.CharField(max_length=100, null=True)
    calorie = models.FloatField(null=True)
    created_by = models.DateTimeField(auto_now_add=True,null=True)
    consumed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_calorie',null=True)
    def __str__(self):
        return f'{self.item_name} - {self.consumed_by.username}'
    

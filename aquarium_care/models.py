from django.db import models
from datetime import timedelta
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
import datetime
import random

class Aquarium(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    pincode = models.IntegerField(validators=[MaxValueValidator(4)], blank=True, null=True)
    pollution = models.IntegerField(validators=[MaxValueValidator(100)], default=100)
    money = models.IntegerField(default=0)

class BaseAquariumCreature(models.Model):
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE)
    satiety = models.IntegerField(validators=[MaxValueValidator(100)], default=100)
    is_alive = models.BooleanField(default=True)
    gender = models.BooleanField()
    time_of_birth = models.DateTimeField()
    time_of_sell = models.DateTimeField(null=True, blank=True)
    time_of_breeding = models.DateTimeField(null=True, blank=True)
    is_sold = models.BooleanField(default=False)
    cost = models.IntegerField(default=0)
    
    class Meta:
        abstract = True 

    def save(self, *args, **kwargs):
        if not self.time_of_sell:
            self.time_of_sell = self.time_of_birth + self.sell_time_offset
        if not self.time_of_breeding:
            self.time_of_breeding = self.time_of_birth + self.breeding_time_offset
        if not self.cost:
            self.cost = self.cost_offset
            
        super(BaseAquariumCreature, self).save(*args, **kwargs)

class Shrimp(BaseAquariumCreature):
    sell_time_offset = timedelta(minutes=30)
    breeding_time_offset = timedelta(minutes=15)
    cost_offset = 5

class Fish(BaseAquariumCreature):
    sell_time_offset = timedelta(hours=1)
    breeding_time_offset = timedelta(minutes=30)
    cost_offset = 15

class Snail(BaseAquariumCreature):
    sell_time_offset = timedelta(hours=2)
    breeding_time_offset = timedelta(hours=1)
    cost_offset = 30

class Fugue(BaseAquariumCreature):
    sell_time_offset = timedelta(hours=4)
    breeding_time_offset = timedelta(hours=2)
    cost_offset = 60
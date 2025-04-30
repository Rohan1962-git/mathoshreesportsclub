from django.db import models

# Create your models here.
class User(models.Model):
    uid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    password=models.CharField(max_length=100)
    contact=models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Book_Turf(models.Model):
    bid=models.AutoField(primary_key=True)
    uid=models.IntegerField()
    name=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
    mobile=models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=40)
    password=models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Event(models.Model):
    eid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()
    
    def __str__(self):
        return self.name


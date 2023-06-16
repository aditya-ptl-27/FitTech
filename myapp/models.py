from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	profile_pic=models.ImageField(upload_to="profile_pic/",default="static 'img/user_default.jpg' ")
	password=models.CharField(max_length=100)
	usertype=models.CharField(max_length=100,default='user')

	def __str__(self):
		return self.fname+" - "+self.lname

class Workout(models.Model):
	trainer=models.ForeignKey(User,on_delete=models.CASCADE)
	w_type=models.CharField(max_length=100)
	w_name=models.CharField(max_length=100)
	w_description=models.TextField(default='null')
	w_difficulty=models.CharField(max_length=50)
	w_muscles_targeted=models.CharField(max_length=100)
	w_gif=models.ImageField(upload_to='workout_gifs/')

	def __str__(self):
		return self.trainer.fname+' - '+self.w_name

class Bmi(models.Model):
	height=models.PositiveIntegerField()
	weight=models.PositiveIntegerField()

	def __str__(self):
		return self.height+" - "+self.weight
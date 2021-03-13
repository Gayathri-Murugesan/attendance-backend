from django.db import models
from rest_framework.authtoken.models import Token
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


# Create your models here.
# permission table 
# credential table
# department table 
# student table 
    
class class_room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=200)
    building = models.CharField(max_length=200)
    campus = models.CharField(max_length=200)

class department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=200)
    institution_name = models.CharField(max_length=200)

class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    dept_id = models.ForeignKey(department, on_delete=CASCADE)
    address = models.CharField(max_length=200)
    phone_no = models.BigIntegerField()

class course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_string = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    dept_id = models.ForeignKey(department, on_delete=CASCADE)
    term = models.CharField(max_length=200)
    year = models.IntegerField()

class session(models.Model):
    session_id = models.AutoField(primary_key=True)
    session_name = models.CharField(max_length=200)
    course_id = models.ForeignKey(course, on_delete=CASCADE)
    dept_id = models.ForeignKey(department, on_delete=CASCADE)
    faculty_id = models.ForeignKey(User, on_delete=CASCADE)
    room_id = models.ForeignKey(class_room, on_delete=CASCADE)

class course_enrolled(models.Model):
    student_id = models.ForeignKey(User, on_delete=CASCADE)
    dept_id = models.ForeignKey(department, on_delete=CASCADE)
    course_id = models.ForeignKey(course, on_delete=CASCADE)
    session_id = models.ForeignKey(session, on_delete=CASCADE)
    term = models.CharField(max_length=200)
    year = models.IntegerField()

class attendance(models.Model): 
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    dept_id = models.ForeignKey(department, on_delete=CASCADE)
    course_id = models.ForeignKey(course, on_delete=CASCADE)
    session_id = models.ForeignKey(session, on_delete=CASCADE)
    attendance = models.BooleanField()
    date = models.DateField()
    marked_by = models.CharField(max_length=100)
    


    

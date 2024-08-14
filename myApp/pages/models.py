from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField()

class Course(models.Model):
    name = models.CharField(max_length=255)
    student = models.ForeignKey(Student, related_name="courses",on_delete=models.CASCADE)
    

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData.get('first_name', '')) < 2:
            errors["first_name"] = "First name should be at least 2 characters!"
        if len(postData.get('last_name', '')) < 2:
            errors["last_name"] = "Last name should be at least 2 characters!"
        import re
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex,postData.get('email')) :
            errors["email"] = "Enter a valid email address!"
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

        password = postData.get('password', '')
        if not re.match(password_regex,password):
            errors["password"] = "Enter a valid Password!"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    
    objects = UserManager()


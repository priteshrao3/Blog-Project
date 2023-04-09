from django.db import models
from django.db.models.fields import CharField, EmailField, TextField

# Create your models here.
# Contact Data
class Contact(models.Model):
    name = CharField(max_length=150)
    email = EmailField(max_length=200)
    subject = CharField(max_length=250)
    message = TextField()

# For Home Page Data
class Post(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()



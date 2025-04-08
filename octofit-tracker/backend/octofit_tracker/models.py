from djongo import models

class User(models.Model):
    _id = models.ObjectIdField()
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class Team(models.Model):
    _id = models.ObjectIdField(primary_key=True)  # Use ObjectIdField for primary key
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

class Activity(models.Model):
    _id = models.ObjectIdField(primary_key=True)  # Use ObjectIdField for primary key
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # Duration in minutes
    date = models.DateField()

class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True)  # Use ObjectIdField for primary key
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    points = models.IntegerField()

class Workout(models.Model):
    _id = models.ObjectIdField(primary_key=True)  # Use ObjectIdField for primary key
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)

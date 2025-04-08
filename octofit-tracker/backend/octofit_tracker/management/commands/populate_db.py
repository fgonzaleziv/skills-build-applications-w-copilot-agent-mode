from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        # Ensure only fully saved Team objects are processed during deletion
        for team in Team.objects.filter(id__isnull=False):
            team.members.clear()
        Team.objects.filter(id__isnull=False).delete()
        # Ensure proper deletion of User objects
        User.objects.filter(id__isnull=False).delete()

        # Refresh each user after creation to ensure valid primary keys
        users = []
        user_data = [
            {'email': 'thundergod@mhigh.edu', 'name': 'Thor', 'age': 30},
            {'email': 'metalgeek@mhigh.edu', 'name': 'Tony Stark', 'age': 35},
            {'email': 'zerocool@mhigh.edu', 'name': 'Steve Rogers', 'age': 32},
            {'email': 'crashoverride@mhigh.edu', 'name': 'Natasha Romanoff', 'age': 28},
            {'email': 'sleeptoken@mhigh.edu', 'name': 'Bruce Banner', 'age': 40},
        ]
        for data in user_data:
            user = User.objects.create(**data)
            users.append(User.objects.get(pk=user.pk))

        # Refresh users from the database
        users = list(User.objects.all())

        # Create teams
        team1 = Team.objects.create(name='Blue Team')
        team2 = Team.objects.create(name='Gold Team')
        team1.members.add(*users[:3])
        team2.members.add(*users[3:])

        # Create activities
        activities = [
            Activity(user=users[0], activity_type='Cycling', duration=60, date=date(2025, 4, 8)),
            Activity(user=users[1], activity_type='Crossfit', duration=120, date=date(2025, 4, 7)),
            Activity(user=users[2], activity_type='Running', duration=90, date=date(2025, 4, 6)),
            Activity(user=users[3], activity_type='Strength', duration=30, date=date(2025, 4, 5)),
            Activity(user=users[4], activity_type='Swimming', duration=75, date=date(2025, 4, 4)),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=team1, points=300),
            Leaderboard(team=team2, points=250),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event', difficulty='Medium'),
            Workout(name='Crossfit', description='High-intensity functional training', difficulty='Hard'),
            Workout(name='Running Training', description='Training for a marathon', difficulty='Medium'),
            Workout(name='Strength Training', description='Weightlifting and strength exercises', difficulty='Hard'),
            Workout(name='Swimming Training', description='Training for a swimming competition', difficulty='Medium'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
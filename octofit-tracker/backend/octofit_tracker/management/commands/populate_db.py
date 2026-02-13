from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        
        # Delete existing data using Django ORM
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('✓ Existing data deleted'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Avengers Assemble! The mightiest heroes of Earth.'
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League! Defenders of truth and justice.'
        )
        
        self.stdout.write(self.style.SUCCESS('✓ Teams created'))
        
        # Create Users - Marvel Heroes
        self.stdout.write('Creating Marvel heroes...')
        marvel_users = [
            User.objects.create(
                email='ironman@marvel.com',
                username='Iron Man',
                password='iamironman',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                email='captainamerica@marvel.com',
                username='Captain America',
                password='avengersassemble',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                email='thor@marvel.com',
                username='Thor',
                password='worthyofmjolnir',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                email='blackwidow@marvel.com',
                username='Black Widow',
                password='redledger',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                email='hulk@marvel.com',
                username='Hulk',
                password='hulksmash',
                team_id=str(team_marvel._id)
            ),
        ]
        
        self.stdout.write(self.style.SUCCESS('✓ Marvel heroes created'))
        
        # Create Users - DC Heroes
        self.stdout.write('Creating DC heroes...')
        dc_users = [
            User.objects.create(
                email='superman@dc.com',
                username='Superman',
                password='krypton',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                email='batman@dc.com',
                username='Batman',
                password='darkknight',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                email='wonderwoman@dc.com',
                username='Wonder Woman',
                password='amazonian',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                email='flash@dc.com',
                username='The Flash',
                password='speedforce',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                email='aquaman@dc.com',
                username='Aquaman',
                password='atlantis',
                team_id=str(team_dc._id)
            ),
        ]
        
        self.stdout.write(self.style.SUCCESS('✓ DC heroes created'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        all_users = marvel_users + dc_users
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'Martial Arts']
        
        activities_data = []
        for user in all_users:
            # Create 5-10 random activities for each user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                calories = duration * random.randint(5, 10)
                distance = round(random.uniform(2, 25), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                
                activity = Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    calories_burned=calories,
                    distance=distance,
                    date=timezone.now() - timedelta(days=random.randint(0, 30)),
                    notes=f'{user.username} completed {activity_type.lower()} session'
                )
                activities_data.append({
                    'user_id': str(user._id),
                    'username': user.username,
                    'team_id': user.team_id,
                    'duration': duration,
                    'calories': calories,
                    'distance': distance or 0
                })
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(activities_data)} activities'))
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        user_stats = {}
        
        # Build user and team lookup
        user_lookup = {}
        team_lookup = {
            str(team_marvel._id): team_marvel,
            str(team_dc._id): team_dc
        }
        
        for user in all_users:
            user_lookup[str(user._id)] = user
        
        for activity in activities_data:
            user_id = activity['user_id']
            if user_id not in user_stats:
                user_stats[user_id] = {
                    'username': activity['username'],
                    'team_id': activity['team_id'],
                    'total_activities': 0,
                    'total_calories': 0,
                    'total_distance': 0.0,
                    'total_duration': 0
                }
            
            user_stats[user_id]['total_activities'] += 1
            user_stats[user_id]['total_calories'] += activity['calories']
            user_stats[user_id]['total_distance'] += activity['distance']
            user_stats[user_id]['total_duration'] += activity['duration']
        
        # Sort by total calories and assign ranks
        sorted_users = sorted(user_stats.items(), key=lambda x: x[1]['total_calories'], reverse=True)
        
        for rank, (user_id, stats) in enumerate(sorted_users, start=1):
            user = user_lookup[user_id]
            team = team_lookup[user.team_id]
            
            Leaderboard.objects.create(
                user_id=user_id,
                username=stats['username'],
                team_id=stats['team_id'],
                team_name=team.name,
                total_activities=stats['total_activities'],
                total_calories=stats['total_calories'],
                total_distance=round(stats['total_distance'], 2),
                total_duration=stats['total_duration'],
                rank=rank
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(user_stats)} leaderboard entries'))
        
        # Create Workouts
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            {
                'name': 'Super Soldier Training',
                'description': 'Captain America\'s signature workout routine for peak human conditioning',
                'activity_type': 'Weightlifting',
                'difficulty': 'Advanced',
                'duration': 60,
                'calories_estimate': 500,
                'equipment': ['Barbell', 'Dumbbells', 'Pull-up bar'],
                'instructions': [
                    'Warm-up: 10 minutes of dynamic stretching',
                    'Bench press: 4 sets of 8 reps',
                    'Pull-ups: 4 sets to failure',
                    'Squats: 4 sets of 10 reps',
                    'Military press: 3 sets of 8 reps',
                    'Cool-down: 5 minutes stretching'
                ]
            },
            {
                'name': 'Speed Force Circuit',
                'description': 'The Flash\'s high-intensity interval training for maximum speed',
                'activity_type': 'Running',
                'difficulty': 'Expert',
                'duration': 45,
                'calories_estimate': 600,
                'equipment': ['Running track', 'Timer'],
                'instructions': [
                    'Warm-up: 5 minutes light jog',
                    'Sprint 400m at 90% max speed',
                    'Rest 2 minutes',
                    'Repeat 8 times',
                    'Cool-down: 5 minutes walk'
                ]
            },
            {
                'name': 'Asgardian Power Lift',
                'description': 'Thor\'s legendary strength training routine',
                'activity_type': 'Weightlifting',
                'difficulty': 'Expert',
                'duration': 75,
                'calories_estimate': 550,
                'equipment': ['Barbell', 'Heavy weights', 'Lifting platform'],
                'instructions': [
                    'Warm-up: 10 minutes mobility work',
                    'Deadlifts: 5 sets of 5 reps',
                    'Overhead press: 5 sets of 5 reps',
                    'Power cleans: 4 sets of 3 reps',
                    'Farmer\'s walk: 3 sets',
                    'Cool-down: 10 minutes stretching'
                ]
            },
            {
                'name': 'Warrior Princess Routine',
                'description': 'Wonder Woman\'s balanced strength and agility training',
                'activity_type': 'Martial Arts',
                'difficulty': 'Advanced',
                'duration': 60,
                'calories_estimate': 480,
                'equipment': ['Mat', 'Resistance bands', 'Medicine ball'],
                'instructions': [
                    'Warm-up: 10 minutes shadowboxing',
                    'Bodyweight circuits: 3 rounds',
                    'Kick combinations: 15 minutes',
                    'Core work: 20 minutes',
                    'Flexibility training: 15 minutes'
                ]
            },
            {
                'name': 'Dark Knight Training',
                'description': 'Batman\'s tactical combat conditioning program',
                'activity_type': 'Martial Arts',
                'difficulty': 'Advanced',
                'duration': 90,
                'calories_estimate': 650,
                'equipment': ['Heavy bag', 'Training pads', 'Obstacle course'],
                'instructions': [
                    'Warm-up: 10 minutes rope jumping',
                    'Heavy bag work: 20 minutes',
                    'Pad work: 20 minutes',
                    'Grappling drills: 20 minutes',
                    'Obstacle course: 15 minutes',
                    'Cool-down: 5 minutes meditation'
                ]
            },
            {
                'name': 'Atlantean Swim Training',
                'description': 'Aquaman\'s underwater endurance and strength program',
                'activity_type': 'Swimming',
                'difficulty': 'Intermediate',
                'duration': 60,
                'calories_estimate': 500,
                'equipment': ['Swimming pool', 'Fins', 'Kickboard'],
                'instructions': [
                    'Warm-up: 400m easy swim',
                    'Main set: 10x100m intervals',
                    'Kick set: 300m with board',
                    'Sprint: 8x50m max effort',
                    'Cool-down: 200m easy swim'
                ]
            },
            {
                'name': 'Widow\'s Flexibility Flow',
                'description': 'Black Widow\'s yoga and flexibility routine for agility',
                'activity_type': 'Yoga',
                'difficulty': 'Intermediate',
                'duration': 45,
                'calories_estimate': 200,
                'equipment': ['Yoga mat', 'Blocks', 'Strap'],
                'instructions': [
                    'Sun salutations: 5 rounds',
                    'Warrior sequences: 15 minutes',
                    'Balance poses: 10 minutes',
                    'Hip openers: 10 minutes',
                    'Savasana: 5 minutes'
                ]
            },
            {
                'name': 'Hulk Smash Strength',
                'description': 'Raw power training inspired by the strongest Avenger',
                'activity_type': 'Weightlifting',
                'difficulty': 'Expert',
                'duration': 60,
                'calories_estimate': 520,
                'equipment': ['Heavy weights', 'Chains', 'Sledgehammer', 'Tire'],
                'instructions': [
                    'Warm-up: 10 minutes dynamic stretching',
                    'Heavy squats: 5 sets of 3 reps',
                    'Tire flips: 5 sets of 5 reps',
                    'Sledgehammer strikes: 10 minutes',
                    'Grip work: 15 minutes',
                    'Cool-down stretching'
                ]
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(workouts)} workout suggestions'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Database populated successfully!'))
        self.stdout.write(f'Teams: {Team.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Activities: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts: {Workout.objects.count()}')

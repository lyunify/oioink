"""
Management command: Create default achievements
Usage: python manage.py create_default_achievements
"""
from django.core.management.base import BaseCommand
from achievements.models import Achievement


class Command(BaseCommand):
    help = 'Create default achievements for the system'

    def handle(self, *args, **options):
        achievements_data = [
            {
                'name': 'First Wallet',
                'description': 'Create your first wallet',
                'icon': '💼',
                'color': '#667eea',
                'achievement_type': 'wallet_created',
                'coin_reward': 10,
                'requirements': {'wallet_count': 1},
                'order': 1,
            },
            {
                'name': 'Wallet Master',
                'description': 'Create 5 wallets',
                'icon': '🎯',
                'color': '#764ba2',
                'achievement_type': 'wallet_created',
                'coin_reward': 50,
                'requirements': {'wallet_count': 5},
                'order': 2,
            },
            {
                'name': 'First Saving Goal',
                'description': 'Complete your first saving goal',
                'icon': '🎯',
                'color': '#28a745',
                'achievement_type': 'saving_goal_reached',
                'coin_reward': 25,
                'requirements': {},
                'order': 3,
            },
            {
                'name': 'Saving Champion',
                'description': 'Complete 5 saving goals',
                'icon': '🏆',
                'color': '#ffc107',
                'achievement_type': 'saving_goal_reached',
                'coin_reward': 100,
                'requirements': {},
                'order': 4,
            },
            {
                'name': 'Spending Tracker',
                'description': 'Track your first spending',
                'icon': '💰',
                'color': '#dc3545',
                'achievement_type': 'spending_tracked',
                'coin_reward': 15,
                'requirements': {'spending_count': 1},
                'order': 5,
            },
            {
                'name': 'Budget Master',
                'description': 'Track 20 spending records',
                'icon': '📊',
                'color': '#17a2b8',
                'achievement_type': 'spending_tracked',
                'coin_reward': 75,
                'requirements': {'spending_count': 20},
                'order': 6,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for achievement_data in achievements_data:
            achievement, created = Achievement.objects.update_or_create(
                name=achievement_data['name'],
                defaults=achievement_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created achievement: {achievement.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated achievement: {achievement.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} and updated {updated_count} achievements!'
            )
        )





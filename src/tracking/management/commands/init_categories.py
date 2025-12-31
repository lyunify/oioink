"""
Django management command to initialize default spending categories
"""
from django.core.management.base import BaseCommand
from tracking.models import SpendingCategory


class Command(BaseCommand):
    help = 'Creates default spending categories for tracking app'

    def handle(self, *args, **options):
        # Define default categories
        categories_data = [
            {
                'name': 'Clothing',
                'icon': '👕',
                'color': '#FF6B6B',
                'description': 'Clothes, shoes, accessories, etc.'
            },
            {
                'name': 'Video',
                'icon': '🎬',
                'color': '#4ECDC4',
                'description': 'Movies, video subscriptions, entertainment, etc.'
            },
            {
                'name': 'Electronics',
                'icon': '📱',
                'color': '#45B7D1',
                'description': 'Phones, tablets, computers, game consoles, etc.'
            },
            {
                'name': 'School Supplies',
                'icon': '📚',
                'color': '#96CEB4',
                'description': 'Books, stationery, learning tools, etc.'
            },
            {
                'name': 'Games',
                'icon': '🎮',
                'color': '#FFEAA7',
                'description': 'Games, toys, entertainment items, etc.'
            },
            {
                'name': 'Food',
                'icon': '🍔',
                'color': '#DDA15E',
                'description': 'Snacks, drinks, dining out, etc.'
            },
            {
                'name': 'Transportation',
                'icon': '🚗',
                'color': '#6C5CE7',
                'description': 'Transportation fees, travel, etc.'
            },
            {
                'name': 'Sports',
                'icon': '⚽',
                'color': '#00B894',
                'description': 'Sports equipment, sports classes, etc.'
            },
            {
                'name': 'Gifts',
                'icon': '🎁',
                'color': '#E17055',
                'description': 'Birthday gifts, holiday gifts, etc.'
            },
            {
                'name': 'Other',
                'icon': '📦',
                'color': '#95A5A6',
                'description': 'Other expenses, can customize category name'
            },
        ]

        created_count = 0
        updated_count = 0

        for cat_data in categories_data:
            category, created = SpendingCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {cat_data["icon"]} {cat_data["name"]}'))
            else:
                # If already exists, update info (but don't overwrite user-modified content)
                updated = False
                if category.icon != cat_data['icon']:
                    category.icon = cat_data['icon']
                    updated = True
                if category.color != cat_data['color']:
                    category.color = cat_data['color']
                    updated = True
                if category.description != cat_data['description']:
                    category.description = cat_data['description']
                    updated = True
                
                if updated:
                    category.save()
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f'↻ Updated category: {cat_data["icon"]} {cat_data["name"]}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'✓ Category already exists: {cat_data["icon"]} {cat_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Categories initialization completed!'))
        self.stdout.write(self.style.SUCCESS(f'  Created: {created_count}'))
        if updated_count > 0:
            self.stdout.write(self.style.WARNING(f'  Updated: {updated_count}'))


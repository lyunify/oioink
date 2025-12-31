# Generated manually to initialize default spending categories

from django.db import migrations


def create_default_categories(apps, schema_editor):
    """创建默认支出类别"""
    SpendingCategory = apps.get_model('tracking', 'SpendingCategory')
    
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
    
    for cat_data in categories_data:
        SpendingCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )


def remove_default_categories(apps, schema_editor):
    """移除默认类别（回滚时使用）"""
    SpendingCategory = apps.get_model('tracking', 'SpendingCategory')
    
    default_names = ['Clothing', 'Video', 'Electronics', 'School Supplies', 'Games', 'Food', 'Transportation', 'Sports', 'Gifts', 'Other']
    SpendingCategory.objects.filter(name__in=default_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_categories, remove_default_categories),
    ]


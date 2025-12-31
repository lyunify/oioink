"""
Django management command to create Lesson 1: How to Save Money
"""
from django.core.management.base import BaseCommand
from lessons.models import Lesson, LessonSection, LessonTip


class Command(BaseCommand):
    help = 'Creates Lesson 1: How to Save Money for kids'

    def handle(self, *args, **options):
        # Check if Lesson 1 already exists
        lesson, created = Lesson.objects.get_or_create(
            lesson_number=1,
            defaults={
                'title': 'The Magic of Saving Money',
                'slug': 'how-to-save-money',
                'subtitle': 'Learn how to save money and reach your goals!',
                'description': 'A fun and interactive lesson teaching kids the importance of saving money, how to create a savings plan, and practical saving tips.',
                'icon': 'piggy-bank',
                'age_range': '6-12',
                'duration_minutes': 15,
                'status': 'published',
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created Lesson 1: {lesson.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Lesson 1 already exists. Updating content...'))
            lesson.title = 'The Magic of Saving Money'
            lesson.slug = 'how-to-save-money'
            lesson.subtitle = 'Learn how to save money and reach your goals!'
            lesson.description = 'A fun and interactive lesson teaching kids the importance of saving money, how to create a savings plan, and practical saving tips.'
            lesson.icon = 'piggy-bank'
            lesson.age_range = '6-12'
            lesson.duration_minutes = 15
            lesson.status = 'published'
            lesson.save()
            # Delete existing sections and tips to recreate them
            lesson.sections.all().delete()
            lesson.tips.all().delete()
            self.stdout.write(self.style.SUCCESS(f'✓ Updated Lesson 1: {lesson.title}'))

        # Create sections
        sections_data = [
            {
                'title': 'What is Saving?',
                'section_type': 'content',
                'order': 1,
                'icon': 'bank',
                'content': '''## Saving is keeping your money safe for later!

Imagine you have a magic box (a piggy bank). Every time you put your allowance or money into it, it keeps it safe for you to use later.

### Why should we save money?

1. 🎁 **To buy things you want**
   Like a new toy, game, or a fun book you've been wanting!

2. 🚨 **For emergencies**
   If your bike breaks and needs fixing, you'll have money to fix it!

3. 🎯 **To reach big dreams**
   Want a new bicycle? Or a trip to the amusement park? Saving helps you make your dreams come true!

Remember: Every coin counts! Even small amounts add up over time.'''
            },
            {
                'title': 'How to Start Saving: 3 Simple Steps',
                'section_type': 'content',
                'order': 2,
                'icon': 'rocket-takeoff',
                'content': '''### Step 1: Set a Goal 🎯

Think about what you want to save for:
- A new toy?
- Your favorite book?
- Or maybe a trip to the amusement park?

Write down your goal and put it somewhere you can see it often!

### Step 2: Make a Plan 📅

Decide how much money you'll save each week.
- If you get $10 allowance per week, try saving $5
- If you get birthday money, save half of it

### Step 3: Start Saving! ▶️

Find a fun piggy bank or jar and start putting your money in it!
Every time you add money, you're getting closer to your goal!'''
            },
            {
                'title': 'Smart Saving Tips',
                'section_type': 'content',
                'order': 3,
                'icon': 'lightbulb',
                'content': '''### Tip 1: Separate Your Money 📦

Think about two types of things:
- **Things you NEED**: Essential food, clothes
- **Things you WANT**: Fun toys, treats

Always take care of your needs first, then spend on wants!

### Tip 2: The Save-Half Rule 💰

Here's a simple rule:
- 💰 50% - Save it!
- 🍎 30% - Spend on things you need
- 🎮 20% - Spend on things you want

### Tip 3: Wait 24 Hours ⏰

Thinking about buying something new? Wait 24 hours first!

This helps you:
- Think if you really need it
- Avoid buying things on impulse
- Save money for things you really want'''
            },
            {
                'title': 'Activity: Set Your Saving Goal',
                'section_type': 'activity',
                'order': 4,
                'icon': 'journal-plus',
                'content': '''## Your Turn!

### Activity: My Savings Plan

1. Write down what you want to buy (your goal)
2. Write down how much it costs
3. Write down how much you can save each week
4. Calculate: How many weeks until you reach your goal?

**Example:**
- Goal: Buy a toy 🎁
- Cost: $50
- Saving per week: $5
- Time needed: 10 weeks (about 2.5 months)

You can do it! 💪

Try making your own savings plan now!'''
            },
            {
                'title': "Emma's Saving Story",
                'section_type': 'story',
                'order': 5,
                'icon': 'star-fill',
                'content': '''## How Emma Saved for Her Bicycle

Emma was 8 years old, and she wanted a new bicycle that cost $100.

She made a savings plan:
- Save $10 from her weekly allowance
- Save all $50 from her birthday money
- Save extra money from helping with chores

After 5 weeks, Emma saved $100!

When she got her new bike, she felt so proud because she achieved her goal through saving!

**You can be like Emma too!** 🎉

What's your savings goal? Write it down and start saving today!'''
            }
        ]

        for section_data in sections_data:
            section, created = LessonSection.objects.get_or_create(
                lesson=lesson,
                title=section_data['title'],
                defaults=section_data
            )
            if not created:
                for key, value in section_data.items():
                    setattr(section, key, value)
                section.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created/Updated section: {section.title}'))

        # Create tips
        tips_data = [
            {
                'title': 'Write down your goal',
                'icon': 'pencil',
                'order': 1,
                'content': 'Write your savings goal on paper and put it where you can see it often. This helps you remember and stay focused!'
            },
            {
                'title': 'Use a clear jar or piggy bank',
                'icon': 'safe2',
                'order': 2,
                'content': 'Use a transparent piggy bank so you can see your money grow. This gives you a great sense of achievement!'
            },
            {
                'title': 'Celebrate small milestones',
                'icon': 'trophy',
                'order': 3,
                'content': 'When you reach 25%, 50%, or 75% of your goal, give yourself a small reward, like watching your favorite movie!'
            }
        ]

        for tip_data in tips_data:
            tip, created = LessonTip.objects.get_or_create(
                lesson=lesson,
                title=tip_data['title'],
                defaults=tip_data
            )
            if not created:
                for key, value in tip_data.items():
                    setattr(tip, key, value)
                tip.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created/Updated tip: {tip.title}'))

        self.stdout.write(self.style.SUCCESS('\n✓ Lesson 1 created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Visit: http://127.0.0.1:8000/lessons/{lesson.slug}/'))


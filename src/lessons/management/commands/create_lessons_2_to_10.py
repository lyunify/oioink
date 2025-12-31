"""
Django management command to create Lessons 2-10: Financial Savvy for Kids
Based on the 10 lessons PDF content
"""
from django.core.management.base import BaseCommand
from lessons.models import Lesson, LessonSection, LessonTip


class Command(BaseCommand):
    help = 'Creates Lessons 2-10: Financial Savvy for Kids'

    def handle(self, *args, **options):
        lessons_data = [
            {
                'lesson_number': 2,
                'title': 'Earning Money',
                'slug': 'earning-money',
                'subtitle': 'Learn how money is earned through effort and work!',
                'description': 'A fun lesson teaching kids that money is earned through doing jobs or chores, and how hard work leads to rewards.',
                'icon': 'briefcase',
                'age_range': '5-7',
                'duration_minutes': 20,
                'status': 'published',
                'sections': [
                    {
                        'title': 'What is Earning?',
                        'section_type': 'content',
                        'order': 1,
                        'icon': 'briefcase-fill',
                        'content': '''## Earning means getting money for doing work!

When you do a job or help with chores, you can earn money as a reward for your effort.

### How do people earn money?

1. **Parents work at jobs** 👨‍💼
   - They go to work every day
   - They do their job well
   - They get paid money for their work

2. **Kids can earn money too!** 👧👦
   - By doing chores at home
   - By helping neighbors
   - By completing tasks

3. **Allowance is practice** 💰
   - Some kids get allowance for doing chores
   - This helps you learn about earning money
   - It's like practice for when you grow up!

Remember: Money doesn't just appear - it comes from working hard!'''
                    },
                    {
                        'title': 'Ways to Earn Money',
                        'section_type': 'content',
                        'order': 2,
                        'icon': 'bullseye',
                        'content': '''### Chore Chart System 📋

Create a simple chart with tasks:
- Making your bed = 25 cents
- Picking up toys = 25 cents
- Setting the table = 25 cents
- Taking out trash = 50 cents

Each completed chore earns you money!

### Job Jar System 🏺

Write easy jobs on slips of paper:
- "Water the plants"
- "Feed the pet"
- "Help with laundry"
- "Organize books"

Pick one job and complete it to earn play money or real money!

### Why Earning Feels Good ✨

When you earn your own money:
- You feel proud and independent
- You learn the value of hard work
- You understand that money comes from effort

Try it yourself - complete a chore and see how good it feels!'''
                    },
                    {
                        'title': 'Activity: Create Your Chore Chart',
                        'section_type': 'activity',
                        'order': 3,
                        'icon': 'clipboard-check',
                        'content': '''## Your Turn!

### Activity: My Chore Chart

1. **List 5 chores** you can do at home
2. **Assign a reward** for each chore (like 25 cents or 50 cents)
3. **Create a chart** with checkboxes
4. **Track your earnings** in a notebook

**Example:**
- ✅ Make bed - 25 cents
- ✅ Pick up toys - 25 cents
- ✅ Set table - 25 cents
- ✅ Take out trash - 50 cents
- ✅ Water plants - 25 cents

**Total earned this week: $1.50!**

Start your chore chart today and watch your earnings grow! 💪'''
                    },
                    {
                        'title': 'Discussion: Family Jobs',
                        'section_type': 'content',
                        'order': 4,
                        'icon': 'chat-dots',
                        'content': '''## Talk About It!

### Discussion Questions:

1. **What jobs do family members do to earn money?**
   - Ask your parents about their jobs
   - Learn what they do at work
   - Understand how they earn money for the family

2. **How does it feel to earn your own money?**
   - Do you feel proud?
   - Do you want to save it or spend it?
   - What would you like to buy with your earnings?

3. **What chores can you do to help?**
   - Think about ways you can help at home
   - Remember: every little bit helps!

### Homework 📝

Complete one chore this week and track your earnings in a notebook. Write down:
- What chore you did
- How much you earned
- How it made you feel

You're learning to be responsible and earn your own money! 🎉'''
                    }
                ],
                'tips': [
                    {
                        'title': 'Start with small chores',
                        'icon': 'target',
                        'order': 1,
                        'content': 'Begin with easy tasks like making your bed or picking up toys. Small steps lead to big achievements!'
                    },
                    {
                        'title': 'Track your earnings',
                        'icon': 'journal-text',
                        'order': 2,
                        'content': 'Keep a notebook to write down each chore you complete and how much you earned. This helps you see your progress!'
                    },
                    {
                        'title': 'Be consistent',
                        'icon': 'clock',
                        'order': 3,
                        'content': 'Do your chores regularly. Consistency helps you earn more and builds good habits for the future!'
                    }
                ]
            },
            {
                'lesson_number': 3,
                'title': 'Saving Money Basics',
                'slug': 'saving-money-basics',
                'subtitle': 'Learn why and how to save money for the future!',
                'description': 'An engaging lesson explaining why saving is important, how to use a piggy bank, and how saving helps buy bigger things in the future.',
                'icon': 'safe-fill',
                'age_range': '5-7',
                'duration_minutes': 20,
                'status': 'published',
                'sections': [
                    {
                        'title': 'What is Saving?',
                        'section_type': 'content',
                        'order': 1,
                        'icon': 'bank',
                        'content': '''## Saving means keeping money for later!

Instead of spending all your money right away, you put some aside to use later.

### Why do we save?

1. **To buy bigger things** 🎁
   - A new toy that costs more
   - A special book you want
   - Something you really want but can't afford yet

2. **For emergencies** 🚨
   - If something breaks and needs fixing
   - If you need something important
   - To be prepared for surprises

3. **To reach your dreams** ✨
   - Save for something special
   - Make your goals come true
   - Feel proud of your achievement

Remember: Saving is like planting a seed - it grows over time!'''
                    },
                    {
                        'title': 'How to Save: Piggy Bank',
                        'section_type': 'content',
                        'order': 2,
                        'icon': 'safe2',
                        'content': '''### Make Your Own Piggy Bank! 🐷

**Materials needed:**
- A clear jar or container
- Decorations (stickers, markers, paint)
- Your allowance or money

**Steps:**
1. Decorate your jar to make it special
2. Label it "My Savings"
3. Start adding coins and bills
4. Watch your money grow!

### Why Use a Clear Jar? 👀

When you can see your money:
- You feel excited watching it grow
- You're motivated to save more
- You can see your progress

Every coin you add brings you closer to your goal!'''
                    },
                    {
                        'title': 'Setting a Savings Goal',
                        'section_type': 'content',
                        'order': 3,
                        'icon': 'target',
                        'content': '''### Pick a Goal! 🎯

Think about what you want to save for:
- A toy that costs $10
- A book you really want
- A special treat

### Track Your Progress 📊

Use stickers or draw a chart:
- Each time you save money, add a sticker
- Watch your progress grow
- Celebrate when you reach your goal!

### The Save Rule 💰

Try this simple rule:
- When you get money, save **1 out of every 5 coins**
- Or save **half** of your allowance
- The rest you can spend

This way, you're always saving something!'''
                    },
                    {
                        'title': 'Activity: Decorate Your Piggy Bank',
                        'section_type': 'activity',
                        'order': 4,
                        'icon': 'palette',
                        'content': '''## Your Turn!

### Activity: Create Your Savings Jar

1. **Find a clear jar** or container
2. **Decorate it** with your favorite colors and stickers
3. **Write your goal** on a piece of paper and tape it to the jar
4. **Add your first coin** to start saving!

**Example Goal:**
"I want to save $5 for a new toy!"

**Your Savings Plan:**
- Save 1 coin from every 5 you get
- Add it to your jar every day
- Watch it grow!

Start saving today and make your dreams come true! 💪'''
                    },
                    {
                        'title': 'Story: Saving for Something Special',
                        'section_type': 'story',
                        'order': 5,
                        'icon': 'star-fill',
                        'content': '''## A Saving Story

Once upon a time, there was a kid who wanted a special toy that cost $10.

Every week, they saved $2 from their allowance:
- Week 1: Saved $2 (Total: $2)
- Week 2: Saved $2 (Total: $4)
- Week 3: Saved $2 (Total: $6)
- Week 4: Saved $2 (Total: $8)
- Week 5: Saved $2 (Total: $10) ✅

After 5 weeks, they had enough money to buy the toy!

They felt so proud because they saved their own money to buy it.

**You can do this too!** 🎉

What do you want to save for? Start your savings jar today!'''
                    }
                ],
                'tips': [
                    {
                        'title': 'Save regularly',
                        'icon': 'clock-history',
                        'order': 1,
                        'content': 'Make saving a habit. Add money to your piggy bank every time you receive money, even if it\'s just a little bit!'
                    },
                    {
                        'title': 'Use a clear container',
                        'icon': 'eye',
                        'order': 2,
                        'content': 'A clear jar or piggy bank lets you see your money grow, which makes saving more fun and motivating!'
                    },
                    {
                        'title': 'Set a clear goal',
                        'icon': 'flag',
                        'order': 3,
                        'content': 'Write down what you\'re saving for and put it where you can see it. This helps you stay focused on your goal!'
                    }
                ]
            },
            {
                'lesson_number': 4,
                'title': 'Needs vs. Wants',
                'slug': 'needs-vs-wants',
                'subtitle': 'Learn the difference between things you need and things you want!',
                'description': 'An important lesson teaching kids to differentiate between essential needs and optional wants, and how to prioritize spending wisely.',
                'icon': 'target',
                'age_range': '8-10',
                'duration_minutes': 25,
                'status': 'published',
                'sections': [
                    {
                        'title': 'What are Needs?',
                        'section_type': 'content',
                        'order': 1,
                        'icon': 'house',
                        'content': '''## Needs are things we MUST have to live!

These are essential things that keep us healthy, safe, and happy.

### Examples of Needs:

1. **Food** 🍎
   - Healthy meals
   - Water to drink
   - Things that keep us strong

2. **Clothing** 👕
   - Clothes to wear
   - Shoes for our feet
   - Warm clothes in winter

3. **Shelter** 🏠
   - A place to live
   - A safe home
   - A bed to sleep in

4. **Healthcare** 🏥
   - Medicine when sick
   - Doctor visits
   - Things that keep us healthy

Remember: Needs come first! Always take care of your needs before spending on wants.'''
                    },
                    {
                        'title': 'What are Wants?',
                        'section_type': 'content',
                        'order': 2,
                        'icon': 'controller',
                        'content': '''## Wants are fun things we LIKE but can live without!

These are things that make us happy but aren't necessary for survival.

### Examples of Wants:

1. **Toys and Games** 🎮
   - Video games
   - Action figures
   - Board games

2. **Treats** 🍭
   - Candy
   - Ice cream
   - Special snacks

3. **Entertainment** 🎬
   - Movies
   - Theme park visits
   - Fun activities

4. **Fancy Things** ✨
   - Designer clothes
   - Latest gadgets
   - Expensive toys

Remember: Wants are nice to have, but we can be happy without them!'''
                    },
                    {
                        'title': 'Smart Spending: Needs First!',
                        'section_type': 'content',
                        'order': 3,
                        'icon': 'lightbulb',
                        'content': '''### The Golden Rule: Needs Before Wants! 💰

When you have money, always:
1. **First**: Buy things you NEED
2. **Then**: Buy things you WANT (if you have money left)

### Why is this important?

- **Staying healthy**: Needs keep you safe and healthy
- **Avoiding problems**: If you only buy wants, you might not have money for needs
- **Being responsible**: Smart kids know the difference!

### Example Shopping List:

**Needs (Buy First):**
- ✅ Milk
- ✅ Bread
- ✅ Fruits
- ✅ Vegetables

**Wants (Buy if Money Left):**
- 🎮 Video game
- 🍭 Candy
- 🎁 Toys

Always shop smart!'''
                    },
                    {
                        'title': 'Activity: Needs vs. Wants Sorting Game',
                        'section_type': 'activity',
                        'order': 4,
                        'icon': 'shuffle',
                        'content': '''## Your Turn!

### Activity: Sort the Items

**Instructions:**
1. Look at each item below
2. Decide if it's a NEED or a WANT
3. Sort them into two groups

**Items to Sort:**
- 🍎 Apple
- 🎮 Video game
- 👕 T-shirt
- 🍭 Candy
- 🏠 House
- 🎬 Movie ticket
- 🥛 Milk
- 🚲 Bicycle
- 🏥 Medicine
- 🎁 Toy

**Think about it:**
- Which items do you NEED to live?
- Which items are fun but not necessary?

**Challenge:**
Pretend you have $20. Make a shopping list with needs first, then see what's left for wants!

Practice makes perfect! 💪'''
                    },
                    {
                        'title': 'What if You Want Something?',
                        'section_type': 'content',
                        'order': 5,
                        'icon': 'question-circle',
                        'content': '''## What if you want something but can't afford it?

### The Solution: Save Up! 💰

If you want something that's a WANT (not a need):
1. **Don't worry!** It's okay to want things
2. **Save your money** from allowance or chores
3. **Wait until you have enough** to buy it
4. **Then enjoy it!** You earned it!

### Example:

You want a video game that costs $50:
- You get $10 allowance per week
- Save $5 each week
- After 10 weeks, you'll have $50!
- Then you can buy your game! 🎮

### Remember:

- ✅ Needs = Buy now if you need them
- 💰 Wants = Save up and buy later
- 🎯 Always prioritize needs first!

This is how smart kids manage their money!'''
                    }
                ],
                'tips': [
                    {
                        'title': 'Ask yourself: Do I need it?',
                        'icon': 'question-circle-fill',
                        'order': 1,
                        'content': 'Before buying something, ask: "Is this a need or a want?" This helps you make smart spending decisions!'
                    },
                    {
                        'title': 'Needs come first',
                        'icon': '1-circle',
                        'order': 2,
                        'content': 'Always make sure you have money for needs before spending on wants. This keeps you healthy and safe!'
                    },
                    {
                        'title': 'Save for wants',
                        'icon': 'cash-stack',
                        'order': 3,
                        'content': 'If you want something that\'s not a need, save up for it! This teaches patience and makes the purchase more special!'
                    }
                ]
            },
            {
                'lesson_number': 5,
                'title': 'Simple Budgeting',
                'slug': 'simple-budgeting',
                'subtitle': 'Learn how to plan and track your money!',
                'description': 'An interactive lesson introducing budgeting concepts, teaching kids to divide money into Save, Spend, and Give categories.',
                'icon': 'graph-up',
                'age_range': '8-10',
                'duration_minutes': 25,
                'status': 'published',
                'sections': [
                    {
                        'title': 'What is a Budget?',
                        'section_type': 'content',
                        'order': 1,
                        'icon': 'graph-up',
                        'content': '''## A budget is a plan for your money!

It helps you decide:
- How much to SAVE
- How much to SPEND
- How much to GIVE

### Why is budgeting important?

1. **Helps you reach goals** 🎯
   - You know where your money goes
   - You can plan for things you want
   - You won't run out of money

2. **Teaches responsibility** 💪
   - You learn to plan ahead
   - You make smart choices
   - You feel in control

3. **Prevents overspending** 🚫
   - You know your limits
   - You avoid running out of money
   - You stay organized

Remember: A budget is like a map for your money!'''
                    },
                    {
                        'title': 'The 50-30-20 Rule',
                        'section_type': 'content',
                        'order': 2,
                        'icon': 'cash-coin',
                        'content': '''### Divide Your Money into 3 Jars! 🏺

Here's a simple rule for budgeting:

**If you get $10 allowance:**

1. **SAVE: 50% = $5** 💰
   - Put this in your savings jar
   - Use it for big goals
   - Watch it grow!

2. **SPEND: 30% = $3** 🛒
   - Use this for things you need
   - Buy small treats
   - Have fun with it!

3. **GIVE: 20% = $2** ❤️
   - Donate to charity
   - Help others
   - Make the world better!

### Example Budget:

**Weekly Allowance: $10**
- 💰 Save: $5 (50%)
- 🛒 Spend: $3 (30%)
- ❤️ Give: $2 (20%)

Try this with your allowance!'''
                    },
                    {
                        'title': 'Budget Jar System',
                        'section_type': 'activity',
                        'order': 3,
                        'icon': 'bucket',
                        'content': '''## Your Turn!

### Activity: Create Your Budget Jars

**Materials:**
- 3 clear jars or containers
- Labels: "SAVE", "SPEND", "GIVE"
- Your allowance or money

**Steps:**
1. Label your three jars
2. When you get money, divide it:
   - 50% goes to SAVE jar
   - 30% goes to SPEND jar
   - 20% goes to GIVE jar
3. Track your money in each jar

**Example:**
If you get $10:
- 💰 SAVE jar: $5
- 🛒 SPEND jar: $3
- ❤️ GIVE jar: $2

**Track Your Budget:**

<table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
<thead>
<tr style="background-color: #eef2ff; border-bottom: 2px solid #6366f1;">
<th style="padding: 12px; text-align: left; border: 1px solid #c7d2fe;">Category</th>
<th style="padding: 12px; text-align: right; border: 1px solid #c7d2fe;">Amount In</th>
<th style="padding: 12px; text-align: right; border: 1px solid #c7d2fe;">Amount Out</th>
<th style="padding: 12px; text-align: right; border: 1px solid #c7d2fe;">Balance</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding: 10px; border: 1px solid #e5e7eb;"><strong>Save</strong></td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$5.00</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$0.00</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb; color: #22c55e; font-weight: bold;">$5.00</td>
</tr>
<tr style="background-color: #fafafa;">
<td style="padding: 10px; border: 1px solid #e5e7eb;"><strong>Spend</strong></td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$3.00</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$1.50</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb; color: #22c55e; font-weight: bold;">$1.50</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #e5e7eb;"><strong>Give</strong></td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$2.00</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$0.00</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb; color: #22c55e; font-weight: bold;">$2.00</td>
</tr>
</tbody>
</table>

Start your budget jars today! 💪'''
                    },
                    {
                        'title': 'Weekly Budget Sheet',
                        'section_type': 'content',
                        'order': 4,
                        'icon': 'journal-text',
                        'content': '''### Track Your Money! 📝

Create a simple table to log your money:

**Weekly Budget Sheet:**

<table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
<thead>
<tr style="background-color: #eef2ff; border-bottom: 2px solid #6366f1;">
<th style="padding: 12px; text-align: left; border: 1px solid #c7d2fe;">Category</th>
<th style="padding: 12px; text-align: right; border: 1px solid #c7d2fe;">Money In</th>
<th style="padding: 12px; text-align: right; border: 1px solid #c7d2fe;">Money Out</th>
<th style="padding: 12px; text-align: right; border: 1px solid #c7d2fe;">Balance</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding: 10px; border: 1px solid #e5e7eb;"><strong>Save</strong></td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$5.00</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$0.00</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb; color: #22c55e; font-weight: bold;">$5.00</td>
</tr>
<tr style="background-color: #fafafa;">
<td style="padding: 10px; border: 1px solid #e5e7eb;"><strong>Spend</strong></td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$3.00</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$2.00</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb; color: #22c55e; font-weight: bold;">$1.00</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #e5e7eb;"><strong>Give</strong></td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$2.00</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$0.00</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb; color: #22c55e; font-weight: bold;">$2.00</td>
</tr>
</tbody>
</table>

### How to Use It:

1. **Write down** money you receive
2. **Write down** money you spend
3. **Calculate** your balance
4. **Check** if you're staying on budget

### What if you overspend?

- ⚠️ Don't take money from other jars
- 💡 Wait until next week
- 🎯 Learn from your mistake
- ✅ Plan better next time

Remember: A budget helps you stay organized!'''
                    },
                    {
                        'title': 'Discussion: Budgeting Benefits',
                        'section_type': 'content',
                        'order': 5,
                        'icon': 'chat-quote',
                        'content': '''## Talk About It!

### Discussion Questions:

1. **What happens if you overspend in one category?**
   - You might run out of money
   - You can't take from other jars
   - You need to wait until next week

2. **How does budgeting help avoid running out of money?**
   - You plan ahead
   - You know your limits
   - You stay organized

3. **Why is it important to save 50%?**
   - You build savings for goals
   - You're prepared for emergencies
   - You learn good habits

### Homework 📝

Track one week's allowance using the jars or budget sheet:
- Write down all money in
- Write down all money out
- Calculate your balance
- See if you stayed on budget!

You're learning to be a money manager! 🎉'''
                    }
                ],
                'tips': [
                    {
                        'title': 'Use three separate jars',
                        'icon': 'bucket',
                        'order': 1,
                        'content': 'Having separate jars for Save, Spend, and Give helps you see exactly where your money goes and stay organized!'
                    },
                    {
                        'title': 'Track everything',
                        'icon': 'journal-text',
                        'order': 2,
                        'content': 'Write down every time you add or take money from your jars. This helps you understand your spending habits!'
                    },
                    {
                        'title': 'Stick to your budget',
                        'icon': 'target',
                        'order': 3,
                        'content': 'Once you divide your money, try not to take from one jar to use in another. This teaches discipline and planning!'
                    }
                ]
            },
            {
                'lesson_number': 6,
                'title': 'Giving and Sharing',
                'slug': 'giving-and-sharing',
                'subtitle': 'Learn the joy of helping others!',
                'description': 'A heartwarming lesson teaching kids the value of generosity, how giving helps others, and how to balance giving with saving and spending.',
                'icon': 'heart-fill',
                'age_range': '8-10',
                'duration_minutes': 25,
                'status': 'published',
                'sections': [
                    {
                        'title': 'What is Giving?',
                        'section_type': 'content',
                        'order': 1,
                        'icon': 'heart-fill',
                        'content': '''## Giving means sharing with others!

When you give money, time, or help to others, you make the world a better place.

### Why is giving important?

1. **Helps others in need** 🤝
   - People who need food
   - Animals who need care
   - Communities that need support

2. **Makes you feel good** 😊
   - Giving brings happiness
   - You feel proud and kind
   - It's rewarding!

3. **Builds a better world** 🌍
   - Small acts add up
   - Everyone can help
   - Together we make a difference

Remember: Giving is a superpower that everyone has!'''
                    },
                    {
                        'title': 'Ways to Give',
                        'section_type': 'content',
                        'order': 2,
                        'icon': 'gift',
                        'content': '''### How Can Kids Give?

1. **Donate Money** 💰
   - Use money from your "GIVE" jar
   - Donate to animal shelters
   - Support food banks
   - Help children in need

2. **Donate Time** ⏰
   - Help at a community center
   - Volunteer with family
   - Clean up your neighborhood
   - Visit elderly neighbors

3. **Donate Things** 📦
   - Give away toys you don't use
   - Donate clothes that don't fit
   - Share books with others
   - Help organize a donation drive

4. **Fundraising** 🍋
   - Have a bake sale
   - Run a lemonade stand
   - Organize a car wash
   - Donate the money you earn!

Every little bit helps!'''
                    },
                    {
                        'title': 'Charity Research Activity',
                        'section_type': 'activity',
                        'order': 3,
                        'icon': 'search',
                        'content': '''## Your Turn!

### Activity: Find a Cause to Support

**Steps:**
1. **Research** kid-friendly charities (with parent help):
   - Animal shelters 🐾
   - Food banks 🍎
   - Children's hospitals 🏥
   - Environmental groups 🌱

2. **Choose one** that interests you
3. **Learn about it** - what do they do?
4. **Decide** how you want to help

**Examples:**
- 🐾 **Animal Shelter**: Donate money for pet food
- 🍎 **Food Bank**: Donate money for meals
- 🏥 **Children's Hospital**: Donate toys or money
- 🌱 **Environmental Group**: Help plant trees

**Your Giving Plan:**
- Set aside money from your "GIVE" jar
- Decide how much to donate
- Make your donation!

Start making a difference today! 💪'''
                    },
                    {
                        'title': 'Bake Sale or Lemonade Stand',
                        'section_type': 'activity',
                        'order': 4,
                        'icon': 'cup-straw',
                        'content': '''### Fundraising Ideas! 🍋

**Bake Sale:**
- Bake cookies or cupcakes with family
- Sell them to neighbors
- Donate the money to charity

**Lemonade Stand:**
- Set up a stand in your neighborhood
- Sell lemonade
- Donate profits to a good cause

**How it works:**
1. **Earn money** from your sale
2. **Keep some** for yourself (like 50%)
3. **Donate some** to charity (like 50%)
4. **Feel proud** of helping others!

**Example:**
- You earn $20 from lemonade stand
- You keep $10 for yourself
- You donate $10 to animal shelter
- Everyone wins! 🎉

Try organizing a fundraiser with your family!'''
                    },
                    {
                        'title': 'Balancing Give, Save, and Spend',
                        'section_type': 'content',
                        'order': 5,
                        'icon': 'scale',
                        'content': '''### The 50-30-20 Rule ⚖️

Remember your budget:
- 💰 **50% Save** - For your goals
- 🛒 **30% Spend** - For your needs and wants
- ❤️ **20% Give** - To help others

### Why balance is important:

- ✅ **You help others** (Give)
- ✅ **You reach your goals** (Save)
- ✅ **You enjoy life** (Spend)

All three are important!

### Discussion Questions:

1. **How does giving make the world better?**
   - It helps people in need
   - It makes communities stronger
   - It spreads kindness

2. **Share a story about helping someone:**
   - When did you help someone?
   - How did it make you feel?
   - What did you learn?

### Homework 📝

Set aside money from your "GIVE" jar for a chosen cause:
- Choose a charity
- Decide how much to give
- Make your donation
- Feel proud of your kindness!

You're learning to be generous and kind! 🎉'''
                    }
                ],
                'tips': [
                    {
                        'title': 'Start small',
                        'icon': 'seedling',
                        'order': 1,
                        'content': 'You don\'t need to give a lot to make a difference. Even small donations help and teach you the value of giving!'
                    },
                    {
                        'title': 'Choose causes you care about',
                        'icon': 'heart-fill',
                        'order': 2,
                        'content': 'Pick charities or causes that matter to you. When you care about what you\'re supporting, giving feels more meaningful!'
                    },
                    {
                        'title': 'Give regularly',
                        'icon': 'clock',
                        'order': 3,
                        'content': 'Make giving a habit by setting aside money from your "GIVE" jar regularly. Consistency makes a bigger impact!'
                    }
                ]
            },
            {
                'lesson_number': 7,
                'title': 'Smart Spending and Avoiding Impulse Buys',
                'slug': 'smart-spending-avoiding-impulse',
                'subtitle': 'Learn to make thoughtful purchasing decisions!',
                'description': 'An important lesson teaching kids to compare prices, avoid impulse purchases, and make smart spending decisions.',
                'icon': 'cart',
                'age_range': '11-12',
                'duration_minutes': 30,
                'status': 'published',
                'sections': [
                    {
                        'title': 'What is Smart Spending?',
                        'section_type': 'content',
                        'order': 1,
                        'icon': 'lightbulb-fill',
                        'content': '''## Smart spending means thinking before you buy!

Before spending money, ask yourself:
- Do I **need** it?
- Can I **afford** it?
- Is there a **better option**?

### Why is smart spending important?

1. **Saves money** 💰
   - You get better deals
   - You avoid wasting money
   - You have more for important things

2. **Prevents regret** 😔
   - You think before buying
   - You make better choices
   - You feel satisfied with purchases

3. **Builds good habits** ✅
   - You learn to compare prices
   - You become a smart shopper
   - You manage money better

Remember: Smart spending is a superpower!'''
                    },
                    {
                        'title': 'What are Impulse Buys?',
                        'section_type': 'content',
                        'order': 2,
                        'icon': 'exclamation-triangle',
                        'content': '''## Impulse buys are quick decisions that lead to regret!

These are purchases you make without thinking:
- You see something and buy it immediately
- You don't compare prices
- You might regret it later

### Examples of impulse buys:

- 🍭 Buying candy at checkout
- 🎮 Grabbing a game you just saw
- 👕 Buying clothes on a whim
- 🎁 Getting something because it's "on sale"

### Why are they bad?

- 💸 You waste money
- 😔 You might regret it
- 🎯 You don't reach your goals
- 📉 You can't save as much

Remember: Impulse buys are like traps - avoid them!'''
                    },
                    {
                        'title': 'The 24-Hour Rule',
                        'section_type': 'content',
                        'order': 3,
                        'icon': 'clock',
                        'content': '''### Wait 24 Hours Before Buying! ⏰

**The Rule:**
If you want to buy something, wait 24 hours first!

**Why?**
- You have time to think
- You can compare prices
- You might realize you don't need it
- You avoid impulse buys

### How it works:

1. **See something you want** 👀
2. **Wait 24 hours** ⏰
3. **Think about it** 🤔
   - Do I really need it?
   - Can I afford it?
   - Is there a better option?
4. **Then decide** ✅

### Example:

You see a cool toy for $30:
- **Day 1**: You want it, but wait...
- **Day 2**: Do you still want it?
  - ✅ Yes → Save up and buy it
  - ❌ No → You saved $30!

Try the 24-hour rule - it works!'''
                    },
                    {
                        'title': 'Price Comparison Activity',
                        'section_type': 'activity',
                        'order': 4,
                        'icon': 'search',
                        'content': '''## Your Turn!

### Activity: Compare Prices

**Task:** Compare prices of the same item at different stores

**Example: Buying a Bike**

**Store A:**
- Bike: $150
- Includes: Bike only

**Store B:**
- Bike: $160
- Includes: Bike + helmet + lock

**Store C:**
- Bike: $140
- Includes: Bike only
- On sale: 10% off = $126

**Which is the best deal?**
- Store C: $126 (cheapest)
- Store B: $160 (includes extras)

**Think about:**
- Which store has the best price?
- What extras are included?
- Is it worth paying more for extras?

**Your Turn:**
Pick an item you want (with parent help):
1. Check prices at 3 different stores
2. Compare what's included
3. Find the best deal
4. Make a smart choice!

Practice makes you a smart shopper! 💪'''
                    },
                    {
                        'title': 'Understanding Advertising',
                        'section_type': 'content',
                        'order': 5,
                        'icon': 'tv',
                        'content': '''### What are ads trying to do? 📺

**Ads want to:**
- Make you want things
- Make you think you need them
- Make you buy right away
- Make you spend money

### How to be smart about ads:

1. **Question ads** ❓
   - Do I really need this?
   - Is this just trying to sell me something?
   - Will this make me happy long-term?

2. **Don't fall for tricks** 🎭
   - "Limited time offer" - usually not true
   - "Everyone has one" - not a good reason
   - "You'll be cool" - things don't make you cool

3. **Wait and think** 🤔
   - Use the 24-hour rule
   - Compare prices
   - Talk to parents

### Sales and Coupons 💰

**Good deals:**
- ✅ Things you actually need
- ✅ Things you planned to buy
- ✅ Real discounts (not fake sales)

**Bad deals:**
- ❌ Things you don't need
- ❌ Impulse purchases
- ❌ "Sales" that aren't really sales

Remember: Smart shoppers think before they buy!'''
                    },
                    {
                        'title': 'Homework: Track a Purchase',
                        'section_type': 'content',
                        'order': 6,
                        'icon': 'journal-text',
                        'content': '''## Your Assignment!

### Track a Potential Purchase

**Steps:**
1. **Pick something** you want to buy
2. **Research alternatives:**
   - Check different stores
   - Compare prices
   - Look for sales or coupons
3. **Wait 24 hours** before deciding
4. **Make your decision:**
   - Is it worth it?
   - Can you afford it?
   - Is it the best deal?

**Write down:**
- What you want to buy
- Prices at different stores
- What you learned
- Your final decision

**Example:**

**Item:** Video game
- Store A: $60
- Store B: $55 (on sale)
- Store C: $60 (includes bonus content)

**Decision:** Store B - best price!

**What I learned:** Comparing prices saved me $5!

Practice smart spending and become a money expert! 🎉'''
                    }
                ],
                'tips': [
                    {
                        'title': 'Always compare prices',
                        'icon': 'search',
                        'order': 1,
                        'content': 'Before buying, check prices at different stores. You might find the same item for less money elsewhere!'
                    },
                    {
                        'title': 'Use the 24-hour rule',
                        'icon': 'clock',
                        'order': 2,
                        'content': 'Wait a day before making a purchase. This helps you avoid impulse buys and make better decisions!'
                    },
                    {
                        'title': 'Question advertisements',
                        'icon': 'question-circle',
                        'order': 3,
                        'content': 'Ads try to make you want things. Always ask yourself: "Do I really need this, or is the ad just trying to sell me something?"'
                    }
                ]
            },
            {
                'lesson_number': 8,
                'title': 'Introduction to Banking and Interest',
                'slug': 'banking-and-interest',
                'subtitle': 'Learn how banks work and how money can grow!',
                'description': 'An educational lesson explaining how banks keep money safe, what interest is, and how savings accounts help money grow over time.',
                'icon': 'bank',
                'age_range': '11-12',
                'duration_minutes': 30,
                'status': 'published',
                'sections': [
                    {
                        'title': 'What is a Bank?',
                        'section_type': 'content',
                        'order': 1,
                        'icon': 'bank',
                        'content': '''## A bank is a safe place to keep your money!

Banks are like super-secure piggy banks that:
- Keep your money safe
- Help it grow
- Let you access it when needed

### Why use a bank instead of a piggy bank?

1. **Safety** 🔒
   - Banks are protected
   - Your money is insured
   - Much safer than keeping cash at home

2. **Growth** 📈
   - Banks pay you interest
   - Your money grows over time
   - Free money just for saving!

3. **Convenience** 💳
   - Access money from ATMs
   - Use debit cards
   - Transfer money easily

Remember: Banks are like helpers for your money!'''
                    },
                    {
                        'title': 'Types of Bank Accounts',
                        'section_type': 'content',
                        'order': 2,
                        'icon': 'credit-card',
                        'content': '''### Savings Account 💰

**What it is:**
- A place to save money
- Earns interest (free money!)
- Good for long-term savings

**Best for:**
- Saving for goals
- Emergency funds
- Money you won't need soon

### Checking Account 💳

**What it is:**
- A place for everyday money
- Easy to access
- Use with debit card

**Best for:**
- Daily spending
- Paying bills
- Money you use regularly

### For Kids:

Many banks offer **kid-friendly accounts**:
- Joint accounts with parents
- Lower fees
- Educational resources
- Fun features

Ask your parents about opening a kid-friendly account!'''
                    },
                    {
                        'title': 'What is Interest?',
                        'section_type': 'content',
                        'order': 3,
                        'icon': 'cash-coin',
                        'content': '''## Interest is FREE MONEY the bank pays you!

When you save money in a bank, the bank pays you extra money just for keeping it there!

### How does it work?

**Example:**
- You save $100 in the bank
- Bank pays 5% interest per year
- After 1 year, you have $105!
- You earned $5 for free! 🎉

### Simple Interest Formula:

**Interest = Principal × Rate × Time**

**Example:**
- Principal (money saved): $100
- Rate (interest %): 5% = 0.05
- Time: 1 year
- Interest = $100 × 0.05 × 1 = $5
- Total = $100 + $5 = $105

### Why is this exciting?

- 💰 Your money grows without doing anything!
- 📈 The longer you save, the more you earn
- 🎯 It helps you reach goals faster

Remember: Interest makes saving even better!'''
                    },
                    {
                        'title': 'Compound Interest (Advanced)',
                        'section_type': 'content',
                        'order': 4,
                        'icon': 'graph-up',
                        'content': '''### Compound Interest = Interest on Interest! 📈

**Simple Interest:**
- You earn interest only on your original money
- $100 at 5% = $5 per year

**Compound Interest:**
- You earn interest on your money AND on the interest you already earned
- Your money grows faster!

### Example:

**Year 1:**
- Start: $100
- Interest (5%): $5
- Total: $105

**Year 2:**
- Start: $105 (includes last year's interest!)
- Interest (5%): $5.25
- Total: $110.25

**Year 3:**
- Start: $110.25
- Interest (5%): $5.51
- Total: $115.76

**See how it grows?** The longer you save, the faster it grows!

### The Power of Time:

- 💪 Start saving early
- ⏰ Let time work for you
- 📈 Watch your money multiply

Remember: Time is your friend when saving!'''
                    },
                    {
                        'title': 'Bank Visit Simulation Activity',
                        'section_type': 'activity',
                        'order': 5,
                        'icon': 'controller',
                        'content': '''## Your Turn!

### Activity: Role-Play Opening an Account

**Scenario:** You want to open a savings account

**Steps:**
1. **Research** kid-friendly bank accounts (with parents)
2. **Learn** about interest rates
3. **Calculate** how much you'd earn

**Example Calculation:**

**Opening a Savings Account:**
- Starting amount: $100
- Interest rate: 5% per year
- Time: 1 year

**Calculate Interest:**
- Interest = $100 × 0.05 × 1 = $5
- Total after 1 year = $105

**After 2 years:**
- Interest = $105 × 0.05 × 1 = $5.25
- Total = $110.25

**Practice:**
- Try with different amounts
- Try with different interest rates
- See how your money grows!

**Your Turn:**
1. Pick an amount to save: $___
2. Find an interest rate: ___%
3. Calculate interest for 1 year: $___
4. Calculate total after 1 year: $___

Practice makes you a banking expert! 💪'''
                    },
                    {
                        'title': 'Interest Calculator Game',
                        'section_type': 'activity',
                        'order': 6,
                        'icon': 'calculator',
                        'content': '''### Practice Calculating Interest! 🧮

**Game Rules:**
1. Pick a starting amount
2. Pick an interest rate
3. Calculate interest for different time periods

**Example Problems:**

**Problem 1:**
- Amount: $200
- Rate: 4% per year
- Time: 1 year
- Interest = ?

**Answer:**
- Interest = $200 × 0.04 × 1 = $8
- Total = $208

**Problem 2:**
- Amount: $500
- Rate: 3% per year
- Time: 2 years
- Interest = ?

**Answer:**
- Year 1: $500 × 0.03 × 1 = $15 (Total: $515)
- Year 2: $515 × 0.03 × 1 = $15.45 (Total: $530.45)

**Your Turn:**
Create your own problems and solve them!

**Why is this useful?**
- You understand how banks work
- You can compare different accounts
- You make smarter saving decisions

Become an interest calculation expert! 🎉'''
                    },
                    {
                        'title': 'Homework: Research Kid-Friendly Banks',
                        'section_type': 'content',
                        'order': 7,
                        'icon': 'journal-text',
                        'content': '''## Your Assignment!

### Research Kid-Friendly Bank Accounts

**Steps:**
1. **With parent help**, research banks that offer kid accounts
2. **Compare** different options:
   - Interest rates
   - Fees
   - Features
   - Requirements

3. **Learn** about:
   - How to open an account
   - What you need
   - How interest works

4. **Discuss** with parents:
   - Is it a good idea?
   - Which bank is best?
   - When can you open one?

**Questions to Ask:**
- What is the interest rate?
- Are there any fees?
- What is the minimum deposit?
- Can parents monitor the account?
- What features does it have?

**What You'll Learn:**
- How banks work
- How to compare accounts
- How interest helps your money grow

Talk to your parents about opening a savings account! 🎉'''
                    }
                ],
                'tips': [
                    {
                        'title': 'Start saving early',
                        'icon': 'clock',
                        'order': 1,
                        'content': 'The earlier you start saving in a bank, the more time your money has to grow with interest. Time is your best friend!'
                    },
                    {
                        'title': 'Compare interest rates',
                        'icon': 'search',
                        'order': 2,
                        'content': 'Different banks offer different interest rates. Compare them to find the best deal and make your money grow faster!'
                    },
                    {
                        'title': 'Understand compound interest',
                        'icon': 'graph-up-arrow',
                        'order': 3,
                        'content': 'Compound interest means you earn interest on your interest. The longer you save, the faster your money grows!'
                    }
                ]
            },
            {
                'lesson_number': 9,
                'title': 'Basics of Investing',
                'slug': 'basics-of-investing',
                'subtitle': 'Learn how to make your money grow beyond saving!',
                'description': 'An introductory lesson explaining investing concepts, how investments can grow money, and the basics of risk and diversification.',
                'icon': 'trending-up',
                'age_range': '11-12',
                'duration_minutes': 30,
                'status': 'published',
                'sections': [
                    {
                        'title': 'What is Investing?',
                        'section_type': 'content',
                        'order': 1,
                        'icon': 'graph-up-arrow',
                        'content': '''## Investing means using money to make more money!

Instead of just saving money in a bank, you can invest it to potentially earn more.

### Saving vs. Investing:

**Saving:**
- 💰 Put money in a bank
- 🔒 Very safe
- 📈 Small, steady growth (interest)
- ✅ Guaranteed returns

**Investing:**
- 📊 Put money in stocks, bonds, etc.
- ⚠️ Some risk involved
- 📈 Potential for bigger growth
- ❓ Returns not guaranteed

### Why invest?

1. **Bigger growth potential** 📈
   - Can earn more than savings interest
   - Helps money grow faster
   - Reaches goals sooner

2. **Beat inflation** 💪
   - Prices go up over time
   - Investing helps your money keep up
   - Maintains purchasing power

3. **Long-term wealth** 🏆
   - Build wealth over time
   - Plan for the future
   - Achieve big goals

Remember: Investing is for the long term!'''
                    },
                    {
                        'title': 'Understanding Risk',
                        'section_type': 'content',
                        'order': 2,
                        'icon': 'exclamation-triangle',
                        'content': '''### What is Risk? ⚠️

**Risk** means your investment might:
- Go up in value ✅
- Go down in value ❌
- Stay the same ➡️

**Important:** Not all investments succeed!

### Types of Risk:

1. **Low Risk** 🟢
   - Savings accounts
   - Government bonds
   - Small, steady returns
   - Very safe

2. **Medium Risk** 🟡
   - Some stocks
   - Mutual funds
   - Moderate returns
   - Some ups and downs

3. **High Risk** 🔴
   - Individual stocks
   - Cryptocurrency
   - Big potential gains
   - Big potential losses

### For Kids:

- ✅ Start with low-risk options
- ✅ Learn before investing
- ✅ Only invest money you can afford to lose
- ✅ Talk to parents first

Remember: Never invest more than you can afford to lose!'''
                    },
                    {
                        'title': 'What are Stocks?',
                        'section_type': 'content',
                        'order': 3,
                        'icon': 'graph-up',
                        'content': '''### Stocks = Owning a Piece of a Company! 🏢

**What is a stock?**
- A small piece of a company
- When you buy a stock, you own part of that company
- If the company does well, your stock might go up in value

### How it works:

**Example:**
- Company: "Toy Store Inc."
- You buy 1 share for $10
- Company does well, makes more money
- Your share might be worth $12 now
- You made $2! 🎉

**But:**
- If company does poorly
- Your share might be worth $8
- You lost $2 😔

### For Learning:

**Stock Market Game:**
- Use free apps or websites
- Pretend to "buy" shares
- Track favorite companies
- Learn how stocks work
- No real money at risk!

**Example Companies:**
- Disney 🏰
- Apple 🍎
- Nike ✓
- McDonald's 🍔

Remember: Stocks can go up or down!'''
                    },
                    {
                        'title': 'Diversification: Don\'t Put All Eggs in One Basket',
                        'section_type': 'content',
                        'order': 4,
                        'icon': 'egg',
                        'content': '''### What is Diversification? 🥚

**Diversification** means spreading your investments across different things.

**Why?**
- If one investment fails, others might do well
- Reduces overall risk
- More balanced portfolio

### Example:

**Bad (Not Diversified):**
- Put all $100 in one company's stock
- If that company fails, you lose everything ❌

**Good (Diversified):**
- $30 in Company A
- $30 in Company B
- $30 in Company C
- $10 in savings
- If one fails, others might do well ✅

### For Kids:

**Simple Diversification:**
- Some money in savings (safe)
- Some money in different stocks (if allowed)
- Don't put everything in one place

**Remember:**
- 🥚 Don't put all eggs in one basket
- 📊 Spread your investments
- 🛡️ Reduce your risk

Diversification is like having a safety net!'''
                    },
                    {
                        'title': 'Stock Market Game Activity',
                        'section_type': 'activity',
                        'order': 5,
                        'icon': 'controller',
                        'content': '''## Your Turn!

### Activity: Track a Stock

**Task:** Follow a company's stock for one week

**Steps:**
1. **Pick a company** you know (with parent help):
   - Disney 🏰
   - Apple 🍎
   - Nike ✓
   - Or another favorite

2. **Track the stock price:**
   - Check the price on Day 1
   - Check the price each day for a week
   - See if it goes up or down

3. **Record your findings:**

**Stock Tracking Sheet:**

<table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
<thead>
<tr style="background-color: #eef2ff; border-bottom: 2px solid #6366f1;">
<th style="padding: 12px; text-align: left; border: 1px solid #c7d2fe;">Day</th>
<th style="padding: 12px; text-align: left; border: 1px solid #c7d2fe;">Company</th>
<th style="padding: 12px; text-align: right; border: 1px solid #c7d2fe;">Price</th>
<th style="padding: 12px; text-align: right; border: 1px solid #c7d2fe;">Change</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding: 10px; border: 1px solid #e5e7eb;"><strong>Mon</strong></td>
<td style="padding: 10px; border: 1px solid #e5e7eb;">Disney</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$100</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">-</td>
</tr>
<tr style="background-color: #fafafa;">
<td style="padding: 10px; border: 1px solid #e5e7eb;"><strong>Tue</strong></td>
<td style="padding: 10px; border: 1px solid #e5e7eb;">Disney</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$102</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb; color: #22c55e; font-weight: bold;">+$2</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #e5e7eb;"><strong>Wed</strong></td>
<td style="padding: 10px; border: 1px solid #e5e7eb;">Disney</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$101</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb; color: #ef4444; font-weight: bold;">-$1</td>
</tr>
<tr style="background-color: #fafafa;">
<td style="padding: 10px; border: 1px solid #e5e7eb;"><strong>Thu</strong></td>
<td style="padding: 10px; border: 1px solid #e5e7eb;">Disney</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$103</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb; color: #22c55e; font-weight: bold;">+$2</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #e5e7eb;"><strong>Fri</strong></td>
<td style="padding: 10px; border: 1px solid #e5e7eb;">Disney</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb;">$105</td>
<td style="padding: 10px; text-align: right; border: 1px solid #e5e7eb; color: #22c55e; font-weight: bold;">+$2</td>
</tr>
</tbody>
</table>

**What you learned:**
- Stocks change every day
- Prices go up and down
- Investing requires patience

**Your Turn:**
Pick a company and track it for a week! 💪'''
                    },
                    {
                        'title': 'Lemonade Stand Investment',
                        'section_type': 'activity',
                        'order': 6,
                        'icon': 'cup-straw',
                        'content': '''### Real-World Investment Example! 🍋

**Scenario:** You have a lemonade stand

**Week 1:**
- You earn $20
- You spend it all on candy

**Week 2 (Smart Investment):**
- You earn $20
- You "invest" $10 in supplies:
  - Better cups
  - More lemons
  - Better sign
- You spend $10 on candy

**Week 3:**
- Because of your investment, you earn $40!
- Your business grew!

**What you learned:**
- Investing in your business helps it grow
- Sometimes spending money now makes more money later
- Smart investments pay off

**Your Turn:**
Think of a way to "invest" in something:
- Better school supplies → Better grades?
- Sports equipment → Better performance?
- Art supplies → Better projects?

How can you invest in yourself? 💪'''
                    },
                    {
                        'title': 'Long-Term Thinking',
                        'section_type': 'content',
                        'order': 7,
                        'icon': 'target',
                        'content': '''### Invest for the Future! 🎯

**Investing is for the long term:**
- Not for quick money
- For future goals
- Requires patience

### Long-Term Goals:

1. **College** 🎓
   - Save and invest for education
   - Start early
   - Let time work for you

2. **First Car** 🚗
   - Save for when you're older
   - Invest to grow money
   - Reach goal faster

3. **Future Dreams** ✨
   - Travel
   - Starting a business
   - Big purchases

### The Power of Starting Early:

**Example:**
- Start investing at age 12
- Invest $10 per month
- By age 18, you have a good start!

**Remember:**
- ⏰ Time is your friend
- 📈 Start early
- 🎯 Think long-term
- 💪 Be patient

Investing is about planning for your future! 🎉'''
                    },
                    {
                        'title': 'Homework: Follow an Investment',
                        'section_type': 'content',
                        'order': 8,
                        'icon': 'journal-text',
                        'content': '''## Your Assignment!

### Follow a Simple Investment

**Task:** Track an investment for one week

**Steps:**
1. **Pick a stock** (with parent help):
   - Choose a company you know
   - Use a free stock tracking app
   - Or use pretend money

2. **Track it daily:**
   - Record the price each day
   - Note if it goes up or down
   - See the changes

3. **Report your findings:**
   - What company did you track?
   - How did the price change?
   - What did you learn?

**Questions to Answer:**
- Did the stock go up or down?
- Why do you think it changed?
- Would you invest in it? Why or why not?

**What You'll Learn:**
- How investments work
- How prices change
- The importance of research

Practice tracking investments and become an investing expert! 🎉'''
                    }
                ],
                'tips': [
                    {
                        'title': 'Start with learning',
                        'icon': 'bookshelf',
                        'order': 1,
                        'content': 'Before investing real money, learn about how investments work. Use games and simulations to practice first!'
                    },
                    {
                        'title': 'Understand risk',
                        'icon': 'exclamation-triangle',
                        'order': 2,
                        'content': 'All investments have risk. Never invest more than you can afford to lose, and always talk to parents first!'
                    },
                    {
                        'title': 'Diversify your investments',
                        'icon': 'egg',
                        'order': 3,
                        'content': 'Don\'t put all your money in one investment. Spread it across different things to reduce risk!'
                    },
                    {
                        'title': 'Think long-term',
                        'icon': 'clock',
                        'order': 4,
                        'content': 'Investing is for the future, not quick money. Be patient and let your investments grow over time!'
                    }
                ]
            },
            {
                'lesson_number': 10,
                'title': 'Avoiding Debt and Credit Basics',
                'slug': 'avoiding-debt-credit-basics',
                'subtitle': 'Learn about debt and how to use credit wisely!',
                'description': 'An important lesson teaching kids about debt, credit cards, and how to live within your means to stay debt-free.',
                'icon': 'credit-card-2-front',
                'age_range': '11-12',
                'duration_minutes': 30,
                'status': 'published',
                'sections': [
                    {
                        'title': 'What is Debt?',
                        'section_type': 'content',
                        'order': 1,
                        'icon': 'credit-card',
                        'content': '''## Debt is borrowing money you must pay back!

When you borrow money, you have to pay it back, usually with extra money called interest.

### Types of Debt:

1. **Good Debt** ✅
   - Student loans (for education)
   - Mortgage (for a house)
   - Things that help you in the long run

2. **Bad Debt** ❌
   - Credit card debt for toys
   - Loans for things you don't need
   - Debt that doesn't help you

### Why is debt dangerous?

- 💸 You pay back MORE than you borrowed
- ⏰ You're stuck paying for a long time
- 😔 It can be stressful
- 🚫 Limits your future choices

Remember: Debt means you owe money to someone!'''
                    },
                    {
                        'title': 'What are Credit Cards?',
                        'section_type': 'content',
                        'order': 2,
                        'icon': 'credit-card',
                        'content': '''### Credit Cards = Borrowed Money! 💳

**What is a credit card?**
- A card that lets you borrow money
- You buy things now, pay later
- If you don't pay on time, you pay extra (interest)

### How credit cards work:

**Example:**
- You buy a $50 toy with a credit card
- You don't pay the bill on time
- You now owe $50 + interest (maybe $55)
- You pay MORE than the toy cost!

### For Kids:

**Credit cards are for adults:**
- You need to be 18+ to get one
- Parents use them responsibly
- Kids should learn about them

**What to know:**
- ⚠️ Credit cards are like loans
- 💰 You must pay back what you borrow
- ⏰ Pay on time or pay extra
- 🚫 Don't spend more than you can afford

Remember: Credit cards are tools, not free money!'''
                    },
                    {
                        'title': 'The Dangers of Debt',
                        'section_type': 'content',
                        'order': 3,
                        'icon': 'exclamation-triangle',
                        'content': '''### Why Debt is Dangerous ⚠️

**Problem 1: Interest**
- You borrow $100
- You pay back $110 (with interest)
- You paid $10 extra!

**Problem 2: Debt Grows**
- You owe $100
- You can't pay it
- Interest keeps adding up
- Soon you owe $150, $200, more!

**Problem 3: Stress**
- Worrying about money
- Can't buy things you want
- Feel trapped
- Hard to get out

**Problem 4: Limits Future**
- Can't save money
- Can't invest
- Can't reach goals
- Stuck paying debt

### Example:

**Bad Scenario:**
- Buy $200 toy on credit
- Can't pay it back
- Interest adds up
- Owe $250, then $300
- Stuck in debt! 😔

**Good Scenario:**
- Save $200 first
- Then buy the toy
- No debt
- Feel proud! 😊

Remember: Debt can trap you!'''
                    },
                    {
                        'title': 'Living Within Your Means',
                        'section_type': 'content',
                        'order': 4,
                        'icon': 'cash-coin',
                        'content': '''### What Does "Living Within Your Means" Mean? 💰

**It means:**
- Only spend what you have
- Don't borrow to buy things
- Save before you spend
- Stay debt-free

### How to do it:

1. **Budget your money** 📊
   - Know how much you have
   - Plan your spending
   - Stick to your budget

2. **Save before spending** 💰
   - Want something? Save for it!
   - Don't borrow money
   - Wait until you can afford it

3. **Avoid impulse buys** 🚫
   - Think before buying
   - Use the 24-hour rule
   - Don't buy on credit

4. **Build an emergency fund** 🏦
   - Save for surprises
   - Don't need to borrow
   - Feel secure

### Benefits:

- ✅ No debt stress
- ✅ More freedom
- ✅ Can save and invest
- ✅ Reach your goals
- ✅ Feel in control

Remember: Living within your means = freedom!'''
                    },
                    {
                        'title': 'Debt Scenario Role-Play',
                        'section_type': 'activity',
                        'order': 5,
                        'icon': 'mask',
                        'content': '''## Your Turn!

### Activity: Debt Scenario

**Scenario:** You want a $50 toy

**Option 1: Borrow (Bad)**
- Borrow $50 to buy it now
- Interest: 10% = $5
- Total to pay back: $55
- You pay $5 extra! ❌

**Option 2: Save (Good)**
- Save $10 per week
- After 5 weeks, you have $50
- Buy it with your own money
- No debt, no interest! ✅

**Calculate the Difference:**

**Borrowing:**
- Cost: $50
- Interest: $5
- Total: $55
- Time to pay: Several months

**Saving:**
- Cost: $50
- Interest: $0
- Total: $50
- Time to save: 5 weeks

**You save $5 by saving first!**

**Your Turn:**
Pick something you want:
1. Calculate cost if you borrow
2. Calculate time to save
3. Decide: borrow or save?

Practice making smart choices! 💪'''
                    },
                    {
                        'title': 'Pros and Cons of Debt',
                        'section_type': 'content',
                        'order': 6,
                        'icon': 'scale',
                        'content': '''### Debt: Pros and Cons ⚖️

**PROS of Debt:**

1. **Buy now, pay later** ⏰
   - Get things immediately
   - Don't have to wait
   - Instant gratification

2. **Build credit (for adults)** 📊
   - Good for future loans
   - Shows responsibility
   - Helps with big purchases

**CONS of Debt:**

1. **Pay extra interest** 💸
   - Everything costs more
   - Waste money on interest
   - Pay back more than borrowed

2. **Risk of overspending** ⚠️
   - Easy to spend too much
   - Hard to track spending
   - Can get into trouble

3. **Stress and worry** 😔
   - Always thinking about debt
   - Feel trapped
   - Limits your choices

4. **Hard to get out** 🚫
   - Debt can grow
   - Takes time to pay off
   - Limits future options

### The Bottom Line:

- ❌ Avoid debt for wants
- ✅ Only good debt: education, house
- 💰 Save before you spend
- 🎯 Stay debt-free

Remember: Debt is a tool, use it wisely!'''
                    },
                    {
                        'title': 'When is Debt Okay?',
                        'section_type': 'content',
                        'order': 7,
                        'icon': 'check-circle',
                        'content': '''### Good Debt vs. Bad Debt ✅

**GOOD Debt (Maybe Okay):**

1. **Education** 🎓
   - Student loans for college
   - Invests in your future
   - Helps you earn more later

2. **House** 🏠
   - Mortgage for a home
   - Home usually increases in value
   - Long-term investment

3. **Business** 💼
   - Loan to start a business
   - Can make money
   - Calculated risk

**BAD Debt (Avoid!):**

1. **Toys and games** 🎮
   - Things you want but don't need
   - Don't help you in the future
   - Waste of money

2. **Clothes and treats** 👕
   - Things you can save for
   - Not necessary
   - Should pay cash

3. **Impulse purchases** 🛒
   - Things you buy without thinking
   - Usually regret later
   - Should avoid

### Rule of Thumb:

- ✅ Good debt: Invests in your future
- ❌ Bad debt: Just for wants
- 💡 When in doubt, save first!

Remember: Only borrow for things that help your future!'''
                    },
                    {
                        'title': 'How to Avoid Debt',
                        'section_type': 'content',
                        'order': 8,
                        'icon': 'shield-check',
                        'content': '''### Tips to Stay Debt-Free! 🛡️

1. **Save before spending** 💰
   - Want something? Save for it!
   - Don't borrow money
   - Build the habit

2. **Budget your money** 📊
   - Know what you have
   - Plan your spending
   - Stick to your plan

3. **Avoid credit cards (as a kid)** 🚫
   - Wait until you're older
   - Learn about them first
   - Use cash or debit

4. **Build emergency fund** 🏦
   - Save for surprises
   - Don't need to borrow
   - Feel secure

5. **Live within your means** ✅
   - Only spend what you have
   - Don't try to keep up with others
   - Be happy with what you can afford

6. **Think long-term** 🎯
   - Short-term debt = long-term problems
   - Save now = freedom later
   - Plan for the future

### Good Habits:

- ✅ Save regularly
- ✅ Budget your money
- ✅ Avoid impulse buys
- ✅ Think before spending
- ✅ Stay debt-free

Remember: Good habits prevent debt!'''
                    },
                    {
                        'title': 'Homework: Family Money Discussion',
                        'section_type': 'content',
                        'order': 9,
                        'icon': 'journal-text',
                        'content': '''## Your Assignment!

### Discuss Family Examples of Smart Money Choices

**Task:** Talk with your family about money

**Discussion Topics:**

1. **Smart choices your family made:**
   - When did you save before buying?
   - What did you avoid buying?
   - How did it help?

2. **Lessons learned:**
   - What mistakes were made?
   - What did you learn?
   - How did you fix it?

3. **Debt experiences:**
   - Has anyone had debt?
   - How did it feel?
   - How did they get out of it?

4. **Good habits:**
   - What money habits work well?
   - What would you do differently?
   - What advice do you have?

**Questions to Ask:**
- How do we avoid debt?
- What are our family's money rules?
- How can I learn to manage money better?

**What You'll Learn:**
- Real-world money experiences
- How to avoid debt
- Smart money habits
- Family values about money

Have a family money meeting and learn together! 🎉'''
                    }
                ],
                'tips': [
                    {
                        'title': 'Save before you spend',
                        'icon': 'cash-coin',
                        'order': 1,
                        'content': 'The best way to avoid debt is to save money before buying things. This keeps you debt-free and in control!'
                    },
                    {
                        'title': 'Understand interest',
                        'icon': 'currency-dollar',
                        'order': 2,
                        'content': 'When you borrow money, you pay interest. This means everything costs more. Always calculate the true cost!'
                    },
                    {
                        'title': 'Live within your means',
                        'icon': 'check-circle',
                        'order': 3,
                        'content': 'Only spend what you have. Don\'t borrow to buy things you want. This keeps you free from debt stress!'
                    },
                    {
                        'title': 'Build good habits early',
                        'icon': 'seedling',
                        'order': 4,
                        'content': 'Start building good money habits now. Save, budget, and avoid debt. These habits will help you your whole life!'
                    }
                ]
            }
        ]

        # Create all lessons
        for lesson_data in lessons_data:
            lesson_number = lesson_data['lesson_number']
            sections_data = lesson_data.pop('sections')
            tips_data = lesson_data.pop('tips')
            
            lesson, created = Lesson.objects.get_or_create(
                lesson_number=lesson_number,
                defaults=lesson_data
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created Lesson {lesson_number}: {lesson.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Lesson {lesson_number} already exists. Updating content...'))
                for key, value in lesson_data.items():
                    setattr(lesson, key, value)
                lesson.save()
                # Delete existing sections and tips to recreate them
                lesson.sections.all().delete()
                lesson.tips.all().delete()
                self.stdout.write(self.style.SUCCESS(f'✓ Updated Lesson {lesson_number}: {lesson.title}'))
            
            # Create sections
            for section_data in sections_data:
                section, section_created = LessonSection.objects.get_or_create(
                    lesson=lesson,
                    title=section_data['title'],
                    defaults=section_data
                )
                if not section_created:
                    for key, value in section_data.items():
                        setattr(section, key, value)
                    section.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created/Updated section: {section.title}'))
            
            # Create tips
            for tip_data in tips_data:
                tip, tip_created = LessonTip.objects.get_or_create(
                    lesson=lesson,
                    title=tip_data['title'],
                    defaults=tip_data
                )
                if not tip_created:
                    for key, value in tip_data.items():
                        setattr(tip, key, value)
                    tip.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created/Updated tip: {tip.title}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ All lessons (2-10) created successfully!'))
        self.stdout.write(self.style.SUCCESS('Visit: http://127.0.0.1:8000/lessons/'))






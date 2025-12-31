from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Achievement(models.Model):
    """Achievement model"""
    ACHIEVEMENT_TYPES = [
        ('lesson_complete', 'Lesson Completed'),
        ('saving_goal_reached', 'Saving Goal Reached'),
        ('spending_tracked', 'Spending Tracked'),
        ('wallet_created', 'Wallet Created'),
        ('milestone', 'Milestone'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Achievement Name')
    description = models.TextField(verbose_name='Description')
    icon = models.CharField(max_length=50, default='🏆', verbose_name='Icon (emoji)')
    color = models.CharField(max_length=20, default='#FFD700', verbose_name='Color (hex)')
    achievement_type = models.CharField(max_length=50, choices=ACHIEVEMENT_TYPES, verbose_name='Achievement Type')
    coin_reward = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Coin Reward', help_text='Virtual coins awarded when unlocked')
    
    # Unlock conditions (JSON field, stores different types of conditions)
    requirements = models.JSONField(default=dict, blank=True, verbose_name='Requirements', help_text='JSON field for storing unlock conditions')
    
    # Sorting and display
    order = models.IntegerField(default=0, verbose_name='Order', help_text='Order for display')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'
    
    def __str__(self):
        return f"{self.icon} {self.name}"
    
    def get_absolute_url(self):
        return reverse('achievements:achievement_detail', kwargs={'pk': self.pk})


class UserAchievement(models.Model):
    """User achievement tracking model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_achievements', verbose_name='User')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements', verbose_name='Achievement')
    
    # Unlock time
    unlocked_at = models.DateTimeField(auto_now_add=True, verbose_name='Unlocked At')
    
    # Whether user has been notified
    is_notified = models.BooleanField(default=False, verbose_name='Is Notified')
    
    class Meta:
        unique_together = [['user', 'achievement']]
        ordering = ['-unlocked_at']
        verbose_name = 'User Achievement'
        verbose_name_plural = 'User Achievements'
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
    
    def get_absolute_url(self):
        return reverse('achievements:user_achievement_detail', kwargs={'pk': self.pk})





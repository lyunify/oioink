from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Sum
from decimal import Decimal

User = get_user_model()


class SpendingCategory(models.Model):
    """Spending category model"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Category Name')
    icon = models.CharField(max_length=50, default='💰', verbose_name='Icon (emoji)')
    color = models.CharField(max_length=20, default='#667eea', verbose_name='Color (hex)')
    description = models.TextField(blank=True, verbose_name='Description')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Spending Category'
        verbose_name_plural = 'Spending Categories'
    
    def __str__(self):
        return f"{self.icon} {self.name}"


class Spending(models.Model):
    """Spending record model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spendings', verbose_name='User')
    category = models.ForeignKey(SpendingCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Category')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    description = models.CharField(max_length=200, verbose_name='Description')
    child_name = models.CharField(max_length=50, blank=True, verbose_name='Child Name')
    date = models.DateField(verbose_name='Date')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Spending'
        verbose_name_plural = 'Spendings'
    
    def __str__(self):
        return f"{self.date} - {self.amount} - {self.description}"
    
    def get_absolute_url(self):
        return reverse('tracking:spending_detail', kwargs={'pk': self.pk})


class SavingGoal(models.Model):
    """Saving goal model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saving_goals', verbose_name='User')
    goal_name = models.CharField(max_length=200, verbose_name='Goal Name', help_text='What are you saving for?')
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Target Amount')
    child_name = models.CharField(max_length=50, blank=True, verbose_name='Child Name')
    deadline = models.DateField(null=True, blank=True, verbose_name='Deadline', help_text='Optional deadline for this goal')
    icon = models.CharField(max_length=50, default='🎯', verbose_name='Icon (emoji)')
    color = models.CharField(max_length=20, default='#28a745', verbose_name='Color (hex)')
    description = models.TextField(blank=True, verbose_name='Description')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Saving Goal'
        verbose_name_plural = 'Saving Goals'
    
    def __str__(self):
        return f"{self.goal_name} - ${self.target_amount}"
    
    def get_absolute_url(self):
        return reverse('tracking:saving_goal_detail', kwargs={'pk': self.pk})
    
    @property
    def current_amount(self):
        """Calculate current saved amount (sum of associated Saving records)"""
        total = self.savings.aggregate(Sum('amount'))['amount__sum']
        return total if total else Decimal('0.00')
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.target_amount > 0:
            percentage = (self.current_amount / self.target_amount) * 100
            return min(percentage, 100)  # Show maximum 100%
        return 0
    
    @property
    def remaining_amount(self):
        """Calculate remaining amount"""
        remaining = self.target_amount - self.current_amount
        return max(remaining, Decimal('0.00'))
    
    @property
    def is_completed(self):
        """Determine if goal is completed"""
        return self.current_amount >= self.target_amount


class Saving(models.Model):
    """Savings record model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings', verbose_name='User')
    saving_goal = models.ForeignKey(SavingGoal, on_delete=models.SET_NULL, null=True, blank=True, related_name='savings', verbose_name='Saving Goal')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    description = models.CharField(max_length=200, verbose_name='Description')
    child_name = models.CharField(max_length=50, blank=True, verbose_name='Child Name')
    date = models.DateField(verbose_name='Date')
    goal = models.CharField(max_length=200, blank=True, verbose_name='Saving Goal (Legacy)', help_text='What are you saving for? (Deprecated: use Saving Goal instead)')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Saving'
        verbose_name_plural = 'Savings'
    
    def __str__(self):
        return f"{self.date} - {self.amount} - {self.description}"
    
    def get_absolute_url(self):
        return reverse('tracking:saving_detail', kwargs={'pk': self.pk})



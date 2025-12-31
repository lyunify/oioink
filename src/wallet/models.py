from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Sum, Q

User = get_user_model()


class Wallet(models.Model):
    """Virtual coin wallet model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets', verbose_name='User')
    child_name = models.CharField(max_length=50, blank=True, verbose_name='Child Name', help_text='Optional: Name of the child this wallet belongs to')
    coin_name = models.CharField(max_length=50, default='Coin', verbose_name='Coin Name', help_text='Name of the virtual coin (e.g., Star Coin, Learning Coin)')
    coin_icon = models.CharField(max_length=10, default='⭐', verbose_name='Coin Icon', help_text='Emoji icon for the coin')
    
    # Practice Mode
    is_practice_mode = models.BooleanField(default=False, verbose_name='Is Practice Mode', help_text='Whether this is a practice mode wallet')
    practice_initial_balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name='Practice Initial Balance',
        help_text='Initial balance for practice mode wallet (optional)'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        unique_together = [['user', 'child_name', 'coin_name']]
    
    def __str__(self):
        mode_text = " (Practice)" if self.is_practice_mode else ""
        if self.child_name:
            return f"{self.coin_icon} {self.coin_name} - {self.child_name}{mode_text}"
        return f"{self.coin_icon} {self.coin_name}{mode_text}"
    
    def get_absolute_url(self):
        return reverse('wallet:wallet_detail', kwargs={'pk': self.pk})
    
    @property
    def balance(self):
        """Calculate wallet balance"""
        from .utils import calculate_wallet_balance
        return calculate_wallet_balance(self)


class WalletTransaction(models.Model):
    """Wallet transaction record model"""
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions', verbose_name='Wallet')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, verbose_name='Transaction Type')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    description = models.CharField(max_length=200, verbose_name='Description')
    date = models.DateField(verbose_name='Date')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Wallet Transaction'
        verbose_name_plural = 'Wallet Transactions'
    
    def __str__(self):
        return f"{self.date} - {self.transaction_type} - {self.amount} - {self.description}"
    
    def get_absolute_url(self):
        return reverse('wallet:transaction_detail', kwargs={'pk': self.pk})


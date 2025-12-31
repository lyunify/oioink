from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Prize(models.Model):
    """Prize model"""
    PRIZE_CATEGORIES = [
        ('digital', 'Digital Reward'),      # Digital rewards (e.g., virtual badges, avatar frames)
        ('physical', 'Physical Prize'),      # Physical prizes (e.g., stickers, small toys)
        ('privilege', 'Special Privilege'),  # Privileges (e.g., unlock special content)
        ('certificate', 'Certificate'),      # Certificates/awards
    ]
    
    PRIZE_STATUS = [
        ('active', 'Active'),      # Available
        ('inactive', 'Inactive'),  # Unavailable
        ('sold_out', 'Sold Out'),  # Sold out
    ]
    
    # Basic information
    name = models.CharField(max_length=200, verbose_name='Prize Name')
    description = models.TextField(verbose_name='Description')
    icon = models.CharField(max_length=50, default='🎁', verbose_name='Icon (emoji)')
    image = models.ImageField(upload_to='prizes/', blank=True, null=True, verbose_name='Prize Image')
    
    # Category and status
    category = models.CharField(max_length=20, choices=PRIZE_CATEGORIES, default='digital', verbose_name='Category')
    status = models.CharField(max_length=20, choices=PRIZE_STATUS, default='active', verbose_name='Status')
    
    # Price and stock
    coin_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Coin Cost', help_text='Virtual coin price')
    stock_quantity = models.IntegerField(default=-1, verbose_name='Stock Quantity', help_text='Stock quantity (-1 means unlimited)')
    available_from = models.DateField(null=True, blank=True, verbose_name='Available From', help_text='Start availability date')
    available_until = models.DateField(null=True, blank=True, verbose_name='Available Until', help_text='End availability date')
    
    # Sorting and priority
    priority = models.IntegerField(default=0, verbose_name='Priority', help_text='Display priority (higher number appears first)')
    is_featured = models.BooleanField(default=False, verbose_name='Is Featured', help_text='Whether recommended/featured')
    
    # Age restrictions
    min_age = models.IntegerField(null=True, blank=True, verbose_name='Minimum Age')
    max_age = models.IntegerField(null=True, blank=True, verbose_name='Maximum Age')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        ordering = ['-priority', '-is_featured', 'name']
        verbose_name = 'Prize'
        verbose_name_plural = 'Prizes'
    
    def __str__(self):
        return f"{self.icon} {self.name}"
    
    def get_absolute_url(self):
        return reverse('prizes:prize_detail', kwargs={'pk': self.pk})
    
    @property
    def is_available(self):
        """Check if prize is available"""
        if self.status != 'active':
            return False
        
        now = timezone.now().date()
        
        # Check time restrictions
        if self.available_from and now < self.available_from:
            return False
        if self.available_until and now > self.available_until:
            return False
        
        # Check stock
        if self.stock_quantity >= 0 and self.stock_quantity <= 0:
            return False
        
        return True
    
    @property
    def remaining_stock(self):
        """Get remaining stock"""
        if self.stock_quantity < 0:
            return -1  # Unlimited
        return self.stock_quantity
    
    def can_be_redeemed_by(self, user):
        """Check if user can redeem this prize"""
        if not self.is_available:
            return False, "This prize is not available"
        
        # Check stock
        if self.stock_quantity >= 0 and self.stock_quantity <= 0:
            return False, "This prize is sold out"
        
        # Check user balance (need to get from wallet system)
        try:
            from wallet.models import Wallet
            from wallet.utils import get_user_wallets_summary
            
            wallet_summary = get_user_wallets_summary(user)
            total_balance = wallet_summary.get('total_balance', 0)
            
            if total_balance < self.coin_cost:
                return False, f"Insufficient balance. You need {self.coin_cost} coins, but you have {total_balance} coins"
            
            return True, "Can be redeemed"
        except Exception:
            return False, "Error checking balance"
    
    def redeem_for_user(self, user, wallet=None):
        """Redeem prize for user (deduct virtual coins)"""
        can_redeem, message = self.can_be_redeemed_by(user)
        if not can_redeem:
            return False, message
        
        try:
            from wallet.models import Wallet, WalletTransaction
            from wallet.utils import get_user_wallets_summary
            from django.utils import timezone
            
            # If no wallet specified, use first wallet
            if not wallet:
                wallet = Wallet.objects.filter(user=user).first()
                if not wallet:
                    return False, "No wallet found. Please create a wallet first."
            
            # Deduct virtual coins
            WalletTransaction.objects.create(
                wallet=wallet,
                transaction_type='expense',
                amount=self.coin_cost,
                description=f'Prize redemption: {self.name}',
                date=timezone.now().date()
            )
            
            # If stock limited, decrease stock
            if self.stock_quantity >= 0:
                self.stock_quantity -= 1
                if self.stock_quantity <= 0:
                    self.status = 'sold_out'
                self.save()
            
            return True, "Prize redeemed successfully"
        except Exception as e:
            return False, f"Error redeeming prize: {str(e)}"





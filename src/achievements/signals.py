"""Achievement system signal handlers"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from tracking.models import SavingGoal, Saving, Spending
from wallet.models import Wallet
from achievements.utils import check_and_unlock_achievements

User = get_user_model()


@receiver(post_save, sender=Saving)
def check_saving_goal_achievements(sender, instance, created, **kwargs):
    """When saving record is saved, check if associated saving goal is completed and unlock achievements"""
    if created and instance.saving_goal:
        # Refresh goal object to get latest progress
        saving_goal = SavingGoal.objects.get(pk=instance.saving_goal.pk)
        
        # Check if goal is completed
        if saving_goal.is_completed:
            # Check and unlock "saving goal reached" type achievements
            check_and_unlock_achievements(
                user=instance.user,
                achievement_type='saving_goal_reached',
                goal_id=saving_goal.id
            )


@receiver(post_save, sender=Wallet)
def check_wallet_created_achievements(sender, instance, created, **kwargs):
    """When wallet is created, check if achievements should be unlocked"""
    if created:
        # Get user's total wallet count
        wallet_count = Wallet.objects.filter(user=instance.user).count()
        
        # Check and unlock "wallet created" type achievements
        check_and_unlock_achievements(
            user=instance.user,
            achievement_type='wallet_created',
            wallet_count=wallet_count
        )


@receiver(post_save, sender=Spending)
def check_spending_tracked_achievements(sender, instance, created, **kwargs):
    """When spending record is created, check if achievements should be unlocked"""
    if created:
        # Get user's total spending record count
        spending_count = Spending.objects.filter(user=instance.user).count()
        
        # Check and unlock "spending tracked" type achievements
        check_and_unlock_achievements(
            user=instance.user,
            achievement_type='spending_tracked',
            tracked_count=spending_count
        )


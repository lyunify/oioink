"""Achievement system utility functions"""
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Achievement, UserAchievement
from decimal import Decimal

User = get_user_model()


def unlock_achievement(user, achievement, notify=True):
    """Unlock achievement
    
    Args:
        user: User object
        achievement: Achievement object
        notify: Whether to mark as needing user notification
    
    Returns:
        UserAchievement object (returns existing object if already unlocked)
    """
    # Check if already unlocked
    user_achievement, created = UserAchievement.objects.get_or_create(
        user=user,
        achievement=achievement
    )
    
    if created:
        # If newly unlocked achievement, reward virtual coins
        if achievement.coin_reward > 0:
            # Try to add to user's wallet (need at least one wallet)
            try:
                from wallet.models import Wallet, WalletTransaction
                # Get user's first wallet, skip reward if none exists
                user_wallet = Wallet.objects.filter(user=user).first()
                if user_wallet:
                    WalletTransaction.objects.create(
                        wallet=user_wallet,
                        transaction_type='income',
                        amount=achievement.coin_reward,
                        description=f'Achievement reward: {achievement.name}',
                        date=timezone.now().date()
                    )
            except Exception:
                # If wallet system unavailable, fail silently
                pass
        
        # Mark if notification needed
        if notify:
            user_achievement.is_notified = False
            user_achievement.save()
    
    return user_achievement


def check_and_unlock_achievements(user, achievement_type, **kwargs):
    """Check and unlock achievements that meet conditions
    
    Args:
        user: User object
        achievement_type: Achievement type
        **kwargs: Additional condition parameters
    """
    # Get all active achievements of this type
    achievements = Achievement.objects.filter(
        achievement_type=achievement_type,
        is_active=True
    )
    
    unlocked_achievements = []
    
    for achievement in achievements:
        # Check if already unlocked
        if UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            continue
        
        # Check conditions based on achievement type
        if _check_achievement_requirements(user, achievement, achievement_type, **kwargs):
            user_achievement = unlock_achievement(user, achievement)
            unlocked_achievements.append(user_achievement)
    
    return unlocked_achievements


def _check_achievement_requirements(user, achievement, achievement_type, **kwargs):
    """Check if achievement meets unlock conditions (internal function)
    
    Args:
        user: User object
        achievement: Achievement object
        achievement_type: Achievement type
        **kwargs: Condition parameters
    """
    requirements = achievement.requirements or {}
    
    if achievement_type == 'lesson_complete':
        # Check completed lesson count
        required_count = requirements.get('lesson_count', 1)
        completed_count = kwargs.get('completed_count', 0)
        return completed_count >= required_count
    
    elif achievement_type == 'saving_goal_reached':
        # Check if saving goal reached
        # If goal_id not specified in requirements, any goal completion works
        goal_id = kwargs.get('goal_id')
        target_id = requirements.get('goal_id')
        # If no specific goal specified, any goal completion can unlock
        if target_id is None:
            return True
        return goal_id == target_id
    
    elif achievement_type == 'spending_tracked':
        # Check tracked spending count
        required_count = requirements.get('spending_count', 1)
        tracked_count = kwargs.get('tracked_count', 0)
        return tracked_count >= required_count
    
    elif achievement_type == 'wallet_created':
        # Check created wallet count
        required_count = requirements.get('wallet_count', 1)
        wallet_count = kwargs.get('wallet_count', 0)
        return wallet_count >= required_count
    
    elif achievement_type == 'milestone':
        # Generic milestone type, can define various conditions via requirements
        return True  # Temporarily always return True, can implement specific logic based on requirements later
    
    return False


def get_user_achievements(user):
    """Get all achievements for user
    
    Returns:
        dict: {
            'unlocked': [...],  # Unlocked achievements
            'locked': [...],    # Locked achievements
            'total': int,       # Total achievement count
            'unlocked_count': int,  # Unlocked count
        }
    """
    all_achievements = Achievement.objects.filter(is_active=True).order_by('order', 'created_at')
    unlocked_achievement_ids = UserAchievement.objects.filter(
        user=user
    ).values_list('achievement_id', flat=True)
    
    unlocked = []
    locked = []
    
    for achievement in all_achievements:
        if achievement.id in unlocked_achievement_ids:
            unlocked.append(achievement)
        else:
            locked.append(achievement)
    
    return {
        'unlocked': unlocked,
        'locked': locked,
        'total': all_achievements.count(),
        'unlocked_count': len(unlocked),
    }


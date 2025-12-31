"""Lesson system signal handlers"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import UserLessonProgress
from .utils import reward_lesson_completion
from achievements.utils import check_and_unlock_achievements


# For tracking previous status
_previous_status = {}


@receiver(pre_save, sender=UserLessonProgress)
def save_previous_status(sender, instance, **kwargs):
    """Save previous status"""
    if instance.pk:
        try:
            previous = UserLessonProgress.objects.get(pk=instance.pk)
            _previous_status[instance.pk] = previous.status
        except UserLessonProgress.DoesNotExist:
            _previous_status[instance.pk] = None


@receiver(post_save, sender=UserLessonProgress)
def handle_lesson_completion(sender, instance, **kwargs):
    """When lesson progress is saved, check if completed and handle rewards"""
    # Check if lesson was just marked as completed (previous status was not completed)
    previous_status = _previous_status.get(instance.pk)
    
    if (instance.status == 'completed' and 
        instance.completed_at and 
        previous_status != 'completed'):
        
        # Reward virtual coins
        reward_lesson_completion(instance.user, instance.lesson)
        
        # Check and unlock achievements
        try:
            completed_count = UserLessonProgress.objects.filter(
                user=instance.user,
                status='completed'
            ).count()
            
            check_and_unlock_achievements(
                user=instance.user,
                achievement_type='lesson_complete',
                completed_count=completed_count
            )
        except Exception:
            pass  # If achievement system unavailable, fail silently
        
        # Clean up temporary status
        if instance.pk in _previous_status:
            del _previous_status[instance.pk]


from markdown import markdown
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Lesson, LessonSection, LessonTip, UserLessonProgress

User = get_user_model()


def get_published_lessons():
    """Get all published lessons"""
    return Lesson.objects.filter(status='published').order_by('lesson_number')


def get_lesson_by_number(lesson_number):
    """Get lesson by lesson number"""
    try:
        return Lesson.objects.get(lesson_number=lesson_number, status='published')
    except Lesson.DoesNotExist:
        return None


def get_next_lesson(current_lesson):
    """Get next lesson after current lesson
    
    Args:
        current_lesson: Current lesson object
    
    Returns:
        Lesson object or None (if no next lesson)
    """
    try:
        return Lesson.objects.filter(
            lesson_number__gt=current_lesson.lesson_number,
            status='published'
        ).order_by('lesson_number').first()
    except Exception:
        return None


def convert_sections_to_html(sections):
    """Convert markdown content in sections to HTML"""
    for section in sections:
        section.content_html = markdown(section.content)
    return sections


def prepare_lesson_detail_data(lesson):
    """Prepare lesson detail page data"""
    sections = lesson.sections.all()
    tips = lesson.tips.all()
    
    # Convert Markdown content to HTML
    sections = convert_sections_to_html(sections)
    
    return {
        'lesson': lesson,
        'sections': sections,
        'tips': tips,
    }


def get_user_lesson_progress(user, lesson):
    """Get user's progress for specific lesson
    
    Args:
        user: User object
        lesson: Lesson object
    
    Returns:
        UserLessonProgress object or None
    """
    try:
        return UserLessonProgress.objects.get(user=user, lesson=lesson)
    except UserLessonProgress.DoesNotExist:
        return None


def get_or_create_user_lesson_progress(user, lesson):
    """Get or create user lesson progress record
    
    Args:
        user: User object
        lesson: Lesson object
    
    Returns:
        UserLessonProgress object
    """
    progress, created = UserLessonProgress.objects.get_or_create(
        user=user,
        lesson=lesson,
        defaults={'status': 'not_started'}
    )
    return progress


def get_user_lessons_with_progress(user):
    """Get all published lessons with user's progress status
    
    Args:
        user: User object
    
    Returns:
        list: List of dictionaries containing lesson and progress information
    """
    lessons = get_published_lessons()
    lessons_with_progress = []
    
    for lesson in lessons:
        progress = get_user_lesson_progress(user, lesson)
        lessons_with_progress.append({
            'lesson': lesson,
            'progress': progress,
            'status': progress.status if progress else 'not_started',
        })
    
    return lessons_with_progress


def get_user_lesson_statistics(user):
    """Get user's lesson statistics
    
    Returns:
        dict: {
            'total_lessons': int,        # Total lesson count
            'completed_count': int,      # Completed count
            'in_progress_count': int,    # In progress count
            'not_started_count': int,    # Not started count
            'completion_percentage': float,  # Completion percentage
        }
    """
    total_lessons = get_published_lessons().count()
    user_progresses = UserLessonProgress.objects.filter(user=user)
    
    completed_count = user_progresses.filter(status='completed').count()
    in_progress_count = user_progresses.filter(status='in_progress').count()
    not_started_count = total_lessons - completed_count - in_progress_count
    
    completion_percentage = (completed_count / total_lessons * 100) if total_lessons > 0 else 0
    
    return {
        'total_lessons': total_lessons,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'not_started_count': not_started_count,
        'completion_percentage': completion_percentage,
    }


def reward_lesson_completion(user, lesson):
    """Reward user for completing lesson (add virtual coins to wallet)
    
    Args:
        user: User object
        lesson: Lesson object
    
    Returns:
        bool: Whether reward was successful
    """
    if lesson.coin_reward <= 0:
        return False
    
    try:
        from wallet.models import Wallet, WalletTransaction
        
        # Get user's first wallet, skip reward if none exists
        user_wallet = Wallet.objects.filter(user=user).first()
        if user_wallet:
            WalletTransaction.objects.create(
                wallet=user_wallet,
                transaction_type='income',
                amount=lesson.coin_reward,
                description=f'Lesson completion reward: {lesson.title}',
                date=timezone.now().date()
            )
            return True
        else:
            # If no wallet, try to create default wallet
            default_wallet = Wallet.objects.create(
                user=user,
                coin_name='Coin',
                coin_icon='⭐',
                child_name=''
            )
            WalletTransaction.objects.create(
                wallet=default_wallet,
                transaction_type='income',
                amount=lesson.coin_reward,
                description=f'Lesson completion reward: {lesson.title}',
                date=timezone.now().date()
            )
            return True
    except Exception:
        # If wallet system unavailable, fail silently
        return False

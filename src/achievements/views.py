from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Achievement, UserAchievement
from .utils import get_user_achievements


@login_required
def achievement_list_view(request):
    """Achievement list page"""
    user_achievements_data = get_user_achievements(request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        unlocked_filtered = [
            a for a in user_achievements_data['unlocked']
            if search_query.lower() in a.name.lower() or search_query.lower() in a.description.lower()
        ]
        locked_filtered = [
            a for a in user_achievements_data['locked']
            if search_query.lower() in a.name.lower() or search_query.lower() in a.description.lower()
        ]
        user_achievements_data['unlocked'] = unlocked_filtered
        user_achievements_data['locked'] = locked_filtered
    
    # Filter by type
    type_filter = request.GET.get('type', '')
    if type_filter:
        unlocked_filtered = [a for a in user_achievements_data['unlocked'] if a.achievement_type == type_filter]
        locked_filtered = [a for a in user_achievements_data['locked'] if a.achievement_type == type_filter]
        user_achievements_data['unlocked'] = unlocked_filtered
        user_achievements_data['locked'] = locked_filtered
    
    # Get achievement type list (for filtering)
    achievement_types = Achievement.ACHIEVEMENT_TYPES
    
    context = {
        **user_achievements_data,
        'search_query': search_query,
        'type_filter': type_filter,
        'achievement_types': achievement_types,
        'progress_percentage': (user_achievements_data['unlocked_count'] / user_achievements_data['total'] * 100) if user_achievements_data['total'] > 0 else 0,
    }
    return render(request, 'achievements/achievement_list.html', context)


@login_required
def achievement_detail_view(request, pk):
    """Achievement detail page"""
    achievement = get_object_or_404(Achievement, pk=pk, is_active=True)
    
    # Check if user has unlocked this achievement
    user_achievement = UserAchievement.objects.filter(
        user=request.user,
        achievement=achievement
    ).first()
    
    is_unlocked = user_achievement is not None
    
    context = {
        'achievement': achievement,
        'user_achievement': user_achievement,
        'is_unlocked': is_unlocked,
    }
    return render(request, 'achievements/achievement_detail.html', context)


@login_required
def my_achievements_view(request):
    """My achievements page (only show unlocked)"""
    unlocked_achievements = Achievement.objects.filter(
        user_achievements__user=request.user,
        is_active=True
    ).order_by('-user_achievements__unlocked_at').distinct()
    
    context = {
        'unlocked_achievements': unlocked_achievements,
        'total_count': unlocked_achievements.count(),
    }
    return render(request, 'achievements/my_achievements.html', context)


@login_required
@require_http_methods(["GET"])
def get_unnotified_achievements_view(request):
    """Get unnotified achievements (API endpoint)"""
    unnotified_achievements = UserAchievement.objects.filter(
        user=request.user,
        is_notified=False
    ).select_related('achievement').order_by('-unlocked_at')[:5]
    
    achievements_data = []
    for user_achievement in unnotified_achievements:
        achievements_data.append({
            'id': user_achievement.id,
            'achievement_id': user_achievement.achievement.id,
            'name': user_achievement.achievement.name,
            'description': user_achievement.achievement.description,
            'icon': user_achievement.achievement.icon,
            'color': user_achievement.achievement.color,
            'coin_reward': float(user_achievement.achievement.coin_reward),
            'unlocked_at': user_achievement.unlocked_at.isoformat(),
        })
    
    return JsonResponse({
        'success': True,
        'achievements': achievements_data,
        'count': len(achievements_data)
    })


@login_required
@require_http_methods(["POST"])
def mark_achievement_notified_view(request, pk):
    """Mark achievement as notified"""
    try:
        user_achievement = UserAchievement.objects.get(
            pk=pk,
            user=request.user
        )
        user_achievement.is_notified = True
        user_achievement.save()
        return JsonResponse({'success': True, 'message': 'Achievement marked as notified'})
    except UserAchievement.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Achievement not found'}, status=404)


from django import template
from ..models import Lesson

register = template.Library()


@register.simple_tag
def get_all_lessons_for_menu():
    """Get all published lessons for navigation menu"""
    # Directly query from model to ensure we get all published lessons
    lessons = Lesson.objects.filter(status='published').order_by('lesson_number')
    return lessons


@register.filter
def render_icon(icon_name):
    """Render Remix Icon from icon name (cute icon library)"""
    if not icon_name:
        return ''
    # If it's already an emoji or HTML, return as is (for backward compatibility)
    if icon_name.startswith('<') or len(icon_name) > 30:
        return icon_name
    
    # Map Bootstrap icon names to Remix icon names (using correct Remix Icon names)
    icon_mapping = {
        # Main lesson icons
        'piggy-bank': 'ri-piggy-bank-line',
        'briefcase': 'ri-briefcase-line',
        'safe-fill': 'ri-safe-line',
        'target': 'ri-target-line',
        'graph-up': 'ri-line-chart-line',
        'heart-fill': 'ri-heart-line',
        'cart': 'ri-shopping-cart-line',
        'bank': 'ri-bank-line',
        'trending-up': 'ri-stock-line',
        'credit-card-2-front': 'ri-bank-card-line',
        
        # Section icons
        'rocket-takeoff': 'ri-rocket-line',
        'lightbulb': 'ri-lightbulb-line',
        'journal-plus': 'ri-book-open-line',
        'star-fill': 'ri-star-line',
        'briefcase-fill': 'ri-briefcase-line',
        'bullseye': 'ri-focus-line',
        'clipboard-check': 'ri-clipboard-check-line',
        'chat-dots': 'ri-chat-3-line',
        'safe2': 'ri-safe-line',
        'palette': 'ri-palette-line',
        'house': 'ri-home-line',
        'controller': 'ri-gamepad-line',
        'lightbulb-fill': 'ri-lightbulb-flash-line',
        'shuffle': 'ri-shuffle-line',
        'question-circle': 'ri-question-line',
        'pie-chart': 'ri-pie-chart-line',
        'cash-coin': 'ri-coin-line',
        'bucket': 'ri-archive-line',
        'journal-text': 'ri-file-text-line',
        'chat-quote': 'ri-chat-quote-line',
        'heart': 'ri-heart-line',
        'gift': 'ri-gift-line',
        'search': 'ri-search-line',
        'cup-straw': 'ri-cup-line',
        'scale': 'ri-scales-line',
        'seedling': 'ri-plant-line',
        'exclamation-triangle': 'ri-error-warning-line',
        'clock': 'ri-time-line',
        'tv': 'ri-tv-line',
        'question-circle-fill': 'ri-question-answer-line',
        '1-circle': 'ri-number-1',
        'cash-stack': 'ri-money-dollar-circle-line',
        'building': 'ri-building-line',
        'credit-card': 'ri-bank-card-line',
        'calculator': 'ri-calculator-line',
        'graph-up-arrow': 'ri-bar-chart-line',
        'egg': 'ri-egg-line',
        'bookshelf': 'ri-book-line',
        'mask': 'ri-emotion-line',
        'check-circle': 'ri-checkbox-circle-line',
        'shield-check': 'ri-shield-check-line',
        'currency-dollar': 'ri-money-dollar-box-line',
        'eye': 'ri-eye-line',
        'flag': 'ri-flag-line',
        'pencil': 'ri-pencil-line',
        'trophy': 'ri-trophy-line',
        'clock-history': 'ri-history-line',
    }
    
    # Get Remix Icon class name
    if icon_name in icon_mapping:
        remix_icon = icon_mapping[icon_name]
    else:
        # Try to auto-convert format
        # Remove common suffixes
        clean_name = icon_name.replace('-fill', '').replace('-2-front', '').replace('-front', '')
        # Convert to Remix format (ri-{name}-line)
        remix_icon = f'ri-{clean_name}-line'
    
    # Return icon with styling
    # Note: Cover icons will be set to white in CSS via .lesson-default-cover-icon class
    # Use default color here, let CSS control the cover icon color
    return f'<i class="{remix_icon} lesson-icon"></i>'







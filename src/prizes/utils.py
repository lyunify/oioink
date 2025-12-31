from django.db.models import Q
from .models import Prize
from wallet.utils import get_user_wallets_summary


def get_available_prizes(category=None, featured=False):
    """Get list of available prizes
    
    Args:
        category: Prize category (optional)
        featured: Whether to return only featured prizes
    
    Returns:
        QuerySet: List of available prizes
    """
    prizes = Prize.objects.filter(status='active')
    
    if category:
        prizes = prizes.filter(category=category)
    
    if featured:
        prizes = prizes.filter(is_featured=True)
    
    # Filter out unavailable prizes (based on time and stock)
    available_prizes = []
    for prize in prizes:
        if prize.is_available:
            available_prizes.append(prize)
    
    return available_prizes


def get_user_prize_history(user):
    """Get user's prize redemption history (via wallet transaction records)
    
    Args:
        user: User object
    
    Returns:
        list: List of prize redemption records (from WalletTransaction)
    """
    try:
        from wallet.models import WalletTransaction
        from django.utils import timezone
        
        # Find all transactions containing "Prize redemption"
        transactions = WalletTransaction.objects.filter(
            wallet__user=user,
            transaction_type='expense',
            description__icontains='Prize redemption:'
        ).order_by('-date', '-created_at')
        
        return transactions
    except Exception:
        return []


def search_prizes(query, category=None):
    """Search prizes
    
    Args:
        query: Search keyword
        category: Prize category (optional)
    
    Returns:
        QuerySet: List of matching prizes
    """
    prizes = Prize.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )
    
    if category:
        prizes = prizes.filter(category=category)
    
    return prizes.filter(status='active')


def get_featured_prizes(limit=6):
    """Get featured prizes
    
    Args:
        limit: Return count limit
    
    Returns:
        list: List of featured prizes
    """
    return get_available_prizes(featured=True)[:limit]





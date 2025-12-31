from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Prize
from .utils import get_available_prizes, get_user_prize_history, search_prizes, get_featured_prizes
from wallet.utils import get_user_wallets_summary


def prize_list_view(request):
    """Prize list page"""
    # Get filter parameters
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    featured_only = request.GET.get('featured', '') == 'true'
    
    # Get prizes
    if search_query:
        prizes = search_prizes(search_query, category_filter if category_filter else None)
    elif featured_only:
        prizes = get_available_prizes(category=category_filter if category_filter else None, featured=True)
    else:
        prizes = get_available_prizes(category=category_filter if category_filter else None)
    
    # Get user balance (if logged in)
    user_balance = None
    if request.user.is_authenticated:
        wallet_summary = get_user_wallets_summary(request.user)
        user_balance = wallet_summary.get('total_balance', 0)
    
    # Get category options
    categories = Prize.PRIZE_CATEGORIES
    
    # Get featured prizes (for sidebar or recommendation area)
    featured_prizes = get_featured_prizes(limit=6)
    
    context = {
        'prizes': prizes,
        'categories': categories,
        'category_filter': category_filter,
        'search_query': search_query,
        'featured_only': featured_only,
        'user_balance': user_balance,
        'featured_prizes': featured_prizes,
    }
    return render(request, 'prizes/prize_list.html', context)


def prize_detail_view(request, pk):
    """Prize detail page"""
    from wallet.models import Wallet
    
    prize = get_object_or_404(Prize, pk=pk)
    
    # Get user balance and whether can redeem
    user_balance = None
    can_redeem = False
    redeem_message = ""
    wallet_count = 0
    
    if request.user.is_authenticated:
        wallet_summary = get_user_wallets_summary(request.user)
        user_balance = wallet_summary.get('total_balance', 0)
        can_redeem, redeem_message = prize.can_be_redeemed_by(request.user)
        wallet_count = Wallet.objects.filter(user=request.user).count()
    
    context = {
        'prize': prize,
        'user_balance': user_balance,
        'can_redeem': can_redeem,
        'redeem_message': redeem_message,
        'wallet_count': wallet_count,
    }
    return render(request, 'prizes/prize_detail.html', context)


@login_required
def prize_redeem_view(request, pk):
    """Redeem prize - supports wallet selection"""
    from .forms import PrizeRedeemForm
    from wallet.models import Wallet
    
    prize = get_object_or_404(Prize, pk=pk)
    
    # Check if can redeem
    can_redeem, message = prize.can_be_redeemed_by(request.user)
    if not can_redeem:
        messages.error(request, f"Cannot redeem prize: {message}")
        return redirect('prizes:prize_detail', pk=pk)
    
    # Check if user has wallets
    user_wallets = Wallet.objects.filter(user=request.user)
    if not user_wallets.exists():
        messages.error(request, "No wallet found. Please create a wallet first.")
        return redirect('prizes:prize_detail', pk=pk)
    
    # Handle form submission
    if request.method == 'POST':
        form = PrizeRedeemForm(request.POST, user=request.user, prize_cost=prize.coin_cost)
        
        if form.is_valid():
            wallet = form.cleaned_data['wallet']
            
            # Check wallet balance again
            from wallet.utils import calculate_wallet_balance
            from decimal import Decimal
            wallet_balance = calculate_wallet_balance(wallet)
            
            if wallet_balance < Decimal(str(prize.coin_cost)):
                messages.error(request, f"Insufficient balance in selected wallet. You have {wallet_balance} coins, but need {prize.coin_cost} coins.")
                return redirect('prizes:prize_detail', pk=pk)
            
            # Redeem prize
            success, message = prize.redeem_for_user(request.user, wallet)
            
            if success:
                messages.success(request, f"Congratulations! You successfully redeemed '{prize.name}'! {message}")
                return redirect('prizes:my_prizes')
            else:
                messages.error(request, f"Failed to redeem prize: {message}")
                return redirect('prizes:prize_detail', pk=pk)
    else:
        # GET request, show wallet selection form
        form = PrizeRedeemForm(user=request.user, prize_cost=prize.coin_cost)
        
        # If only one available wallet, use it directly
        if form.fields['wallet'].queryset.count() == 1:
            wallet = form.fields['wallet'].queryset.first()
            success, message = prize.redeem_for_user(request.user, wallet)
            
            if success:
                messages.success(request, f"Congratulations! You successfully redeemed '{prize.name}'! {message}")
                return redirect('prizes:my_prizes')
            else:
                messages.error(request, f"Failed to redeem prize: {message}")
                return redirect('prizes:prize_detail', pk=pk)
    
    # Get wallet balance information
    from wallet.utils import get_user_wallets_summary, calculate_wallet_balance
    wallet_summary = get_user_wallets_summary(request.user)
    wallets_with_balance = []
    
    for wallet_item in wallet_summary['wallets']:
        wallet = wallet_item['wallet']
        balance = wallet_item['balance']
        # Only show wallets with sufficient balance, or if none sufficient, show all wallets
        if balance >= prize.coin_cost or form.fields['wallet'].queryset.count() == 0:
            wallets_with_balance.append({
                'wallet': wallet,
                'balance': balance,
                'is_sufficient': balance >= prize.coin_cost,
            })
    
    # Show wallet selection form
    context = {
        'prize': prize,
        'form': form,
        'wallets_with_balance': wallets_with_balance,
    }
    return render(request, 'prizes/prize_redeem.html', context)


@login_required
def my_prizes_view(request):
    """My prizes page (show redemption history)"""
    # Get user's redemption history (via wallet transaction records)
    prize_history = get_user_prize_history(request.user)
    
    # Get user balance
    wallet_summary = get_user_wallets_summary(request.user)
    user_balance = wallet_summary.get('total_balance', 0)
    
    context = {
        'prize_history': prize_history,
        'user_balance': user_balance,
    }
    return render(request, 'prizes/my_prizes.html', context)


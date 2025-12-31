from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q, Count
from django.utils import timezone
from datetime import timedelta

from .models import Wallet, WalletTransaction
from .forms import WalletForm, WalletTransactionForm
from .utils import calculate_wallet_balance, get_wallet_statistics, get_user_wallets_summary


# Wallet views ==================================================================

@login_required
def wallet_list_view(request):
    """Wallet list page"""
    wallets = Wallet.objects.filter(user=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        wallets = wallets.filter(
            Q(child_name__icontains=search_query) |
            Q(coin_name__icontains=search_query)
        )
    
    # Filter by child
    child_filter = request.GET.get('child', '')
    if child_filter:
        wallets = wallets.filter(child_name=child_filter)
    
    # Filter by mode
    mode_filter = request.GET.get('mode', '')
    if mode_filter == 'practice':
        wallets = wallets.filter(is_practice_mode=True)
    elif mode_filter == 'real':
        wallets = wallets.filter(is_practice_mode=False)
    
    # Calculate balance for each wallet
    wallets_with_balance = []
    for wallet in wallets:
        balance = calculate_wallet_balance(wallet)
        wallets_with_balance.append({
            'wallet': wallet,
            'balance': balance,
        })
    
    # Get all child names (for filtering)
    child_names = Wallet.objects.filter(user=request.user).values_list('child_name', flat=True).distinct()
    child_names = [name for name in child_names if name]  # Filter empty values
    
    # Calculate total balance
    total_balance = sum(w['balance'] for w in wallets_with_balance)
    
    # Calculate balances separately for practice mode and real mode
    practice_balance = sum(w['balance'] for w in wallets_with_balance if w['wallet'].is_practice_mode)
    real_balance = sum(w['balance'] for w in wallets_with_balance if not w['wallet'].is_practice_mode)
    practice_count = sum(1 for w in wallets_with_balance if w['wallet'].is_practice_mode)
    real_count = sum(1 for w in wallets_with_balance if not w['wallet'].is_practice_mode)
    
    context = {
        'wallets_with_balance': wallets_with_balance,
        'total_balance': total_balance,
        'practice_balance': practice_balance,
        'real_balance': real_balance,
        'practice_count': practice_count,
        'real_count': real_count,
        'child_names': child_names,
        'search_query': search_query,
        'child_filter': child_filter,
        'mode_filter': mode_filter,
    }
    return render(request, 'wallet/wallet_list.html', context)


@login_required
def wallet_detail_view(request, pk):
    """Wallet detail page"""
    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
    balance = calculate_wallet_balance(wallet)
    statistics = get_wallet_statistics(wallet)
    
    # Get recent transactions
    recent_transactions = WalletTransaction.objects.filter(wallet=wallet)[:10]
    
    context = {
        'wallet': wallet,
        'balance': balance,
        'statistics': statistics,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'wallet/wallet_detail.html', context)


@login_required
def wallet_create_view(request):
    """Create wallet"""
    if request.method == 'POST':
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            wallet.save()
            
            # If practice mode and has preset initial balance, create initial income transaction
            if wallet.is_practice_mode and wallet.practice_initial_balance and wallet.practice_initial_balance > 0:
                WalletTransaction.objects.create(
                    wallet=wallet,
                    transaction_type='income',
                    amount=wallet.practice_initial_balance,
                    description='Practice mode initial balance',
                    date=timezone.now().date()
                )
            
            mode_text = "Practice Mode " if wallet.is_practice_mode else ""
            messages.success(request, f'{mode_text}Wallet "{wallet.coin_name}" created successfully!')
            return redirect('wallet:wallet_list')
    else:
        form = WalletForm()
    
    context = {
        'form': form,
        'title': 'Create New Wallet',
    }
    return render(request, 'wallet/wallet_form.html', context)


@login_required
def wallet_edit_view(request, pk):
    """Edit wallet"""
    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = WalletForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            return redirect('wallet:wallet_detail', pk=wallet.pk)
    else:
        form = WalletForm(instance=wallet)
    
    context = {
        'form': form,
        'wallet': wallet,
        'title': 'Edit Wallet',
    }
    return render(request, 'wallet/wallet_form.html', context)


@login_required
def wallet_delete_view(request, pk):
    """Delete wallet"""
    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
    balance = calculate_wallet_balance(wallet)
    
    if request.method == 'POST':
        wallet.delete()
        return redirect('wallet:wallet_list')
    
    context = {
        'wallet': wallet,
        'balance': balance,
    }
    return render(request, 'wallet/wallet_confirm_delete.html', context)


@login_required
def wallet_dashboard_view(request):
    """Wallet statistics dashboard"""
    wallets = Wallet.objects.filter(user=request.user)
    
    # Get summary of all wallets
    summary = get_user_wallets_summary(request.user)
    
    # This month statistics
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    this_month_transactions = WalletTransaction.objects.filter(
        wallet__user=request.user,
        date__gte=first_day_of_month
    )
    this_month_income = this_month_transactions.filter(
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    this_month_expense = this_month_transactions.filter(
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Last 7 days statistics
    seven_days_ago = today - timedelta(days=7)
    recent_transactions = WalletTransaction.objects.filter(
        wallet__user=request.user,
        date__gte=seven_days_ago
    )
    recent_income = recent_transactions.filter(
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    recent_expense = recent_transactions.filter(
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Statistics by child
    child_stats = WalletTransaction.objects.filter(
        wallet__user=request.user
    ).exclude(wallet__child_name='').values('wallet__child_name').annotate(
        total_income=Sum('amount', filter=Q(transaction_type='income')),
        total_expense=Sum('amount', filter=Q(transaction_type='expense')),
        count=Count('id')
    ).order_by('-total_income')
    
    context = {
        'total_wallets': summary['total_wallets'],
        'total_balance': summary['total_balance'],
        'this_month_income': this_month_income,
        'this_month_expense': this_month_expense,
        'recent_income': recent_income,
        'recent_expense': recent_expense,
        'child_stats': child_stats,
        'total_transactions': WalletTransaction.objects.filter(wallet__user=request.user).count(),
    }
    return render(request, 'wallet/wallet_dashboard.html', context)


# Wallet Transaction views ==================================================================

@login_required
def transaction_list_view(request, wallet_pk):
    """Transaction list page"""
    wallet = get_object_or_404(Wallet, pk=wallet_pk, user=request.user)
    transactions = WalletTransaction.objects.filter(wallet=wallet)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        transactions = transactions.filter(description__icontains=search_query)
    
    # Filter by transaction type
    type_filter = request.GET.get('type', '')
    if type_filter:
        transactions = transactions.filter(transaction_type=type_filter)
    
    # Date range filter
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    
    # Statistics
    total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'wallet': wallet,
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'search_query': search_query,
        'type_filter': type_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'wallet/transaction_list.html', context)


@login_required
def transaction_detail_view(request, pk):
    """Transaction detail page"""
    transaction = get_object_or_404(WalletTransaction, pk=pk, wallet__user=request.user)
    context = {
        'transaction': transaction,
    }
    return render(request, 'wallet/transaction_detail.html', context)


@login_required
def transaction_create_view(request, wallet_pk):
    """Create transaction record"""
    wallet = get_object_or_404(Wallet, pk=wallet_pk, user=request.user)
    
    if request.method == 'POST':
        form = WalletTransactionForm(request.POST, wallet=wallet)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.wallet = wallet
            transaction.save()
            return redirect('wallet:transaction_list', wallet_pk=wallet.pk)
    else:
        form = WalletTransactionForm(wallet=wallet)
    
    context = {
        'form': form,
        'wallet': wallet,
        'title': 'Add New Transaction',
    }
    return render(request, 'wallet/transaction_form.html', context)


@login_required
def transaction_edit_view(request, pk):
    """Edit transaction record"""
    transaction = get_object_or_404(WalletTransaction, pk=pk, wallet__user=request.user)
    
    if request.method == 'POST':
        form = WalletTransactionForm(request.POST, instance=transaction, wallet=transaction.wallet)
        if form.is_valid():
            form.save()
            return redirect('wallet:transaction_detail', pk=transaction.pk)
    else:
        form = WalletTransactionForm(instance=transaction, wallet=transaction.wallet)
    
    context = {
        'form': form,
        'transaction': transaction,
        'wallet': transaction.wallet,
        'title': 'Edit Transaction',
    }
    return render(request, 'wallet/transaction_form.html', context)


@login_required
def transaction_delete_view(request, pk):
    """Delete transaction record"""
    transaction = get_object_or_404(WalletTransaction, pk=pk, wallet__user=request.user)
    wallet_pk = transaction.wallet.pk
    
    if request.method == 'POST':
        transaction.delete()
        return redirect('wallet:transaction_list', wallet_pk=wallet_pk)
    
    context = {
        'transaction': transaction,
    }
    return render(request, 'wallet/transaction_confirm_delete.html', context)


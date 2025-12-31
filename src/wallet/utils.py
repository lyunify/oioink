from decimal import Decimal
from django.db.models import Sum, Q
from .models import Wallet, WalletTransaction


def calculate_wallet_balance(wallet):
    """Calculate wallet balance"""
    income = WalletTransaction.objects.filter(
        wallet=wallet,
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    expense = WalletTransaction.objects.filter(
        wallet=wallet,
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    return income - expense


def get_wallet_statistics(wallet):
    """Get wallet statistics"""
    transactions = WalletTransaction.objects.filter(wallet=wallet)
    
    total_income = transactions.filter(transaction_type='income').aggregate(
        Sum('amount')
    )['amount__sum'] or Decimal('0.00')
    
    total_expense = transactions.filter(transaction_type='expense').aggregate(
        Sum('amount')
    )['amount__sum'] or Decimal('0.00')
    
    balance = calculate_wallet_balance(wallet)
    
    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'transaction_count': transactions.count(),
    }


def get_user_wallets_summary(user):
    """Get summary information for all user wallets"""
    wallets = Wallet.objects.filter(user=user)
    
    summary = {
        'total_wallets': wallets.count(),
        'wallets': [],
        'total_balance': Decimal('0.00'),
    }
    
    for wallet in wallets:
        balance = calculate_wallet_balance(wallet)
        summary['wallets'].append({
            'wallet': wallet,
            'balance': balance,
        })
        summary['total_balance'] += balance
    
    return summary





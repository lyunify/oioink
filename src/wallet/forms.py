from django import forms
from .models import Wallet, WalletTransaction


class WalletForm(forms.ModelForm):
    """Wallet form"""
    class Meta:
        model = Wallet
        fields = ['child_name', 'coin_name', 'coin_icon', 'is_practice_mode', 'practice_initial_balance']
        widgets = {
            'child_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Child name (optional)'
            }),
            'coin_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Star Coin, Learning Coin'
            }),
            'coin_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., ⭐, 🎯, 💎',
                'maxlength': '10'
            }),
            'is_practice_mode': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'practice_initial_balance': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Initial balance (optional)'
            }),
        }
        labels = {
            'child_name': 'Child Name',
            'coin_name': 'Coin Name',
            'coin_icon': 'Coin Icon',
            'is_practice_mode': 'Practice Mode',
            'practice_initial_balance': 'Initial Balance (Practice Mode)',
        }
        help_texts = {
            'child_name': 'Optional: Name of the child this wallet belongs to',
            'coin_name': 'Name of the virtual coin',
            'coin_icon': 'Emoji icon for the coin (max 10 characters)',
        }


class WalletTransactionForm(forms.ModelForm):
    """Wallet transaction form"""
    class Meta:
        model = WalletTransaction
        fields = ['transaction_type', 'amount', 'description', 'date']
        widgets = {
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What is this transaction for?'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
        labels = {
            'transaction_type': 'Transaction Type',
            'amount': 'Amount',
            'description': 'Description',
            'date': 'Date',
        }
    
    def __init__(self, *args, **kwargs):
        wallet = kwargs.pop('wallet', None)
        super().__init__(*args, **kwargs)
        if wallet:
            self.wallet = wallet


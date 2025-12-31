from django import forms
from wallet.models import Wallet


class PrizeRedeemForm(forms.Form):
    """Prize redemption form - select wallet"""
    wallet = forms.ModelChoiceField(
        queryset=Wallet.objects.none(),
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Select Wallet',
        help_text='Choose which wallet to use for this redemption',
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        prize_cost = kwargs.pop('prize_cost', 0)
        super().__init__(*args, **kwargs)
        
        if user:
            # Only show wallets with sufficient balance
            from wallet.utils import calculate_wallet_balance
            from decimal import Decimal
            
            wallets = Wallet.objects.filter(user=user)
            available_wallets = []
            
            for wallet in wallets:
                balance = calculate_wallet_balance(wallet)
                if balance >= Decimal(str(prize_cost)):
                    available_wallets.append(wallet)
            
            self.fields['wallet'].queryset = Wallet.objects.filter(
                id__in=[w.id for w in available_wallets]
            )
            
            # If no available wallets, show all wallets (let user see insufficient balance message)
            if not available_wallets:
                self.fields['wallet'].queryset = wallets

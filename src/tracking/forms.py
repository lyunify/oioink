from django import forms
from .models import Spending, SpendingCategory, Saving, SavingGoal


class SavingGoalForm(forms.ModelForm):
    """Saving goal form"""
    class Meta:
        model = SavingGoal
        fields = ['goal_name', 'target_amount', 'child_name', 'deadline', 'icon', 'color', 'description']
        widgets = {
            'goal_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., New Bike, Toy, etc.'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'child_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Child name (optional)'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '🎯', 'maxlength': '10'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional details about this goal (optional)'}),
        }
        labels = {
            'goal_name': 'Goal Name',
            'target_amount': 'Target Amount',
            'child_name': 'Child Name',
            'deadline': 'Deadline',
            'icon': 'Icon (emoji)',
            'color': 'Color',
            'description': 'Description',
        }


class SpendingForm(forms.ModelForm):
    """Spending record form"""
    custom_category_name = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter custom category name',
            'id': 'id_custom_category_name',
        }),
        label='Custom Category Name',
        help_text='Enter a custom category name when "Other" is selected'
    )
    
    class Meta:
        model = Spending
        fields = ['category', 'amount', 'description', 'child_name', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What did you spend on?'}),
            'child_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Child name (optional)'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
        }
        labels = {
            'category': 'Category',
            'amount': 'Amount',
            'description': 'Description',
            'child_name': 'Child Name',
            'date': 'Date',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = SpendingCategory.objects.all().order_by('name')
        self.fields['category'].required = False
        self.fields['category'].empty_label = '---------'
        
        # Default category list (non-custom categories)
        default_categories = ['Clothing', 'Video', 'Electronics', 'School Supplies', 'Games', 
                             'Food', 'Transportation', 'Sports', 'Gifts', 'Other']
        
        # If editing existing record
        if self.instance and self.instance.pk:
            if self.instance.category:
                # If category is "Other" or not in default category list (means it's a custom category)
                if self.instance.category.name == 'Other' or self.instance.category.name not in default_categories:
                    # Show custom input field and pre-fill category name (if custom category)
                    self.fields['custom_category_name'].widget.attrs['style'] = 'display: block;'
                    if self.instance.category.name != 'Other':
                        # Pre-fill custom category name
                        self.fields['custom_category_name'].initial = self.instance.category.name
    
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        custom_category_name = cleaned_data.get('custom_category_name', '').strip()
        
        # If category is empty, user selected Other, must fill custom category name
        if not category:
            if not custom_category_name:
                raise forms.ValidationError({
                    'custom_category_name': 'Please enter a custom category name when "Other" is selected.'
                })
        # If category selected but also filled custom category name, ignore custom category name
        elif custom_category_name:
            # If selected non-Other category but filled custom category name, clear custom category name
            if category.name != 'Other':
                cleaned_data['custom_category_name'] = ''
        
        return cleaned_data


class SavingForm(forms.ModelForm):
    """Savings record form"""
    class Meta:
        model = Saving
        fields = ['saving_goal', 'amount', 'description', 'child_name', 'date', 'goal']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What did you save?'}),
            'child_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Child name (optional)'}),
            'goal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What are you saving for? (optional, legacy)'}),
            'saving_goal': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'saving_goal': 'Saving Goal',
            'amount': 'Amount',
            'description': 'Description',
            'child_name': 'Child Name',
            'date': 'Date',
            'goal': 'Saving Goal (Legacy)',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # If user provided, only show that user's saving goals
        if self.user:
            self.fields['saving_goal'].queryset = SavingGoal.objects.filter(user=self.user).order_by('-created_at')
            self.fields['saving_goal'].required = False
            self.fields['saving_goal'].empty_label = 'No Goal (Optional)'


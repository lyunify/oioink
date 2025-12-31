from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count
from django.utils.safestring import mark_safe
from datetime import timedelta
from django.http import JsonResponse
import json

from .forms import ContactForm
from .utils import send_contact_form


def home_view(request, *args, **kwargs):
    context = {}
    return render(request, 'myhome/home.html', context)


def about_view(request, *args, **kwargs):
    context = {}
    return render(request, 'myhome/about.html', context)


def contact_view(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = {
                'email': form.cleaned_data['email'],
                'name': form.cleaned_data['name'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            context['sent_status'] = send_contact_form(request, contact)
        else:
            context['form'] = form
            context['sent_status'] = 0
            return render(request, 'myhome/contact.html', context)
    else:
        context['sent_status'] = 1
    return render(request, 'myhome/contact.html', context)


def terms_view(request, *args, **kwargs):
    context = {}
    return render(request, 'myhome/terms.html', context)


def privacy_view(request, *args, **kwargs):
    context = {}
    return render(request, 'myhome/privacy.html', context)


def news_view(request, *args, **kwargs):
    context = {}
    return render(request, 'myhome/news.html', context)


def about_miracles_view(request, *args, **kwargs):
    context = {}
    return render(request, 'myhome/about_miracles.html', context)


def faqs_view(request, *args, **kwargs):
    context = {}
    return render(request, 'myhome/faqs.html', context)


def support_view(request, *args, **kwargs):
    context = {}
    return render(request, 'myhome/support.html', context)


@login_required
def dashboard_view(request):
    """Unified colorful dashboard integrating all module data"""
    from wallet.models import Wallet, WalletTransaction
    from wallet.utils import get_user_wallets_summary
    from tracking.models import Spending, SpendingCategory, Saving, SavingGoal
    from lessons.models import Lesson
    
    user = request.user
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    seven_days_ago = today - timedelta(days=7)
    
    # ========== Wallet Data ==========
    wallet_summary = get_user_wallets_summary(user)
    this_month_wallet_income = WalletTransaction.objects.filter(
        wallet__user=user,
        transaction_type='income',
        date__gte=first_day_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    this_month_wallet_expense = WalletTransaction.objects.filter(
        wallet__user=user,
        transaction_type='expense',
        date__gte=first_day_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Distinguish between practice mode and real mode wallets
    practice_wallets = [w for w in wallet_summary['wallets'] if w['wallet'].is_practice_mode]
    real_wallets = [w for w in wallet_summary['wallets'] if not w['wallet'].is_practice_mode]
    from decimal import Decimal
    practice_balance = sum(Decimal(str(w['balance'])) for w in practice_wallets) if practice_wallets else Decimal('0.00')
    real_balance = sum(Decimal(str(w['balance'])) for w in real_wallets) if real_wallets else Decimal('0.00')
    
    # ========== Spending Data ==========
    spendings = Spending.objects.filter(user=user)
    this_month_spendings = spendings.filter(date__gte=first_day_of_month)
    this_month_spending_total = this_month_spendings.aggregate(Sum('amount'))['amount__sum'] or 0
    recent_spendings = spendings.filter(date__gte=seven_days_ago)
    recent_spending_total = recent_spendings.aggregate(Sum('amount'))['amount__sum'] or 0
    top_spending_categories = spendings.values('category__name', 'category__icon', 'category__color').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')[:5]
    
    # ========== Savings Data ==========
    savings = Saving.objects.filter(user=user)
    this_month_savings = savings.filter(date__gte=first_day_of_month)
    this_month_saving_total = this_month_savings.aggregate(Sum('amount'))['amount__sum'] or 0
    total_savings_amount = savings.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Savings goals
    saving_goals = SavingGoal.objects.filter(user=user).order_by('-created_at')[:6]
    total_goals = SavingGoal.objects.filter(user=user).count()
    completed_goals = sum(1 for goal in SavingGoal.objects.filter(user=user) if goal.is_completed)
    active_goals = total_goals - completed_goals
    
    # ========== Lesson Data ==========
    from lessons.utils import get_user_lesson_statistics
    published_lessons = Lesson.objects.filter(status='published').order_by('lesson_number')
    total_lessons = published_lessons.count()
    lesson_stats = get_user_lesson_statistics(user)
    
    # ========== Achievement Data ==========
    from achievements.utils import get_user_achievements
    from achievements.models import UserAchievement
    achievements_data = get_user_achievements(user)
    recent_achievements = UserAchievement.objects.filter(user=user).order_by('-unlocked_at')[:5]
    
    # ========== Chart Data - Wallet Income/Expense Trends ==========
    thirty_days_ago = today - timedelta(days=30)
    wallet_daily_data = WalletTransaction.objects.filter(
        wallet__user=user,
        date__gte=thirty_days_ago
    ).values('date', 'transaction_type').annotate(
        total=Sum('amount')
    ).order_by('date')
    
    wallet_chart_data = {
        'labels': [],
        'income': [],
        'expense': []
    }
    daily_totals = {}
    for item in wallet_daily_data:
        date_str = item['date'].strftime('%m/%d')
        if date_str not in daily_totals:
            daily_totals[date_str] = {'income': 0, 'expense': 0}
        if item['transaction_type'] == 'income':
            daily_totals[date_str]['income'] += float(item['total'])
        else:
            daily_totals[date_str]['expense'] += float(item['total'])
    
    for date_str in sorted(daily_totals.keys()):
        wallet_chart_data['labels'].append(date_str)
        wallet_chart_data['income'].append(daily_totals[date_str]['income'])
        wallet_chart_data['expense'].append(daily_totals[date_str]['expense'])
    
    # ========== Check if onboarding should be displayed ==========
    from accounts.models import Profile
    try:
        profile = Profile.objects.get(user=user)
        show_onboarding = not profile.onboarding_completed
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
        show_onboarding = True
    
    context = {
        # Wallet data
        'wallet_total_balance': wallet_summary['total_balance'],
        'wallet_total_count': wallet_summary['total_wallets'],
        'wallet_month_income': this_month_wallet_income,
        'wallet_month_expense': this_month_wallet_expense,
        'practice_wallets': practice_wallets,
        'real_wallets': real_wallets,
        'practice_balance': practice_balance,
        'real_balance': real_balance,
        'practice_count': len(practice_wallets),
        'real_count': len(real_wallets),
        
        # Spending data
        'spending_month_total': this_month_spending_total,
        'spending_recent_total': recent_spending_total,
        'spending_total_count': spendings.count(),
        'top_spending_categories': top_spending_categories,
        
        # Savings data
        'saving_month_total': this_month_saving_total,
        'saving_total_amount': total_savings_amount,
        'saving_total_count': savings.count(),
        'saving_goals': saving_goals,
        'saving_goals_total': total_goals,
        'saving_goals_completed': completed_goals,
        'saving_goals_active': active_goals,
        
        # Lesson data
        'lessons_total': total_lessons,
        'lessons_completed': lesson_stats['completed_count'],
        'lessons_in_progress': lesson_stats['in_progress_count'],
        'lessons_completion_percentage': lesson_stats['completion_percentage'],
        'recent_lessons': published_lessons[:5],
        
        # Achievement data
        'achievements_unlocked_count': achievements_data['unlocked_count'],
        'achievements_total': achievements_data['total'],
        'achievements_progress': (achievements_data['unlocked_count'] / achievements_data['total'] * 100) if achievements_data['total'] > 0 else 0,
        'recent_achievements': recent_achievements,
        
        # Chart data
        'wallet_chart_data_json': mark_safe(json.dumps(wallet_chart_data)),
        
        # Onboarding
        'show_onboarding': show_onboarding,
    }
    return render(request, 'myhome/dashboard.html', context)


@login_required
def complete_onboarding_view(request):
    """Mark onboarding as completed"""
    from accounts.models import Profile
    from django.views.decorators.csrf import csrf_exempt
    import json
    
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
            profile.onboarding_completed = True
            profile.save()
            return JsonResponse({'success': True, 'message': 'Onboarding completed!'})
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user, onboarding_completed=True)
            return JsonResponse({'success': True, 'message': 'Onboarding completed!'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

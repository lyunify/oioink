from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, Count
from django.utils import timezone
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
import json

from .models import Spending, SpendingCategory, Saving, SavingGoal
from .forms import SpendingForm, SavingForm, SavingGoalForm


# Spending views ==================================================================

@login_required
def spending_list_view(request):
    """Spending list page"""
    # Get all spending records for current user
    spendings = Spending.objects.filter(user=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        spendings = spendings.filter(
            Q(description__icontains=search_query) |
            Q(child_name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Filter by child
    child_filter = request.GET.get('child', '')
    if child_filter:
        spendings = spendings.filter(child_name=child_filter)
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        spendings = spendings.filter(category_id=category_filter)
    
    # Date range filter
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        spendings = spendings.filter(date__gte=date_from)
    if date_to:
        spendings = spendings.filter(date__lte=date_to)
    
    # Statistics
    total_amount = spendings.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get all categories and child names (for filtering)
    categories = SpendingCategory.objects.all().order_by('name')
    child_names = Spending.objects.filter(user=request.user).values_list('child_name', flat=True).distinct()
    child_names = [name for name in child_names if name]  # Filter empty values
    
    context = {
        'spendings': spendings,
        'total_amount': total_amount,
        'categories': categories,
        'child_names': child_names,
        'search_query': search_query,
        'child_filter': child_filter,
        'category_filter': category_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'tracking/spending_list.html', context)


@login_required
def spending_detail_view(request, pk):
    """Spending detail page"""
    spending = get_object_or_404(Spending, pk=pk, user=request.user)
    context = {
        'spending': spending,
    }
    return render(request, 'tracking/spending_detail.html', context)


@login_required
def spending_create_view(request):
    """Create spending record"""
    if request.method == 'POST':
        form = SpendingForm(request.POST)
        if form.is_valid():
            spending = form.save(commit=False)
            spending.user = request.user
            
            # Handle custom category
            custom_category_name = form.cleaned_data.get('custom_category_name', '').strip()
            # If custom category name is provided (user selected Other), create or get that category
            if custom_category_name:
                custom_category, created = SpendingCategory.objects.get_or_create(
                    name=custom_category_name,
                    defaults={
                        'icon': '📦',
                        'color': '#95A5A6',
                        'description': f'Custom category: {custom_category_name}'
                    }
                )
                spending.category = custom_category
            # If no category and no custom category name, this should not happen (should be blocked by validation)
            elif not spending.category:
                form.add_error('category', 'Please select a category or enter a custom category name.')
                context = {
                    'form': form,
                    'title': 'Add New Spending',
                }
                return render(request, 'tracking/spending_form.html', context)
            
            spending.save()
            return redirect('tracking:spending_list')
    else:
        form = SpendingForm()
    
    context = {
        'form': form,
        'title': 'Add New Spending',
    }
    return render(request, 'tracking/spending_form.html', context)


@login_required
def spending_edit_view(request, pk):
    """Edit spending record"""
    spending = get_object_or_404(Spending, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = SpendingForm(request.POST, instance=spending)
        if form.is_valid():
            spending = form.save(commit=False)
            
            # Handle custom category
            custom_category_name = form.cleaned_data.get('custom_category_name', '').strip()
            # If custom category name is provided (user selected Other), create or get that category
            if custom_category_name:
                custom_category, created = SpendingCategory.objects.get_or_create(
                    name=custom_category_name,
                    defaults={
                        'icon': '📦',
                        'color': '#95A5A6',
                        'description': f'Custom category: {custom_category_name}'
                    }
                )
                spending.category = custom_category
            
            spending.save()
            return redirect('tracking:spending_detail', pk=spending.pk)
    else:
        form = SpendingForm(instance=spending)
    
    context = {
        'form': form,
        'spending': spending,
        'title': 'Edit Spending',
    }
    return render(request, 'tracking/spending_form.html', context)


@login_required
def spending_delete_view(request, pk):
    """Delete spending record"""
    spending = get_object_or_404(Spending, pk=pk, user=request.user)
    
    if request.method == 'POST':
        spending.delete()
        return redirect('tracking:spending_list')
    
    context = {
        'spending': spending,
    }
    return render(request, 'tracking/spending_confirm_delete.html', context)


@login_required
def spending_dashboard_view(request):
    """Spending statistics dashboard"""
    # Get all spending records for current user
    spendings = Spending.objects.filter(user=request.user)
    
    # This month statistics
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    this_month_spendings = spendings.filter(date__gte=first_day_of_month)
    this_month_total = this_month_spendings.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Statistics by category
    category_stats = spendings.values('category__name', 'category__icon').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # Statistics by child
    child_stats = spendings.exclude(child_name='').values('child_name').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # Last 7 days statistics
    seven_days_ago = today - timedelta(days=7)
    recent_spendings = spendings.filter(date__gte=seven_days_ago)
    recent_total = recent_spendings.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Prepare chart data - by category (pie chart)
    category_chart_data = {
        'labels': [],
        'data': [],
        'colors': [],
        'icons': []
    }
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#38f9d7', '#fa709a', '#fee140']
    for idx, stat in enumerate(category_stats[:10]):  # Show up to 10 categories
        category_chart_data['labels'].append(stat.get('category__name', 'Uncategorized') or 'Uncategorized')
        category_chart_data['data'].append(float(stat['total']))
        category_chart_data['colors'].append(colors[idx % len(colors)])
        category_chart_data['icons'].append(stat.get('category__icon', '💰') or '💰')
    
    # Prepare chart data - last 30 days trend (line chart)
    thirty_days_ago = today - timedelta(days=30)
    daily_spendings = spendings.filter(date__gte=thirty_days_ago).values('date').annotate(
        total=Sum('amount')
    ).order_by('date')
    
    daily_chart_data = {
        'labels': [],
        'data': []
    }
    for item in daily_spendings:
        daily_chart_data['labels'].append(item['date'].strftime('%m/%d'))
        daily_chart_data['data'].append(float(item['total']))
    
    context = {
        'this_month_total': this_month_total,
        'recent_total': recent_total,
        'category_stats': category_stats,
        'child_stats': child_stats,
        'total_spendings': spendings.count(),
        'category_chart_data_json': mark_safe(json.dumps(category_chart_data)),
        'daily_chart_data_json': mark_safe(json.dumps(daily_chart_data)),
    }
    return render(request, 'tracking/spending_dashboard.html', context)


# Saving views ==================================================================

@login_required
def saving_list_view(request):
    """Savings list page"""
    # Get all savings records for current user
    savings = Saving.objects.filter(user=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        savings = savings.filter(
            Q(description__icontains=search_query) |
            Q(child_name__icontains=search_query) |
            Q(goal__icontains=search_query)
        )
    
    # Filter by child
    child_filter = request.GET.get('child', '')
    if child_filter:
        savings = savings.filter(child_name=child_filter)
    
    # Date range filter
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        savings = savings.filter(date__gte=date_from)
    if date_to:
        savings = savings.filter(date__lte=date_to)
    
    # Statistics
    total_amount = savings.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get all child names (for filtering)
    child_names = Saving.objects.filter(user=request.user).values_list('child_name', flat=True).distinct()
    child_names = [name for name in child_names if name]  # Filter empty values
    
    context = {
        'savings': savings,
        'total_amount': total_amount,
        'child_names': child_names,
        'search_query': search_query,
        'child_filter': child_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'tracking/saving_list.html', context)


@login_required
def saving_detail_view(request, pk):
    """Savings detail page"""
    saving = get_object_or_404(Saving, pk=pk, user=request.user)
    context = {
        'saving': saving,
    }
    return render(request, 'tracking/saving_detail.html', context)


@login_required
def saving_create_view(request):
    """Create savings record"""
    if request.method == 'POST':
        form = SavingForm(request.POST, user=request.user)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.user = request.user
            saving.save()
            return redirect('tracking:saving_list')
    else:
        form = SavingForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Add New Saving',
    }
    return render(request, 'tracking/saving_form.html', context)


@login_required
def saving_edit_view(request, pk):
    """Edit savings record"""
    saving = get_object_or_404(Saving, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = SavingForm(request.POST, instance=saving, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('tracking:saving_detail', pk=saving.pk)
    else:
        form = SavingForm(instance=saving, user=request.user)
    
    context = {
        'form': form,
        'saving': saving,
        'title': 'Edit Saving',
    }
    return render(request, 'tracking/saving_form.html', context)


@login_required
def saving_delete_view(request, pk):
    """Delete savings record"""
    saving = get_object_or_404(Saving, pk=pk, user=request.user)
    
    if request.method == 'POST':
        saving.delete()
        return redirect('tracking:saving_list')
    
    context = {
        'saving': saving,
    }
    return render(request, 'tracking/saving_confirm_delete.html', context)


@login_required
def saving_dashboard_view(request):
    """Savings statistics dashboard"""
    # Get all savings for current user
    savings = Saving.objects.filter(user=request.user)
    
    # This month statistics
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    this_month_savings = savings.filter(date__gte=first_day_of_month)
    this_month_total = this_month_savings.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Statistics by child
    child_stats = savings.exclude(child_name='').values('child_name').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # Last 7 days statistics
    seven_days_ago = today - timedelta(days=7)
    recent_savings = savings.filter(date__gte=seven_days_ago)
    recent_total = recent_savings.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Statistics by goal (Legacy)
    goal_stats = savings.exclude(goal='').values('goal').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # Get all savings goals
    saving_goals = SavingGoal.objects.filter(user=request.user).order_by('-created_at')[:6]
    total_goals = SavingGoal.objects.filter(user=request.user).count()
    completed_goals = sum(1 for goal in SavingGoal.objects.filter(user=request.user) if goal.is_completed)
    
    context = {
        'this_month_total': this_month_total,
        'recent_total': recent_total,
        'child_stats': child_stats,
        'goal_stats': goal_stats,
        'total_savings': savings.count(),
        'saving_goals': saving_goals,
        'total_goals': total_goals,
        'completed_goals': completed_goals,
    }
    return render(request, 'tracking/saving_dashboard.html', context)


# Saving Goal views ==================================================================

@login_required
def saving_goal_list_view(request):
    """Saving goals list page"""
    saving_goals = SavingGoal.objects.filter(user=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        saving_goals = saving_goals.filter(
            Q(goal_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(child_name__icontains=search_query)
        )
    
    # Filter by child
    child_filter = request.GET.get('child', '')
    if child_filter:
        saving_goals = saving_goals.filter(child_name=child_filter)
    
    # Get all child names (for filtering)
    child_names = SavingGoal.objects.filter(user=request.user).values_list('child_name', flat=True).distinct()
    child_names = [name for name in child_names if name]  # Filter empty values
    
    # Convert to list for filtering
    saving_goals_list = list(saving_goals)
    
    # Filter by completion status
    status_filter = request.GET.get('status', '')
    if status_filter == 'completed':
        saving_goals_list = [goal for goal in saving_goals_list if goal.is_completed]
    elif status_filter == 'in_progress':
        saving_goals_list = [goal for goal in saving_goals_list if not goal.is_completed]
    
    # Calculate total statistics
    total_goals = len(saving_goals_list)
    completed_goals = sum(1 for goal in saving_goals_list if goal.is_completed)
    total_target = sum(goal.target_amount for goal in saving_goals_list)
    total_current = sum(goal.current_amount for goal in saving_goals_list)
    
    context = {
        'saving_goals': saving_goals_list,
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'total_target': total_target,
        'total_current': total_current,
        'child_names': child_names,
        'search_query': search_query,
        'child_filter': child_filter,
        'status_filter': status_filter,
    }
    return render(request, 'tracking/saving_goal_list.html', context)


@login_required
def saving_goal_detail_view(request, pk):
    """Saving goal detail page"""
    saving_goal = get_object_or_404(SavingGoal, pk=pk, user=request.user)
    
    # Get related savings records
    related_savings = Saving.objects.filter(saving_goal=saving_goal).order_by('-date')[:10]
    
    context = {
        'saving_goal': saving_goal,
        'related_savings': related_savings,
    }
    return render(request, 'tracking/saving_goal_detail.html', context)


@login_required
def saving_goal_create_view(request):
    """Create saving goal"""
    if request.method == 'POST':
        form = SavingGoalForm(request.POST)
        if form.is_valid():
            saving_goal = form.save(commit=False)
            saving_goal.user = request.user
            saving_goal.save()
            # Trigger achievement check (handled automatically via signals)
            return redirect('tracking:saving_goal_detail', pk=saving_goal.pk)
    else:
        form = SavingGoalForm()
    
    context = {
        'form': form,
        'title': 'Create New Saving Goal',
    }
    return render(request, 'tracking/saving_goal_form.html', context)


@login_required
def saving_goal_edit_view(request, pk):
    """Edit saving goal"""
    saving_goal = get_object_or_404(SavingGoal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = SavingGoalForm(request.POST, instance=saving_goal)
        if form.is_valid():
            form.save()
            return redirect('tracking:saving_goal_detail', pk=saving_goal.pk)
    else:
        form = SavingGoalForm(instance=saving_goal)
    
    context = {
        'form': form,
        'saving_goal': saving_goal,
        'title': 'Edit Saving Goal',
    }
    return render(request, 'tracking/saving_goal_form.html', context)


@login_required
def saving_goal_delete_view(request, pk):
    """Delete saving goal"""
    saving_goal = get_object_or_404(SavingGoal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        saving_goal.delete()
        return redirect('tracking:saving_goal_list')
    
    context = {
        'saving_goal': saving_goal,
    }
    return render(request, 'tracking/saving_goal_confirm_delete.html', context)


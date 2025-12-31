from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Lesson, UserLessonProgress
from .utils import (
    get_published_lessons, 
    get_lesson_by_number, 
    prepare_lesson_detail_data,
    get_user_lesson_progress,
    get_or_create_user_lesson_progress,
    get_user_lessons_with_progress,
    get_user_lesson_statistics,
    get_next_lesson
)


# Lesson views ==================================================================

def lesson_list_view(request):
    """Lesson list page"""
    lessons = get_published_lessons()
    
    # If user is logged in, get lesson progress information
    lessons_with_progress = None
    if request.user.is_authenticated:
        lessons_with_progress = get_user_lessons_with_progress(request.user)
    
    context = {
        'lessons': lessons,
        'lessons_with_progress': lessons_with_progress,
    }
    return render(request, 'lessons/lesson_list.html', context)


def lesson1_view(request):
    """Lesson 1 detail page (quick access)"""
    lesson = get_lesson_by_number(1)
    if not lesson:
        return redirect('lessons:lesson_list')
    context = prepare_lesson_detail_data(lesson)
    return render(request, 'lessons/lesson_detail.html', context)


def lesson2_view(request):
    """Lesson 2 detail page (quick access)"""
    lesson = get_lesson_by_number(2)
    if not lesson:
        return redirect('lessons:lesson_list')
    context = prepare_lesson_detail_data(lesson)
    return render(request, 'lessons/lesson_detail.html', context)


def lesson3_view(request):
    """Lesson 3 detail page (quick access)"""
    lesson = get_lesson_by_number(3)
    if not lesson:
        return redirect('lessons:lesson_list')
    context = prepare_lesson_detail_data(lesson)
    return render(request, 'lessons/lesson_detail.html', context)


def lesson4_view(request):
    """Lesson 4 detail page (quick access)"""
    lesson = get_lesson_by_number(4)
    if not lesson:
        return redirect('lessons:lesson_list')
    context = prepare_lesson_detail_data(lesson)
    return render(request, 'lessons/lesson_detail.html', context)


def lesson5_view(request):
    """Lesson 5 detail page (quick access)"""
    lesson = get_lesson_by_number(5)
    if not lesson:
        return redirect('lessons:lesson_list')
    context = prepare_lesson_detail_data(lesson)
    return render(request, 'lessons/lesson_detail.html', context)


def lesson6_view(request):
    """Lesson 6 detail page (quick access)"""
    lesson = get_lesson_by_number(6)
    if not lesson:
        return redirect('lessons:lesson_list')
    context = prepare_lesson_detail_data(lesson)
    return render(request, 'lessons/lesson_detail.html', context)


def lesson7_view(request):
    """Lesson 7 detail page (quick access)"""
    lesson = get_lesson_by_number(7)
    if not lesson:
        return redirect('lessons:lesson_list')
    context = prepare_lesson_detail_data(lesson)
    return render(request, 'lessons/lesson_detail.html', context)


def lesson8_view(request):
    """Lesson 8 detail page (quick access)"""
    lesson = get_lesson_by_number(8)
    if not lesson:
        return redirect('lessons:lesson_list')
    context = prepare_lesson_detail_data(lesson)
    return render(request, 'lessons/lesson_detail.html', context)


def lesson9_view(request):
    """Lesson 9 detail page (quick access)"""
    lesson = get_lesson_by_number(9)
    if not lesson:
        return redirect('lessons:lesson_list')
    context = prepare_lesson_detail_data(lesson)
    return render(request, 'lessons/lesson_detail.html', context)


def lesson10_view(request):
    """Lesson 10 detail page (quick access)"""
    lesson = get_lesson_by_number(10)
    if not lesson:
        return redirect('lessons:lesson_list')
    context = prepare_lesson_detail_data(lesson)
    return render(request, 'lessons/lesson_detail.html', context)


def lesson_detail_view(request, slug):
    """Lesson detail page"""
    lesson = get_object_or_404(Lesson, slug=slug, status='published')
    context = prepare_lesson_detail_data(lesson)
    
    # If user is logged in, get progress information for this lesson
    user_progress = None
    if request.user.is_authenticated:
        user_progress = get_user_lesson_progress(request.user, lesson)
        # If user visits lesson detail page but no progress record, mark as started
        if not user_progress:
            user_progress = get_or_create_user_lesson_progress(request.user, lesson)
            user_progress.mark_as_started()
    
    # Get next lesson
    next_lesson = get_next_lesson(lesson)
    
    context['user_progress'] = user_progress
    context['next_lesson'] = next_lesson
    context['is_last_lesson'] = lesson.lesson_number == 10
    return render(request, 'lessons/lesson_detail.html', context)


@login_required
def lesson_complete_view(request, slug):
    """Toggle lesson completion status (complete/cancel completion)"""
    from django.urls import reverse
    
    lesson = get_object_or_404(Lesson, slug=slug, status='published')
    
    # Get or create progress record
    progress = get_or_create_user_lesson_progress(request.user, lesson)
    
    # Toggle completion status
    if progress.status == 'completed':
        # If completed, cancel completion status
        progress.mark_as_in_progress()
        messages.info(request, f'You have reset the progress for "{lesson.title}". You can complete it again!')
        return redirect('lessons:lesson_detail', slug=slug)
    else:
        # If not completed, mark as completed (signal handler will automatically handle rewards and achievements)
        progress.mark_as_completed()
        
        # Build success message
        message = f'Congratulations! You completed "{lesson.title}"!'
        if lesson.coin_reward > 0:
            message += f' You earned {lesson.coin_reward} virtual coins!'
        messages.success(request, message)
        
        # Redirect to detail page, add completed parameter to trigger reward animation
        redirect_url = reverse('lessons:lesson_detail', kwargs={'slug': slug})
        return redirect(f'{redirect_url}?completed=1')

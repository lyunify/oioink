from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Lesson(models.Model):
    """Lesson model"""
    LESSON_STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Lesson Title')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL Slug')
    subtitle = models.CharField(max_length=300, blank=True, verbose_name='Subtitle')
    description = models.TextField(blank=True, verbose_name='Description')
    
    # Cover image
    cover_image = models.ImageField(upload_to='lessons/covers/', blank=True, null=True, verbose_name='Cover Image')
    icon = models.CharField(max_length=50, default='💰', verbose_name='Icon (emoji)')
    
    # Lesson info
    lesson_number = models.IntegerField(unique=True, verbose_name='Lesson Number')
    age_range = models.CharField(max_length=20, default='6-12', verbose_name='Age Range')
    duration_minutes = models.IntegerField(default=15, verbose_name='Duration (minutes)')
    coin_reward = models.DecimalField(max_digits=10, decimal_places=2, default=50, verbose_name='Coin Reward', help_text='Virtual coins awarded when lesson is completed')
    
    # Status
    status = models.CharField(max_length=20, choices=LESSON_STATUS, default='draft', verbose_name='Status')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        ordering = ['lesson_number']
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
    
    def __str__(self):
        return f"Lesson {self.lesson_number}: {self.title}"
    
    def get_absolute_url(self):
        return reverse('lessons:lesson_detail', kwargs={'slug': self.slug})


class LessonSection(models.Model):
    """Lesson section/chapter model"""
    SECTION_TYPES = [
        ('intro', 'Introduction'),
        ('content', 'Content'),
        ('activity', 'Activity'),
        ('game', 'Game'),
        ('story', 'Story'),
        ('summary', 'Summary'),
    ]
    
    lesson = models.ForeignKey(Lesson, related_name='sections', on_delete=models.CASCADE, verbose_name='Lesson')
    title = models.CharField(max_length=200, verbose_name='Section Title')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, default='content', verbose_name='Section Type')
    content = models.TextField(verbose_name='Content (Markdown supported)')
    image = models.ImageField(upload_to='lessons/sections/', blank=True, null=True, verbose_name='Image')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Icon (emoji)')
    
    # Ordering
    order = models.IntegerField(default=0, verbose_name='Order')
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Lesson Section'
        verbose_name_plural = 'Lesson Sections'
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class LessonTip(models.Model):
    """Lesson tip/model hint model"""
    lesson = models.ForeignKey(Lesson, related_name='tips', on_delete=models.CASCADE, verbose_name='Lesson')
    title = models.CharField(max_length=200, verbose_name='Tip Title')
    content = models.TextField(verbose_name='Content')
    icon = models.CharField(max_length=50, default='💡', verbose_name='Icon (emoji)')
    order = models.IntegerField(default=0, verbose_name='Order')
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Lesson Tip'
        verbose_name_plural = 'Lesson Tips'
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class UserLessonProgress(models.Model):
    """User lesson progress model"""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progresses', verbose_name='User')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progresses', verbose_name='Lesson')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', verbose_name='Status')
    
    # Timestamps
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Started At')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Completed At')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        unique_together = [['user', 'lesson']]
        ordering = ['-updated_at']
        verbose_name = 'User Lesson Progress'
        verbose_name_plural = 'User Lesson Progresses'
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {self.get_status_display()}"
    
    def mark_as_started(self):
        """Mark lesson as started"""
        if self.status == 'not_started':
            from django.utils import timezone
            self.status = 'in_progress'
            self.started_at = timezone.now()
            self.save()
    
    def mark_as_completed(self):
        """Mark lesson as completed"""
        if self.status != 'completed':
            from django.utils import timezone
            self.status = 'completed'
            if not self.started_at:
                self.started_at = timezone.now()
            self.completed_at = timezone.now()
            self.save()
    
    def mark_as_in_progress(self):
        """Mark lesson as in progress (cancel completion status)"""
        if self.status == 'completed':
            from django.utils import timezone
            self.status = 'in_progress'
            # Keep started_at, but clear completed_at
            self.completed_at = None
            self.save()
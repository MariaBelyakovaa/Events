from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import Event, Participation, Comment

def index(request):
    """Главная страница с разделением на будущие и прошедшие события"""
    
    # будущие
    future_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    
    # прошедшие
    past_events = Event.objects.filter(date__lt=timezone.now()).order_by('-date')
    
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        date_str = request.POST.get('date', '')
        location = request.POST.get('location', '').strip()
        category = request.POST.get('category', 'other')
        description = request.POST.get('description', '').strip()
        
        if title and date_str and location:
            try:
                
                Event.objects.create(
                    title=title,
                    date=date_str,
                    location=location,
                    category=category,
                    description=description
                )
                messages.success(request, f'Событие "{title}" успешно добавлено!')
                return redirect('index')
            except Exception as e:
                messages.error(request, f'Ошибка: {str(e)}')
        else:
            messages.error(request, 'Заполните все обязательные поля!')
    
    context = {
        'future_events': future_events[:12],  
        'past_events': past_events[:6],       
        'events_count': Event.objects.count(),
        'future_count': future_events.count(),
        'past_count': past_events.count(),
        'now': timezone.now(),
    }
    
    return render(request, 'events/index.html', context)

def event_detail(request, event_id):
    """Детальная страница события"""
    event = get_object_or_404(Event, id=event_id)
    
    context = {
        'event': event,
        'participants': event.participation_set.all(),
        'comments': event.comment_set.all().order_by('-created_at'),
        'now': timezone.now(),
    }
    
    return render(request, 'events/detail.html', context)

def participate(request, event_id):
    """Обработка нажатия "Пойду!" """
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        user_name = request.POST.get('user_name', '').strip()
        
        if user_name:
            
            if not Participation.objects.filter(event=event, user_name=user_name).exists():
                Participation.objects.create(event=event, user_name=user_name)
                messages.success(request, f'Вы записались на событие!')
            else:
                messages.info(request, f'Вы уже записаны на это событие')
            
            return redirect('event_detail', event_id=event.id)
    
    return redirect('event_detail', event_id=event.id)

def add_comment(request, event_id):
    """Добавление комментария"""
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        author_name = request.POST.get('author_name', '').strip()
        text = request.POST.get('text', '').strip()
        
        if author_name and text:
            Comment.objects.create(
                event=event,
                author_name=author_name,
                text=text
            )
            messages.success(request, 'Комментарий добавлен!')
    
    return redirect('event_detail', event_id=event.id)
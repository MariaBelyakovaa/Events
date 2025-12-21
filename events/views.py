from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Event, Participation, Comment
from django.contrib import messages
def index(request):
    """Главная страница"""
    # Получаем все будущие события
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    
    # Обработка формы добавления события
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        date = request.POST.get('date', '')
        location = request.POST.get('location', '').strip()
        category = request.POST.get('category', 'other')
        description = request.POST.get('description', '').strip()
        
        if title and date and location:
            Event.objects.create(
                title=title,
                date=date,
                location=location,
                category=category,
                description=description
            )
            return redirect('index')
    
    context = {
        'events': events[:12],
        'events_count': Event.objects.count(),
        'today': timezone.now().date(),
    }
    
    return render(request, 'events/index.html', context)
def event_detail(request, event_id):
    
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/detail.html', {'event': event})

def participate(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        user_name = request.POST.get('user_name', '').strip()
        
        if user_name:
            if not Participation.objects.filter(event=event, user_name=user_name).exists():
                Participation.objects.create(event=event, user_name=user_name)
            
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
    
    return redirect('event_detail', event_id=event.id)

def event_detail(request, event_id):
    """Детальная страница события"""
    event = get_object_or_404(Event, id=event_id)
    
    context = {
        'event': event,
        'participants': event.participation_set.all(),
        'comments': event.comment_set.all().order_by('-created_at'),
    }
    
    return render(request, 'events/detail.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Event, Participation, Comment
from django.contrib import messages

def index(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    
    
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        location = request.POST.get('location')
        category = request.POST.get('category')
        description = request.POST.get('description')
        
        if title and date and location:
            
            event = Event.objects.create(
                title=title,
                date=date,
                location=location,
                category=category,
                description=description
            )
            messages.success(request, f'Событие "{title}" успешно добавлено!')
            return redirect('index')
        else:
            messages.error(request, 'Заполните все обязательные поля!')
    
    
    events_count = Event.objects.count()
    nearest_event = events.first().title if events.exists() else "Нет событий"
    
    context = {
        'events': events[:12],  
        'events_count': events_count,
        'nearest_event': nearest_event,
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

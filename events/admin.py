from django.contrib import admin
from .models import Event, Participation, Comment

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'category', 'created_at')
    list_filter = ('category', 'date')
    search_fields = ('title', 'location', 'description')

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'event', 'created_at')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'event', 'created_at')
    list_filter = ('created_at',)
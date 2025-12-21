from django.db import models

# Модель события
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('concert', '🎵 Концерт'),
        ('exhibition', '🖼️ Выставка'),
        ('meeting', '🤝 Встреча'),
        ('sport', '⚽ Спорт'),
        ('party', '🎉 Вечеринка'),
        ('other', '✨ Другое'),
    ]
    
    title = models.CharField('Название', max_length=200)
    date = models.DateTimeField('Дата и время')
    location = models.CharField('Место', max_length=200)
    description = models.TextField('Описание')
    category = models.CharField('Категория', max_length=50, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
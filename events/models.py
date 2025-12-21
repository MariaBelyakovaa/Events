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

# Модель участия
class Participation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Событие')
    user_name = models.CharField('Ваше имя', max_length=100)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_name} идет на {self.event.title}"
    
    class Meta:
        verbose_name = 'Участие'
        verbose_name_plural = 'Участники'

# Модель комментария
class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Событие')
    author_name = models.CharField('Ваше имя', max_length=100)
    text = models.TextField('Комментарий')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    def __str__(self):
        return f"Комментарий от {self.author_name}"
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
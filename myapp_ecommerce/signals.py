from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'your_app_name':  
        categories = [
            ('common', 'Common'),
            ('women', 'Women'),
            ('accessories', 'Accessories'),
            ('new_arrival', 'New Arrival')
        ]
        for code, name in categories:
            Category.objects.get_or_create(name=code)

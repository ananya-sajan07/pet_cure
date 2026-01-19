from django.core.management.base import BaseCommand
from userapp.models import Pet

class Command(BaseCommand):
    help = 'Update pet_type for existing pets based on category'
    
    def handle(self, *args, **kwargs):
        pets = Pet.objects.all()
        updated_count = 0
        
        for pet in pets:
            # Force save to trigger auto pet_type setting
            pet.save()
            updated_count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Updated {updated_count} pets with pet_type'))
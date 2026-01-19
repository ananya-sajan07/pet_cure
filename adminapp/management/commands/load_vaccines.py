from django.core.management.base import BaseCommand
from adminapp.models import Vaccine

class Command(BaseCommand):
    help = 'Load initial vaccine data into database'
    
    def handle(self, *args, **kwargs):
        # Dog vaccines
        dog_vaccines = [
            {
                'pet_type': 'dog',
                'vaccine_name': 'DP Vaccine',
                'recommended_age': '6 Weeks',
                'disease_protected': 'Canine Distemper, Parvo Viral Infection',
                'booster_required': True,
                'booster_timing': 'Multi Component Vaccine at 8 weeks',
                'annual_revaccination': True
            },
            {
                'pet_type': 'dog',
                'vaccine_name': 'Multi Component Vaccine',
                'recommended_age': '8 Weeks',
                'disease_protected': 'Canine distemper, Parvo viral infection, Kennel cough, Infectious canine hepatitis, Leptospirosis',
                'booster_required': True,
                'booster_timing': 'Multi Component Vaccine - Booster at 12 weeks',
                'annual_revaccination': True
            },
            {
                'pet_type': 'dog',
                'vaccine_name': 'Anti Rabies Vaccine',
                'recommended_age': '10 Weeks',
                'disease_protected': 'Rabies',
                'booster_required': True,
                'booster_timing': 'Anti Rabies Vaccine - Booster at 14 weeks',
                'annual_revaccination': True
            },
        ]
        for vaccine_data in dog_vaccines:
            Vaccine.objects.get_or_create(**vaccine_data)
        
        # Cat vaccines
        cat_vaccines = [
            {
                'pet_type': 'cat',
                'vaccine_name': 'Combined Core Vaccine',
                'recommended_age': '8 Weeks',
                'disease_protected': 'Feline Rhinotracheitis, Feline Calici, Feline Panleukopenia',
                'booster_required': True,
                'booster_timing': 'Combined Core Vaccine - Booster at 12 weeks',
                'annual_revaccination': True
            },
            {
                'pet_type': 'cat',
                'vaccine_name': 'Anti Rabies Vaccine',
                'recommended_age': '10 Weeks',
                'disease_protected': 'Rabies',
                'booster_required': True,
                'booster_timing': 'Anti Rabies Vaccine - Booster at 14 weeks',
                'annual_revaccination': True
            },
        ]

        for vaccine_data in cat_vaccines:
            Vaccine.objects.get_or_create(**vaccine_data)
        
        # Poultry vaccines
        poultry_vaccines = [
            {
                'pet_type': 'poultry',
                'vaccine_name': "Marek's Disease Vaccine",
                'recommended_age': 'Day old',
                'disease_protected': "Marek's Disease",
                'booster_required': False,
                'booster_timing': '',
                'annual_revaccination': False
            },
            {
                'pet_type': 'poultry', 
                'vaccine_name': 'Lasota',
                'recommended_age': '4-10 days',
                'disease_protected': 'Newcastle Disease',
                'booster_required': True,
                'booster_timing': 'F.Strain at 6-8 weeks',
                'annual_revaccination': True
            },
            {
                'pet_type': 'poultry',
                'vaccine_name': 'IBDV',
                'recommended_age': '10-14 days',
                'disease_protected': 'Infectious Bursal Disease',
                'booster_required': True,
                'booster_timing': 'IBDV at 10-22 weeks',
                'annual_revaccination': True
            },
        ]
        
        for vaccine_data in poultry_vaccines:
            Vaccine.objects.get_or_create(**vaccine_data)
        
        # Cattle vaccines
        cattle_vaccines = [
            {
                'pet_type': 'cattle',
                'vaccine_name': 'Foot and Mouth Disease (Oil Adjuvant)',
                'recommended_age': '4 months',
                'disease_protected': 'Foot and Mouth Disease',
                'booster_required': True,
                'booster_timing': '6 months after primary',
                'annual_revaccination': True
            },
            {
                'pet_type': 'cattle',
                'vaccine_name': 'HS / BQ Vaccine',
                'recommended_age': '6 months',
                'disease_protected': 'Hemorrhagic Septicemia / Black Quarter',
                'booster_required': False,
                'booster_timing': '',
                'annual_revaccination': True
            },
            {
                'pet_type': 'cattle',
                'vaccine_name': 'Brucella abortus (Strain 19)',
                'recommended_age': '4-8 months (female calves)',
                'disease_protected': 'Brucellosis',
                'booster_required': False,
                'booster_timing': '',
                'annual_revaccination': True
            },
        ]
        
        for vaccine_data in cattle_vaccines:
            Vaccine.objects.get_or_create(**vaccine_data)
        
        # Sheep & Goat vaccines
        sheep_goat_vaccines = [
            {
                'pet_type': 'sheep',
                'vaccine_name': 'PPR Vaccine',
                'recommended_age': '4 months onwards',
                'disease_protected': 'Peste des Petits Ruminants',
                'booster_required': False,
                'booster_timing': '',
                'annual_revaccination': False
            },
            {
                'pet_type': 'goat',
                'vaccine_name': 'PPR Vaccine',
                'recommended_age': '4 months onwards',
                'disease_protected': 'Peste des Petits Ruminants',
                'booster_required': False,
                'booster_timing': '',
                'annual_revaccination': False
            },
            {
                'pet_type': 'sheep',
                'vaccine_name': 'Enterotoxemia Vaccine',
                'recommended_age': '4 months of age',
                'disease_protected': 'Enterotoxemia',
                'booster_required': True,
                'booster_timing': '6 months after primary',
                'annual_revaccination': True
            },
            {
                'pet_type': 'goat',
                'vaccine_name': 'Enterotoxemia Vaccine',
                'recommended_age': '4 months of age',
                'disease_protected': 'Enterotoxemia',
                'booster_required': True,
                'booster_timing': '6 months after primary',
                'annual_revaccination': True
            },
        ]
        
        for vaccine_data in sheep_goat_vaccines:
            Vaccine.objects.get_or_create(**vaccine_data)

        # Swine vaccines
        swine_vaccines = [
            {
                'pet_type': 'swine',
                'vaccine_name': 'Swine Fever Vaccine',
                'recommended_age': '45 days - 1st dose',
                'disease_protected': 'Swine Fever',
                'booster_required': True,
                'booster_timing': '7 months - 2nd dose',
                'annual_revaccination': True
            },
            {
                'pet_type': 'swine',
                'vaccine_name': 'FMD Vaccine',
                'recommended_age': 'First dose 4 months of age',
                'disease_protected': 'Foot and Mouth Disease',
                'booster_required': True,
                'booster_timing': '15 days after each Swine Fever Vaccination',
                'annual_revaccination': True
            },
            {
                'pet_type': 'swine',
                'vaccine_name': 'HS Vaccine',
                'recommended_age': 'First dose 6 months of age',
                'disease_protected': 'Hemorrhagic Septicemia',
                'booster_required': True,
                'booster_timing': '5 months interval',
                'annual_revaccination': True
            },
        ]

        for vaccine_data in swine_vaccines:
            Vaccine.objects.get_or_create(**vaccine_data)
        
        self.stdout.write(self.style.SUCCESS('Vaccine data loaded successfully'))
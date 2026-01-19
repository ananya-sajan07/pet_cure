from django.db import models

# Create your models here.
class Admin(models.Model):
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    

class PetCategory(models.Model):
    petcategory=models.CharField(max_length=100)

class PetSubcategory(models.Model):
    petcategory=models.ForeignKey(PetCategory, on_delete=models.CASCADE, related_name='subcategories')
    petsubcategory=models.CharField(max_length=100)
    
class ProductCategory(models.Model):
    productcategory=models.CharField(max_length=100)
    
class Product(models.Model):
    productcategory = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    petcategory = models.ForeignKey(PetCategory, on_delete=models.CASCADE, related_name='products')
    petsubcategory = models.ForeignKey(PetSubcategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    
class Vaccine(models.Model):
    PET_TYPE_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'), 
        ('poultry', 'Poultry'),
        ('cattle', 'Cattle'),
        ('sheep', 'Sheep'),
        ('goat', 'Goat'),
        ('swine', 'Swine'),
    ]
    
    pet_type = models.CharField(max_length=20, choices=PET_TYPE_CHOICES)
    vaccine_name = models.CharField(max_length=200)
    recommended_age = models.CharField(max_length=100)  # e.g., "6 Weeks", "4 months"
    disease_protected = models.TextField()
    booster_required = models.BooleanField(default=False)
    booster_timing = models.CharField(max_length=100, blank=True, null=True)
    annual_revaccination = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.pet_type} - {self.vaccine_name}"
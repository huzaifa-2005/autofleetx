from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone


VEHICLE_TYPE_CHOICES = [
    ('City Car','CITY CAR'),  
    ('Electric','ELECTRIC CAR'),    
    ('Premium','PREMIUM'),
    ('Van OR Truck','VANS AND TRUCKS'),
]

#  Abstract Base 
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

#  Custom User 
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0.0)]
    )
    address = models.TextField(blank=False, null=False,default='')

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def add_balance(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
        self.save()
        return True

    def has_sufficient_balance(self, amount):
        return self.balance >= amount
    def save(self, *args, **kwargs):
        
        if self.email == '':
            self.email = None
        super().save(*args, **kwargs) 

#  Car Model 
class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    seating_capacity = models.PositiveIntegerField()
    rent_per_day = models.PositiveIntegerField()
    model_year = models.PositiveIntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)


    
    vehicle_type = models.CharField(
    max_length=20,
    choices=VEHICLE_TYPE_CHOICES,
    default='City Car',
)
    added_by = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    former_admin_name = models.CharField(max_length=150, default='Admin Not Assigned')
    date_added = models.DateTimeField(auto_now_add=True)
    HAS_ACCIDENT_CHOICES = [
    (True, 'Yes — Accident Reported'),
    (False, 'No — Clean Record'), 
    ]

    accident_history = models.BooleanField(choices=HAS_ACCIDENT_CHOICES, default=False)
    def __str__(self):
        return f"{self.name} - {self.brand}"

    def is_available(self):
        return self.available

    def mark_unavailable(self):
        self.available = False
        self.save()

    def mark_available(self):
        self.available = True
        self.save()
    @property
    def display_admin_name(self):
        if self.added_by is not None:
            if self.added_by.first_name and self.added_by.last_name:
                return f"{self.added_by.first_name} {self.added_by.last_name}"
            return self.added_by.username
        return self.former_admin_name

#  Rental Model 
class Rental(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rentals')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals')

    # Updated for datetime-based rental
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    returned_early = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["start_datetime"]),
            models.Index(fields=["end_datetime"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.start_datetime} to {self.end_datetime})"

    def calculate_days(self):
        delta = self.end_datetime - self.start_datetime
        return delta.total_seconds() / (60 * 60 * 24)  # returns float days

    def calculate_cost(self):
        days = self.calculate_days()
        return round(days * self.car.rent_per_day, 2)

    def save(self, *args, **kwargs):
        if not self.total_cost:
            self.total_cost = self.calculate_cost()
        super().save(*args, **kwargs)

    @classmethod
    def check_returns(cls):
        now = timezone.now()
        completed_rentals = cls.objects.filter(end_datetime__lte=now, is_active=True)
        for rental in completed_rentals:
            rental.is_active = False
            rental.save()
            rental.car.mark_available()

#  Transaction Model 
class Transaction(TimeStampedModel):
    TRANSACTION_TYPES = (
        ('ADD', 'Add Money'),
        ('PAYMENT', 'Rental Payment'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"

#  Contact Message Model 
class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name}"

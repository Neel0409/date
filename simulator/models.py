from django.db import models


class DateSelection(models.Model):
    DATE_CHOICES = [
        ('Beach Date', 'Beach Date'),
        ('Candlelight Dinner', 'Candlelight Dinner'),
        ('Movie Night', 'Movie Night'),
        ('Dream City', 'Dream City'),
    ]

    FOOD_CHOICES = [
        ('Pizza', 'Pizza'),
        ('Pasta', 'Pasta'),
        ('Burger', 'Burger'),
        ('Dessert', 'Dessert'),
    ]

    ACTIVITY_CHOICES = [
        ('Long Drive', 'Long Drive'),
        ('Dancing', 'Dancing'),
        ('Movie', 'Movie'),
        ('Stargazing', 'Stargazing'),
    ]

    name = models.CharField(max_length=100)
    date_choice = models.CharField(max_length=50, choices=DATE_CHOICES)
    food_choice = models.CharField(max_length=50, choices=FOOD_CHOICES)
    activity_choice = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    message = models.TextField(blank=True)
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date_choice}"

from django.db import models
from django.utils import timezone


class DateSelection(models.Model):
    DATE_CHOICES = [
        ('Beach Date', 'Beach Date'),
        ('Candlelight Dinner', 'Candlelight Dinner'),
        ('Movie Night', 'Movie Night'),
        ('Dream City', 'Dream City'),
        ('Other', 'Other (Let me decide)'),
    ]

    FOOD_CHOICES = [
        ('Pizza', 'Pizza'),
        ('Pasta', 'Pasta'),
        ('Burger', 'Burger'),
        ('Dessert', 'Dessert'),
        ("Something special (I'll cook for you ❤️)", "Something special (I'll cook for you ❤️)"),
        ('Other', "Other (I'll decide)"),
    ]

    ACTIVITY_CHOICES = [
        ('Long Drive', 'Long Drive'),
        ('Dancing', 'Dancing'),
        ('Movie', 'Movie'),
        ('Stargazing', 'Stargazing'),
        ('Shopping', 'Shopping'),
        ('Gaming Together', 'Gaming Together'),
        ('Photography', 'Photography'),
        ('Other', 'Other (Your own idea)'),
    ]

    name = models.CharField(max_length=100, verbose_name="Name")
    selected_date = models.DateField(default=timezone.now, verbose_name="Date")
    date_choice = models.CharField(max_length=100, choices=DATE_CHOICES, verbose_name="Date Location")
    custom_date_choice = models.CharField(max_length=255, blank=True, default='', verbose_name="Custom Date Location")
    food_choice = models.CharField(max_length=100, choices=FOOD_CHOICES, verbose_name="Food Choice")
    custom_food_choice = models.CharField(max_length=255, blank=True, default='', verbose_name="Custom Food Choice")
    activity_choice = models.CharField(max_length=100, choices=ACTIVITY_CHOICES, verbose_name="Activity Choice")
    custom_activity_choice = models.CharField(max_length=255, blank=True, default='', verbose_name="Custom Activity")
    message = models.TextField(blank=True, verbose_name="Personal Message")
    consent = models.BooleanField(default=False, verbose_name="Consent")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submission Time")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Date Selection"
        verbose_name_plural = "Date Selections"

    def __str__(self):
        return f"{self.name} - {self.get_effective_date_choice()} ({self.selected_date})"

    def get_effective_date_choice(self):
        if self.date_choice == 'Other' and self.custom_date_choice:
            return f"Other ({self.custom_date_choice})"
        return self.date_choice

    def get_effective_food_choice(self):
        if self.food_choice == 'Other' and self.custom_food_choice:
            return f"Other ({self.custom_food_choice})"
        return self.food_choice

    def get_effective_activity_choice(self):
        if self.activity_choice == 'Other' and self.custom_activity_choice:
            return f"Other ({self.custom_activity_choice})"
        return self.activity_choice

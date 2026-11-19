from django.contrib import admin
from .models import DateSelection


@admin.register(DateSelection)
class DateSelectionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_choice',
        'food_choice',
        'activity_choice',
        'created_at',
    )
    list_filter = (
        'date_choice',
        'food_choice',
        'activity_choice',
    )
    search_fields = (
        'name',
        'message',
    )
    readonly_fields = ('created_at',)

from django.contrib import admin
from .models import DateSelection


@admin.register(DateSelection)
class DateSelectionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'selected_date',
        'display_date_location',
        'display_food_choice',
        'display_activity_choice',
        'consent',
        'created_at',
    )
    list_filter = (
        'selected_date',
        'date_choice',
        'food_choice',
        'activity_choice',
        'consent',
        'created_at',
    )
    search_fields = (
        'name',
        'message',
        'custom_date_choice',
        'custom_food_choice',
        'custom_activity_choice',
    )
    readonly_fields = ('created_at',)
    date_hierarchy = 'selected_date'

    fieldsets = (
        ('Guest Information', {
            'fields': ('name', 'selected_date', 'consent', 'created_at')
        }),
        ('Date Location', {
            'fields': ('date_choice', 'custom_date_choice'),
            'description': 'Selected location or custom destination idea.'
        }),
        ('Food & Dining', {
            'fields': ('food_choice', 'custom_food_choice'),
            'description': 'Selected food preference or special dishes.'
        }),
        ('Activities & Fun', {
            'fields': ('activity_choice', 'custom_activity_choice'),
            'description': 'Selected activity or custom experience idea.'
        }),
        ('Special Message', {
            'fields': ('message',),
        }),
    )

    @admin.display(description='Date Location')
    def display_date_location(self, obj):
        if obj.date_choice == 'Other' and obj.custom_date_choice:
            return f"Other: {obj.custom_date_choice}"
        return obj.date_choice

    @admin.display(description='Food Choice')
    def display_food_choice(self, obj):
        if obj.food_choice == 'Other' and obj.custom_food_choice:
            return f"Other: {obj.custom_food_choice}"
        return obj.food_choice

    @admin.display(description='Activity Choice')
    def display_activity_choice(self, obj):
        if obj.activity_choice == 'Other' and obj.custom_activity_choice:
            return f"Other: {obj.custom_activity_choice}"
        return obj.activity_choice

from django.contrib import admin
from .models import Client

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Organizes columns precisely in the requested layout
    list_display = (
        'last_name', 
        'first_name', 
        'phone_number', 
        'current_coffee_count', 
        'prepaid_cards_remaining', 
        'prepaid_card_coffees_left'
    )
    
    # Enables quick inline editing directly from the table row without clicking into profiles
    list_editable = (
        'current_coffee_count', 
        'prepaid_cards_remaining'
    )
    
    # Adds a rapid lookup search bar targeting phone numbers and names
    search_fields = ('phone_number', 'last_name', 'first_name')
    
    # Orders clients alphabetically by last name by default
    ordering = ('last_name', 'first_name')

    @admin.display(description="Coffees left on active card")
    def prepaid_card_coffees_left(self, obj):
        """
        Calculates and shows how many cups are left out of 11 on the active card.
        If no card is currently punched but they have inventory, it reads 11.
        """
        if obj.current_card_punch_count == 0 and obj.prepaid_cards_remaining > 0:
            return 11
        elif obj.current_card_punch_count == 0:
            return 0
        return obj.PREPAID_CARD_MAX_CUPS - obj.current_card_punch_count
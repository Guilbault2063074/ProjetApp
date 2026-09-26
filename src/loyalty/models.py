from django.db import models

# Create your models here.

from django.db import models
from django.core.exceptions import ValidationError

class Client(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Regular loyalty count (Holds values from 0 up to 10)
    current_coffee_count = models.PositiveIntegerField(default=0)
    
    prepaid_cards_remaining = models.PositiveIntegerField(default=0)
    current_card_punch_count = models.PositiveIntegerField(default=0)

    REGULAR_FREE_THRESHOLD = 10 
    PREPAID_CARD_MAX_CUPS = 11

    def log_regular_coffee_purchase(self):
        """
        Increments standard loyalty stamps up to a maximum of 10.
        If they are sitting at 10/10, clicking the button redeems the reward,
        resetting the counter cleanly back to 0.
        """
        # Fix: Explicitly check if they are ALREADY at 10 BEFORE adding anything new
        if self.current_coffee_count == self.REGULAR_FREE_THRESHOLD:
            self.current_coffee_count = 0
        else:
            self.current_coffee_count += 1
            
        self.save()

    def add_prepaid_cards(self, quantity=1):
        """Allows direct inventory increments from the barista station dashboard view."""
        self.prepaid_cards_remaining += quantity
        self.save()

    def punch_prepaid_card(self):
        """Consumes a coffee cup from their active prepaid inventory card."""
        if self.current_card_punch_count == 0:
            if self.prepaid_cards_remaining <= 0:
                raise ValidationError("This client has no prepaid cards left to use.")
            self.prepaid_cards_remaining -= 1
            self.current_card_punch_count = 1
        else:
            self.current_card_punch_count += 1

        if self.current_card_punch_count >= self.PREPAID_CARD_MAX_CUPS:
            self.current_card_punch_count = 0

        self.save()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"

from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Client
import json

# Create your views here.

def dashboard(request):
    return render(request, 'loyalty/dashboard.html')

def search_clients(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'clients': []})
    
    clients = Client.objects.filter(phone_number__icontains=query)[:5]
    results = []
    for c in clients:
        if c.current_card_punch_count == 0 and c.prepaid_cards_remaining > 0:
            coffees_left = 11
        elif c.current_card_punch_count == 0:
            coffees_left = 0
        else:
            coffees_left = c.PREPAID_CARD_MAX_CUPS - c.current_card_punch_count

        results.append({
            'id': c.id,
            'name': c.full_name,
            'phone_number': c.phone_number,
            'current_coffee_count': c.current_coffee_count,
            'prepaid_cards_remaining': c.prepaid_cards_remaining,
            'prepaid_card_coffees_left': coffees_left
        })
    return JsonResponse({'clients': list(results)})

@csrf_exempt
def handle_action(request):
    """API Endpoint: Processes loyalty points, card punches, or inventory additions."""
    if request.method == 'POST':
        data = json.loads(request.body)
        client_id = data.get('client_id')
        action = data.get('action')
        
        client = get_object_or_404(Client, id=client_id)
        error_message = None
        
        try:
            if action == 'add_regular':
                client.log_regular_coffee_purchase()
            elif action == 'punch_prepaid':
                client.punch_prepaid_card()
            elif action == 'add_card':
                client.add_prepaid_cards(1)  # Directly buys/adds 1 card
        except ValidationError as e:
            error_message = str(e.message)

        if client.current_card_punch_count == 0 and client.prepaid_cards_remaining > 0:
            coffees_left = 11
        elif client.current_card_punch_count == 0:
            coffees_left = 0
        else:
            coffees_left = client.PREPAID_CARD_MAX_CUPS - client.current_card_punch_count

        return JsonResponse({
            'success': error_message is None,
            'error': error_message,
            'client': {
                'id': client.id,
                'name': client.full_name,
                'phone_number': client.phone_number,
                'current_coffee_count': client.current_coffee_count,
                'prepaid_cards_remaining': client.prepaid_cards_remaining,
                'prepaid_card_coffees_left': coffees_left
            }
        })

@csrf_exempt
def create_client_inline(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            client = Client.objects.create(
                phone_number=data.get('phone_number'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                prepaid_cards_remaining=int(data.get('prepaid_cards_remaining', 0))
            )
            return JsonResponse({
                'success': True,
                'client': {
                    'id': client.id,
                    'name': client.full_name,
                    'phone_number': client.phone_number,
                    'current_coffee_count': client.current_coffee_count,
                    'prepaid_cards_remaining': client.prepaid_cards_remaining,
                    'prepaid_card_coffees_left': 11 if client.prepaid_cards_remaining > 0 else 0
                }
            })
        except Exception:
            return JsonResponse({'success': False, 'error': 'This phone number is already registered.'})
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.urls import reverse

from .models import Card, Session


def index(request):
    return HttpResponse("<pre>int seconds = 30;</pre>")


def card_by_id(request, card_nr: int):
    try:
        card = Card.objects.get(number=card_nr)
        return JsonResponse({'card': card_nr, 'words': card.words_list_with_description})
    except ObjectDoesNotExist:
        return JsonResponse({"error": f"Card {card_nr} does not exist!"})


def get_token(request):
    session = Session()
    session.save()
    return JsonResponse({'token': session.id,
                         'secret': session.secret,
                         'get_card': f"{reverse('get-card')}?token={session.id}&secret={session.secret}"
                         })


def get_card(request: HttpRequest):
    token = request.GET.get('token')
    secret = request.GET.get('secret')

    if token and not secret or not token and secret:
        # XOR on token and secret
        return JsonResponse({'error': 'No token or secret'})
    elif token and secret:
        # Verify token and secret match
        try:
            session = Session.objects.get(id=token, secret=secret)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Token expired or invalid"})

        # Check is the session has seen all the cards
        if Card.objects.count() is session.used_cards.count():
            return JsonResponse({"error": "All cards have been used"})

        # Find a new Card
        while True:
            card = Card.random()
            if card not in session.used_cards.all():
                session.used_cards.add(card)
                return JsonResponse(card.json())
    else:
        # Just a random question
        return JsonResponse(Card.random().json())

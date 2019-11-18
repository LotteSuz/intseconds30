from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),
    path('card/<int:card_nr>', views.card_by_id, name='card'),
    path('get_token', views.get_token, name='get-token'),
    path('get_card', views.get_card, name='get-card'),
]

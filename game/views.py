from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests

team1_hits = []
team2_hits = []
round_counter = 0
max_rounds = 4
# Create your views here.
def index(request):
    #return render(request, "game/index.html")
    return render(request, "game/teams.html")

@csrf_exempt
def seconds(request):
    global round_counter
    global max_rounds
    res = requests.get("http://127.0.0.1:8000/api/get_token").json()
    token = res['token']
    secret = res['secret']
    if request.method == "POST":
            hits = request.POST.getlist("words")
            if round_counter % 2 == 0:
                print("TEAM_1")
                for hit in hits:
                    team1_hits.append(hit)
            else:
                print("TEAM_2")
                for hit in hits:
                    team2_hits.append(hit)
            if round_counter == max_rounds:
                team1 = len(team1_hits)
                team2 = len(team2_hits)
                if team1 > team2:
                    winner_name = 'Team 1'
                    winner_points = team1
                    loser_name = 'Team 2'
                    loser_points = team2
                else:
                    winner_name = 'Team 2'
                    winner_points = team2
                    loser_name = 'Team 1'
                    loser_points = team1
                return render(request, "game/end.html", {'winner_name':winner_name, 'winner_points':winner_points, 'loser_name':loser_name,'loser_points':loser_points})
            card = requests.get(f"http://127.0.0.1:8000/api/get_card?token={token}&secret={secret}").json()['words']
            round_counter += 1
            return render(request, "game/seconds.html", {'card':card, 'player':'john'})

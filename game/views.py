from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api.models import Session

team1_hits = []
team2_hits = []
round_counter = 0
max_rounds = 8
player_counter = 0
team1_players = []
team2_players = []


# Create your views here.

def index(request):
    # return render(request, "game/index.html"
    return render(request, "game/teams.html")


@csrf_exempt
@require_http_methods(["POST"])
def seconds(request):
    global round_counter
    global max_rounds
    global player_counter
    global team1_hits
    global team2_hits
    global team1_players
    global team2_players
    if round_counter == 0:
        # res = requests.get(request.build_absolute_uri(reverse("api:get-token"))).json()
        api_session = Session()
        api_session.save()
        # res = requests.get("http://127.0.0.1:8000/api/get_token").json()
        request.session['token'] = api_session.id
        request.session['secret'] = api_session.secret
        for i in range(1, 5):
            if request.POST[f't1{i}'] == '':
                message = 'Please enter four players for each team'
                return redirect('index')
            team1_players.append(request.POST[f't1{i}'])
        for j in range(1, 5):
            if request.POST[f't2{j}'] == '':
                message = 'Please enter four players for each team'
                return redirect('index')
            team2_players.append(request.POST[f't2{j}'])

    hits = request.POST.getlist("words")

    # append points
    if round_counter % 2 == 0:
        request.session['turn'] = team1_players[player_counter]
        for hit in hits:
            team1_hits.append(hit)
    else:
        request.session['turn'] = team2_players[player_counter]
        for hit in hits:
            team2_hits.append(hit)
            player_counter += 1

    # determine winner
    if round_counter == max_rounds:
        round_counter = 0
        team1_points = len(team1_hits)
        team2_points = len(team2_hits)
        team1_players.clear()
        team2_players.clear()
        team1_hits.clear()
        team2_hits.clear()
        player_counter = 0
        if team1_points == team2_points:
            tie = True
            return render(request, "game/end.html", {'tie': tie})
        elif team1_points > team2_points:
            winner_name = 'Team 1'
            winner_points = team1_points
            loser_name = 'Team 2'
            loser_points = team2_points
            return render(request, "game/end.html",
                          {'winner_name': winner_name, 'winner_points': winner_points, 'loser_name': loser_name,
                           'loser_points': loser_points})
        elif team1_points < team2_points:
            winner_name = 'Team 2'
            winner_points = team2_points
            loser_name = 'Team 1'
            loser_points = team1_points
            return render(request, "game/end.html",
                          {'winner_name': winner_name, 'winner_points': winner_points, 'loser_name': loser_name,
                           'loser_points': loser_points})

    # get cards to play with
    token = request.session['token']
    secret = request.session['secret']
    player = request.session['turn']

    # link = request.build_absolute_uri(reverse("api:get-card"))
    # card = requests.get(f"{link}?token={token}&secret={secret}").json()['words']
    card = Session.objects.get(id__exact=token, secret__exact=secret).get_card().json()['words']

    round_counter += 1
    return render(request, "game/seconds.html", {'card': card, 'player': player})

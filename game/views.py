from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api.models import Session

max_rounds = 8


def index(request):
    # return render(request, "game/index.html"
    return render(request, "game/teams.html")


@csrf_exempt
@require_http_methods(["POST"])
def seconds(request):
    global max_rounds
    if 'round' not in request.session or request.session['round'] == 0:
        request.session['round'] = 0
        request.session['player'] = 0
        request.session['scoreteam1'] = 0
        request.session['scoreteam2'] = 0
        request.session['team1'] = []
        request.session['team2'] = []
        api_session = Session()
        api_session.save()
        request.session['token'] = api_session.id
        request.session['secret'] = api_session.secret

        # get teams
        team1_players = []
        for i in range(1, 5):
            if request.POST[f't1{i}'] == '':
                message = 'Please enter four players for each team'
                return redirect('index')
            team1_players.append(request.POST[f't1{i}'])
        request.session['team1'] = team1_players
        team2_players = []
        for j in range(1, 5):
            if request.POST[f't2{j}'] == '':
                message = 'Please enter four players for each team'
                return redirect('index')
            team2_players.append(request.POST[f't2{j}'])
        request.session['team2'] = team2_players

    hits = request.POST.getlist("words")

    round = request.session['round']
    # append points
    if round % 2 == 0:
        points = len(hits)
        request.session['scoreteam1'] += points
        if round != max_rounds:
            request.session['turn'] = request.session['team1'][int(round/2)]
    else:
        points = len(hits)
        request.session['scoreteam2'] += points
        if round != max_rounds:
            request.session['turn'] = request.session['team2'][int(round/2)]

    # determine winner
    if round == max_rounds:
        request.session['round'] = 0
        team1_points = request.session['scoreteam1']
        team2_points = request.session['scoreteam2']
        request.session['scoreteam1'] = 0
        request.session['scoreteam2'] = 0
        request.session['turn'] = 0
        request.session['team1'] = []
        request.session['team2'] = []
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
    request.session['round'] += 1
    return render(request, "game/seconds.html", {'card': card, 'player': player})

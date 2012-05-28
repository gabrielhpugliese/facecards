from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django_fukinbook.decorators import facebook_auth_required
from django_fukinbook.graph_api import GraphAPI
from models import *
import simplejson
import random

def get_friends(player_fb_id, access_token):
    api = GraphAPI(access_token)
    
    fql = ('''SELECT uid, name, friend_count, likes_count, pic_square
        FROM user WHERE uid 
        IN (SELECT uid2 FROM friend WHERE uid1 = {0})''').format(player_fb_id)
    friends = api.get(path='fql', fql=fql)
    
    return friends

def create_cards(player, access_token, limit=20):
    player_friends = get_friends( player.user.username, access_token )
    random.shuffle(player_friends)
    
    count = 1
    for f in player_friends:
            
        likes_count = f['likes_count']
        friend_count = f['friend_count']
        if likes_count == None or friend_count == None:
            continue
        
        c = Card(player=player, name=f['name'], pic_square=f['pic_square'], order=count)
        c.save()
        Attribute(card=c, name="likes", attr=likes_count ).save()
        Attribute(card=c, name="friends", attr=friend_count ).save()
        count += 1
        if count == limit+1:
            break
            
    return player_friends
        
@facebook_auth_required
def create_game(request, opponent_fb_id):
    game = Game(status='1')
    game.save() 
    
    player1 = Player(user = request.user, game=game, last_round=1)
    player1.save()
    op_user_id = User.objects.get(username=opponent_fb_id)
    player2 = Player(user = op_user_id, game=game, last_round=1)
    player2.save();
    
    
    f1 = create_cards( player1, request.access_token )
    f2 = create_cards( player2, request.access_token )
    
    Round(round_number=1, game=game).save()
    
    players = game.player_set.all()
    return HttpResponseRedirect(reverse('app.views.game_details', args=(game.id,)))
    
def list_games(request):
    games = Game.objects.all()
    return render_to_response("games.html", {'games': games})
    
def game_details(request, game_id):
    game = Game.objects.get(pk=game_id)
    players = game.player_set.all()
    
    player = None
    player_number = -1
    if players[0].user == request.user:
        player = players[0]
        player_number = 0
    else:
        player = players[1]
        player_number = 1
        
    rounds = game.round_set.all()
    your_turn = False
    my_last_round = None
    if player.last_round == len(rounds):
        if int(game.status) == player_number:
            your_turn = True
    else:
        my_last_round = Round.objects.filter(game=game, round_number=player.last_round)
        
    return render_to_response("game_details.html", {'game': game, 'players': players, 
                                'your_turn': your_turn, 'my_last_round': my_last_round, 'player': player})

@facebook_auth_required
def index(request):
    friends = get_friends(request.user , request.access_token)
    for f in friends:
        try:
            u = User.objects.get(username=f['uid'])
            f['ourUser'] = True
        except:
            f['ourUser'] = False
    return render_to_response("index.html", {'friends' : friends})
    
    
def show_users(request):
    users = User.objects.all()
    return render_to_response('users.html', {'users': users})

def user_details(request, user_id):
    if not request.user.is_authenticated():
        return render_to_response('user_details.html', {'user': None, 'message': 'You\'re not logged in.'})
    try:
        user = User.objects.get(username=user_id)
        return render_to_response('user_details.html', {'user': user, 'message': 'success'})
    except:
        return render_to_response('user_details.html', {'user': None, 'message': 'Your friend is not on our database'})


@facebook_auth_required
def invite_user(request, user_id):
	print(request.user)
	friends = get_friends(request.user , request.access_token)

	invited = ""
	for f in friends:
		try:
			u = User.objects.get(username=f['uid'])
			f['ourUser'] = True
		except:
			f['ourUser'] = False

	for f in friends:
		if(f['uid'] == int(user_id)):
			invited = f['name']


	if invited == "":
		return render_to_response("index.html", {'friends' : friends})
	else:
		return render_to_response("index.html", {'friends' : friends, 'invited' : invited})



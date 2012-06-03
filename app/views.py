from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django_fukinbook.decorators import facebook_auth_required
from django_fukinbook.graph_api import GraphAPI
from models import *
import simplejson
import random
from django.contrib.auth.decorators import login_required
from facebook_client import FacebookClient
from game_handler import GameHandler
import logging

@facebook_auth_required
def create_game(request, opponent_fb_id):
    handler = GameHandler()
    game_id = handler.create_game(request.user, request.access_token,
                                  opponent_fb_id)
    return HttpResponseRedirect(reverse('app.views.game_details', args=(game_id,)))
    
def list_games(request):
    games = Game.objects.all()
    return render_to_response("games.html", {'games': games})

@login_required    
def game_details(request, game_id):
    handler = GameHandler()
    template_context = handler.get_game_details(request.user, game_id)
    return render_to_response("game_details.html", template_context)

@facebook_auth_required
def index(request):
    client = FacebookClient(request.access_token)
    friends = client.get_friends()
    friends.sort(key=(lambda x: x['name']))

    if friends:
        for f in friends:
            try:
                u = User.objects.get(username=f['uid'])
                f['our_user'] = True
            except:
                f['our_user'] = False
    return render_to_response("index.html", {'friends' : friends})

def show_users(request):
    users = User.objects.all()
    return render_to_response('users.html', {'users': users})

@login_required
def user_details(request, user_id, template='user_details.html'):
    user = None
    try:
        user = User.objects.get(username=user_id)
    except:
        logging.info('User not found: ', user_id)
        
    return render_to_response(template, {'user': user})

@facebook_auth_required
def invite_user(request, user_id):
    client = FacebookClient(request.access_token)
    friends = client.get_friends()

    invited = ""
    for f in friends:
        try:
            u = User.objects.get(username=f['uid'])
            f['our_user'] = True
        except:
            f['our_user'] = False

    for f in friends:
        if(f['uid'] == int(user_id)):
            invited = f['name']

    template_context = {'friends' : friends, 'invited' : invited}
    return render_to_response("index.html", template_context)

@login_required    
def solve_round(request, game_id, attr_name):
    #Fazer a logica pra ver quem ganhou
    #atualizar o Round com o atributo escolhido
    #atualizar as cartas do player que ganhou
    #atualizar o round do player que jogou
    #atualizar o status do game
    #criar um round novo

    game = Game.objects.get(pk=int(game_id))
    total = len( game.round_set.all() )
    Round(round_number=total+1, game=game).save()
    return HttpResponseRedirect(reverse('app.views.game_details', args=(game_id,)))

@login_required    
def refresh_round(request, game_id, player_number):
    game = Game.objects.get(pk=int(game_id))
    total = len( game.round_set.all() )
    player = game.player_set.all()[ int(player_number) ]
    if player.last_round < total:
        player.last_round += 1
        player.save()
    return HttpResponseRedirect(reverse('app.views.game_details', args=(game_id,)))

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


from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render_to_response

def get_friends(player):
    return [1,2,3]
    #return None

def create_cards(player):
    player_friends = get_friends( player )
    
    count = 1
    for f in player_friends:
        c = Card(player=player, name="Amigo", pic_square= None, order=count)
        c.save()
        Attribute(card=c, name="likes", attr=1 ).save() #f.get( likes_count )
        Attribute(card=c, name="friends", attr=2 ).save()
        count += 1
        

def create_game(request):
    game = Game(status='1')
    game.save() 
    
    player1 = Player(user = request.user, game=game, last_round=1)
    player1.save()
    op_user_id = request.POST["opponent_id"]
    player2 = Player(user = op_user_id, game=game, last_round=1)
    player2.save();
    
    
    create_cards( player1 )
    create_cards( player2 )
    
    Round(round_number=1, game=game).save()
    
    return HttpResponse('OK')

def canvas(request):
    return HttpResponse('Voce logou -- acho que precisa daqueles auth_required antes pra dar tudo certo -- ou eu pego a session na mao e adiciono o usuario no banco')
    
    
def show_users(request):
    users = User.objects.all()
    return render_to_response('users.html', {'users': users})

def user_details(request, user_id):
    if not request.user.is_authenticated():
        return render_to_response('user_details.html', {'user': None, 'message': 'You\'re not logged in.'})
    user = User.objects.get(pk=user_id)
    return render_to_response('user_details.html', {'user': user, 'message': 'success'})




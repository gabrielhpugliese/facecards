from facebook_client import FacebookClient
from models import Game, Player, Card, Attribute, Round
from django.contrib.auth.models import User
import random
import logging
from django.db import transaction

class GameHandler(object):
    @transaction.commit_on_success
    def __create_cards(self, player, access_token, limit=20):
        client = FacebookClient(access_token)
        player_friends = client.get_friends_attributes()
        random.shuffle(player_friends)
        
        count = 1
        logging.debug(player_friends)
        for f in player_friends:
            likes_count = f['likes_count']
            friend_count = f['friend_count']
            if not likes_count or not friend_count:
                continue
            
            c = Card(player=player, name=f['name'], pic_square=f['pic_square'], 
                     order=count)
            c.save()
            Attribute(card=c, name="likes", attr=likes_count).save()
            Attribute(card=c, name="friends", attr=friend_count).save()
            count += 1
            if count == limit+1:
                break
                
        return player_friends
    
    @transaction.commit_on_success
    def create_game(self, player, access_token, opponent_fb_id):
        game = Game(status='1')
        game.save() 
        
        player1 = Player(user=player, game=game, last_round=1)
        player1.save()
        
        op_user = User.objects.get(username=opponent_fb_id)
        player2 = Player(user=op_user, game=game, last_round=1)
        player2.save()
        
        f1 = self.__create_cards(player1, access_token)
        f2 = self.__create_cards(player2, access_token)
        
        Round(round_number=1, game=game).save()
        
        players = game.player_set.all()
        
        return game.id
    
    def get_game_details(self, user, game_id):
        game = Game.objects.get(pk=game_id)
        players = game.player_set.all()
        
        player = None
        player_number = -1
        if players[0].user == user:
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
            
        template_context = {'game': game, 'players': players, 
                        'your_turn': your_turn, 'my_last_round': my_last_round, 
                        'player': player}
        return template_context
    
            
            
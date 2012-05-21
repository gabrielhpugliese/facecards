from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.ForeignKey(User)
    last_round = models.IntegerField()
    
    def __unicode__(self):
        return '{0}'.format(self.user.first_name)
    
    
class Card(models.Model):
    player = models.ForeignKey(Player)
    name = models.CharField(max_length=150)
    pic_square = models.URLField()
    order = models.IntegerField()
    
    def __unicode__(self):
        return '{0}'.format(self.name)


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    attr = models.IntegerField()
    card = models.ForeignKey(Card, null=True)
    
    def __unicode__(self):
        return '{0} - {1}'.format(self.name, self.attr)

    
class Game(models.Model):
	status = models.CharField(max_length=1)
	player1 = models.ForeignKey(Player, related_name="player1")
	player2 = models.ForeignKey(Player, related_name="player2")
        
        
class Round(models.Model):
    attr = models.OneToOneField(Attribute, null=True)
    game = models.ForeignKey(Game)
    round_number = models.IntegerField()
    
    def __unicode__(self):
        return '{0} - {1}'.format(self.game, self.attr)

	

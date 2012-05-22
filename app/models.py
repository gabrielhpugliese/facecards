from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
	status = models.CharField(max_length=1)

class Player(models.Model):
    game = models.ForeignKey(Game)
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

    
        
        
class Round(models.Model):
    attr = models.OneToOneField(Attribute, null=True)
    game = models.ForeignKey(Game)
    round_number = models.IntegerField()
    
    def __unicode__(self):
        return '{0} - {1}'.format(self.game, self.attr)

	

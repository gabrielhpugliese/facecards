from django_fukinbook.graph_api import GraphAPI

class FacebookClient(GraphAPI):
    def get_friends(self):
        fql = '''SELECT uid, name, pic_square FROM user WHERE uid 
            IN (SELECT uid2 FROM friend WHERE uid1 = me())'''
        friends = self.get(path='fql', fql=fql)
        return friends
    
    def get_friends_attributes(self):
        fql = '''SELECT uid, name, likes_count, friend_count, pic_square 
        FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())'''
        friends = self.get(path='fql', fql=fql)
        return friends
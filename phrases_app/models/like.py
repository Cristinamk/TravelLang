from phrases_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask import flash, session
from phrases_app.models import user,phrase



class Likes:
    db = 'phrases'
    def __init__(self, data):
        self.user_id=data['user_id']
        self.userphrase_id = data['userphrase_id']



    @classmethod
    def create_like(cls, id):
        data ={'user_id': session['user_id'],
            'userphrase_id': id}
        query = '''
        INSERT INTO likes
        (user_id,userphrase_id)
        VALUES
        (%(user_id)s,%(userphrase_id)s);
        '''
        connectToMySQL(cls.db).query_db(query,data)
        return True
    
    @classmethod
    def fetch_all_by_phrase_id(cls,id):
        data= {'id':id}
        query ='''
        SELECT * FROM likes
        WHERE userphrase_id = %(id)s;
        '''
        return connectToMySQL(cls.db).query_db(query,data)
    @classmethod 
    def delete_like(cls,id,userphrase_id):
        data = {'id':id,
                'userphrase_id':userphrase_id}
        query = '''
        DELETE FROM likes
        WHERE user_id = %(id)s
        AND userphrase_id = %(userphrase_id)s;
        '''
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def if_user_liked_already(id):
        this_phrase_like = Likes.fetch_all_by_phrase_id(id)
        for like in this_phrase_like:
            if like['user_id']== session['user_id']:
                Likes.delete_like(session['user_id'],id)
                return True
        return False

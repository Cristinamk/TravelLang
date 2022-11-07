from phrases_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask import flash, session
from phrases_app.models import user

class Userpharase:
    db = 'phrases'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.phrase = data['phrase']
        self.translation = data['translation']
        self.language = data['language']
        self.experience = data['experience']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.likes = []

    @classmethod
    def create_phrase(cls, form_data):
        if not cls.validate_phrase_form(form_data): 
            return False
        data = form_data.copy()
        data['user_id'] = session['user_id']
        query = '''
        INSERT INTO userphrase
        (user_id,phrase,translation,language,experience)
        VALUES
        (%(user_id)s,%(phrase)s,%(translation)s,%(language)s,%(experience)s);
        '''
        connectToMySQL(cls.db).query_db(query,data)
        return True
    
    @classmethod
    def update_phrase(cls,form_data,id):
        if not cls.validate_phrase_form(form_data):
            return False
        data = form_data.copy()
        data['id'] = id
        query = '''
        UPDATE userphrase
        SET
        phrase= %(phrase)s,
        translation = %(translation)s,
        language = %(language)s,
        experience= %(experience)s
        WHERE id =%(id)s;
        '''
        connectToMySQL(cls.db).query_db(query,data)
        return True

    @classmethod
    def fetch_phrase_by_id(cls,id):
        data = {'id':id}
        query = '''
        SELECT * FROM userphrase 
        JOIN  user ON user.id  = userphrase.user_id 
        LEFT JOIN likes ON userphrase.id = likes.userphrase_id
        LEFT JOIN user AS users2 ON  users2.id = likes.user_id
        WHERE userphrase.id =%(id)s;
        '''
        results = connectToMySQL(cls.db).query_db(query,data)
        if results:
            this_phrase = cls(results[0])
            for row in results:
                creator = {
                    'id':row['user.id'],
                    'fullname':row['fullname'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['user.created_at'],
                    'updated_at':row['user.created_at']
                }

                likes_data ={
                    'id':row['users2.id'],
                    'fullname':row['users2.fullname'],
                    'email':row['users2.email'],
                    'password':row['users2.password'],
                    'created_at':row['users2.created_at'],
                    'updated_at':row['users2.created_at']
                }
                this_phrase.user=user.User(creator)
                this_phrase.likes.append(user.User(likes_data))
            return this_phrase
        return False

    
    @classmethod
    def fetch_phrase_by_user_id(cls,id):
        data = {'id':id}
        query = '''
        SELECT * FROM userphrase
        WHERE user_id = %(id)s;
        '''
        results = connectToMySQL(cls.db).query_db(query,data)
        all_phrases = []
        for row in results:
            this_phrase = cls(row)
            all_phrases.append(this_phrase)
        return all_phrases

    @classmethod
    def fetch_all_phrases(cls):
        query = '''
        SELECT userphrase.id,phrase,translation,language,experience,user.id AS user_id,
        userphrase.created_at,userphrase.updated_at,
        fullname,email,password,user.created_at,user.updated_at,
        COUNT(likes.userphrase_id) 
        AS likes
        FROM userphrase
        JOIN user ON userphrase.user_id = user.id
        LEFT JOIN likes ON likes.userphrase_id = userphrase.id
        GROUP BY userphrase.id
        ORDER BY likes DESC;
        '''
        results = connectToMySQL(cls.db).query_db(query)
        all_phrases = []
        for row in results:
            this_phrase = cls(row)
            user_data ={
                'id':row['user_id'],
                'fullname':row['fullname'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['user.created_at'],
                'updated_at':row['user.updated_at']
            }
            this_phrase.user = user.User(user_data)
            this_phrase.likes = row['likes']
            all_phrases.append(this_phrase)
        return all_phrases



    @classmethod
    def delete_phrase(cls,id):
        data = {'id':id}
        query = '''
        DELETE FROM userphrase
        WHERE id = %(id)s;
        '''
        return connectToMySQL(cls.db).query_db(query,data)


    @staticmethod
    def validate_phrase_form(form_data):
        is_valid = True
        if len(form_data['phrase']) < 5:
            flash('Phrase  must be atleast 5 characters')
            is_valid = False
        if len(form_data['translation']) < 2:
            flash('Translation must be atleast 5 characters')
            is_valid = False
        if len(form_data['experience']) < 4:
            flash('Experience must be atleast 4 characters')
            is_valid = False
        if len(form_data['language']) < 2 or len(form_data['language']) > 10:
            flash('Language must be at least 2 characters and less than 20')
            is_valid = False
        return is_valid




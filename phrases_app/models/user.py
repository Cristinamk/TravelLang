from phrases_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask import flash, session
from flask_bcrypt import Bcrypt        
from flask import flash,session
from phrases_app.models import user
from phrases_app import app
import re
bcrypt = Bcrypt(app)


class User:
    db = 'phrases'

    def __init__(self,data):
        self.fullname = data ['fullname']
        self.email = data ['email']
        self.password = data['password']
        self.created_at = data ['created_at']
        self.updated_at = data['updated_at']
        self.id = data ['id']

    @classmethod
    def get_user_by_email(cls,email):
        data = {'email': email }
        query = """
        SELECT *
        FROM user where email = %(email)s;
        """
        result = connectToMySQL(cls.db).query_db(query ,data)
        if result:
            result = cls(result[0])
        return result
    
    
    @classmethod
    
    def create_user(cls,data):
        if not cls.validate_user_reg_data(data):
            return False
        parsed_data = cls.parse_reg_data(data)
        query = """
        INSERT INTO user (fullname,email,password)
        VALUES (%(fullname)s ,%(email)s ,%(password)s );
        """
        user_id = connectToMySQL(cls.db).query_db(query,parsed_data)
        session['user_id'] = user_id
        session['fullname'] = f' {data["fullname"]}'
        return True
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM user where id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

#validation user
    @staticmethod
    def validate_user_reg_data(data):
        PWD_REGEX = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*?])[\w\d!@#$%^&*?]{6,12}$")
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['fullname']) < 2:
            flash("Your full name must be at least 2 characters")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']) :
            flash("Use a valid email address")
            is_valid = False
        if User.get_user_by_email(data['email']):
            flash("Thi email is already in use")
            is_valid = False
        if not PWD_REGEX.match(data['password']):
            flash("Use a valid password")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Password do not match")
            is_valid = False
        return is_valid

    @staticmethod
    def parse_reg_data(data):
        parsed_data = {}
        parsed_data['fullname'] = data['fullname']
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        parsed_data['email'] = data ['email']
        return parsed_data

    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'].lower())
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data ['password']):
                session['user_id'] = this_user.id
                session['email'] = this_user.email
                session['fullname'] = this_user.fullname
                return True
            flash ('Your login info is incorrect')
            return False
    @staticmethod
    def parse_users_registration_form_data(data):
        parsed_data = {}
        parsed_data['fullname'] = data['fullname'].strip()
        parsed_data['email'] = data['email'].lower().strip()
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data
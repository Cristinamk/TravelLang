from flask import Flask
app = Flask(__name__)
app.secret_key = 'this_is_my_super_secret_key'
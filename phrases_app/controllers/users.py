from phrases_app import app
from flask import render_template,redirect,request,session
from phrases_app.models import user,phrase

@app.route('/register')
def register():
    return render_template ('register.html')
#create users
@app.route('/users/register', methods = ['POST'])
def register_user():
    if user.User.create_user(request.form):
        return redirect ('/users/profile')
    return redirect ('/register')

@app.route('/')
def index():
    return render_template ('index.html')



@app.route('/users/profile')
def profile():
        if not session.get('user_id'): return redirect('/')
        data = {
            "id": session['user_id']
        }
        this_user = user.User.get_one(data)
        all_phrase = phrase.Userpharase.fetch_all_phrases()
        return render_template('profile.html' ,this_user = this_user,all_phrases = all_phrase )


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/login' ,methods = ['POST'])
def login():
    if user.User.login(request.form):
        return redirect('/users/profile')
    return redirect('/')
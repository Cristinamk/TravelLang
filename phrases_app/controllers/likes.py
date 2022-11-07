from phrases_app import app
from flask import render_template,redirect,request,session,flash
from phrases_app.models import user,phrase,like


@app.route('/like/<int:id>')
def like_phrase(id):
    if not session.get('user_id'):
        return redirect('/')
    if not phrase.Userpharase.fetch_phrase_by_id(id):
        flash("this phrase does not exist ")
        return redirect ('/users/profile')
    if like.Likes.if_user_liked_already(id):
        return redirect ('/users/profile')
    like.Likes.create_like(id)
    return redirect ('/users/profile')
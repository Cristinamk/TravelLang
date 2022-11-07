from phrases_app import app
import jsons
from flask import render_template,redirect,request,session,flash,jsonify
from phrases_app.models import phrase

@app.route('/new/phrase', methods=['GET','POST'])
def create_new_phrase():
    if not session.get('user_id'): return redirect('/')
    if request.method == 'GET':return render_template('create_phrase.html', data=None)
    if phrase.Userpharase.create_phrase(request.form): return redirect('/users/profile')
    return render_template('create_phrase.html', data=request.form)



@app.route('/show/<int:id>')
def show_single_phrase(id):
    # if not session.get('user_id'): return redirect('/')
    this_phrase =jsons.dump(phrase.Userpharase.fetch_phrase_by_id(id))
    # if not this_phrase:
    #     flash('This phrase does not exist')
    #     return redirect('/users/profile')
    return (this_phrase),200

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_phrase(id):
    if not session.get('user_id'):return redirect('/')
    if request.method == 'GET':
        this_phrase = phrase.Userpharase.fetch_phrase_by_id(id)
        if not this_phrase:
            flash('This tree does not exist')
            return redirect('/users/profile')
        if this_phrase.user_id == session['user_id']:return render_template('edit_phrase.html', data=this_phrase)
        flash('You are not authorized to do that!')
        return redirect('/users/profile')
    if phrase.Userpharase.update_phrase(request.form,id):return redirect('/users/profile')
    return redirect(f'/edit/{id}')


@app.route('/delete/<int:id>')
def delete_phrase(id):
    if not session.get('user_id'):return redirect('/')
    this_phrase = phrase.Userpharase.fetch_phrase_by_id(id)
    if not this_phrase:
            flash('This phrase does not exist...')
            return redirect('/dashboard')
    if this_phrase.user_id != session['user_id']:
        flash('You are not authorized to do that!')
        return redirect('/users/profile')
    phrase.Userpharase.delete_phrase(id)
    return redirect('/users/profile')
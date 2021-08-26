from werkzeug.utils import redirect
from Website.models import Note
from Website.auth import login
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Lyrics, Note, User, db
import json

views = Blueprint("views", __name__)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Note is too short", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added!", category="success")
        

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/lyrics')
def lyrics_page():
    lyrics = Lyrics.query.all()
    def make_link(title):
        return f"lyrics/{title.replace(' ', '-')}"
    def make_objlink(title):
        return title.replace(' ', '-')
    def make_title(linkedTitle):
        return linkedTitle.replace('-', ' ')
    return render_template('lyrics.html', user=current_user, lyrics=lyrics, makelink=make_link, maketitle=make_title, makeobjlink=make_objlink)

@views.route('/writelyrics', methods=["POST", "GET"])
def writelyrics_page():
    if request.method == "POST":
        title = request.form.get('title')
        type = request.form.get('type')
        reciter = request.form.get('reciter')
        topic = request.form.get('topic')
        link = request.form.get('link')
        tempo = request.form.get('tempo')
        content = request.form.get('content')

        if not title == None and not type == None and not topic == None and not tempo == None and not content == None:
            new_lyric = Lyrics(title=title, content=content, typ=type, reciter=reciter, user_id=current_user.id, topic=topic, link=link, tempo=tempo)
            db.session.add(new_lyric)
            db.session.commit()
            flash("Lyric Added!", category='success')

    return render_template('writelyrics.html', user=current_user)

@views.route("/lyrics/<lyrics_name>")
def lyricsdisplay_page(lyrics_name):
    def make_title(linkedTitle):
        return linkedTitle.replace('-', ' ')
    title = make_title(lyrics_name)
    content = Lyrics.query.filter_by(title=title).first()
    return render_template('lyricscontent.html', user=current_user, content=content, title=title)

@views.route('/delete-lyric/<lyric_title>')
def delete_lyric(lyric_title):
    def make_title(linkedTitle):
        return linkedTitle.replace('-', ' ')
    lyric_title = make_title(lyric_title)
    lyric = Lyrics.query.filter_by(title=lyric_title).first()
    db.session.delete(lyric)
    db.session.commit()
    return redirect('/lyrics')

@views.route('/checkid')
def checkid_page():
    users = User.query.all()
    return render_template('checkid.html', user=current_user, users=users)

@views.route('/search-lyrics')
def search_lyrics():
    if request.method == "GET":
        column = request.form.get('searchcol')
        column_content = request.form.get('searchcol-content')
        entries = Lyrics.query.filter_by(column=column_content)
    
    return render_template('searchlyrics.html', user=current_user, entries=entries)
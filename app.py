from flask import Flask, request, render_template, abort, send_file, jsonify
import os
from pathlib import Path

app = Flask(__name__)
app.config.from_pyfile( 'app.config' );
MOVIES_ROOT = app.config['MOVIES_ROOT']

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get_movies_list')
def get_movies_list():
    movies = []

    for root, dirs, files in os.walk(MOVIES_ROOT):
        for file in files:
            if Path(file).suffix == '.mp4':
                movies.append({
                    'title': file[:file.rfind('.')],
                    'folder': root[len(MOVIES_ROOT)+1:],
                    'file': file
                })

    return jsonify(movies)

@app.route('/movie')
def movie():
    title = request.args.get('title')
    folder = request.args.get('folder')
    file = request.args.get('file')

    if not folder or not file:
        abort(400)

    movie_path = os.path.join(MOVIES_ROOT, folder, file)

    if not os.path.isfile(movie_path):
        abort(404)

    return render_template( 'player.html', title=title, folder=folder, file=file )

@app.route('/stream')
def stream():
    folder = request.args.get('folder')
    file = request.args.get('file')

    movie_path = os.path.join(MOVIES_ROOT, folder, file)

    if not os.path.isfile(movie_path):
        abort(404)

    return send_file(
        movie_path,
        mimetype='video/mp4',
        conditional=True
    )

@app.route('/subtitles')
def subtitles():
    folder = request.args.get('folder')
    file = request.args.get('file')

    path = os.path.join(MOVIES_ROOT, folder, file)

    if not os.path.isfile(path):
        abort(404)

    return send_file(
        path,
        mimetype='text/vtt'
    )

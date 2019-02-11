import os

from flask import Flask, render_template, request, send_from_directory, redirect
from flask_socketio import SocketIO
from inspect import getmembers
from pprint import pprint
from werkzeug.utils import secure_filename
from .lib.video import Video
from .config import endpoints_config

app = Flask(__name__, static_folder=os.getcwd() + '/videos', template_folder=os.getcwd() + '/app/templates')
socketio = SocketIO(app)

@app.route("/")
def index():
    return redirect('/upload')

@app.route('/upload', methods = ['GET', 'POST'])
def video_upload():
	""" realiza o upload de video para diretorio da aplicação para corte """
	if request.method == 'POST':

		file = request.files['video_file']

		file_name = secure_filename(file.filename)

		file_only_name, file_ext = os.path.splitext(file_name)

		if not file_ext == '.mp4':
			return render_template('upload.html', msg='Invalid extension, please select only MP4 videos')
		
		video_full_path = os.path.abspath(os.path.join("videos", file_name))

		file.save(video_full_path)

		video_information = Video(video_full_path)

		video_duration = video_information.get_video_duration_tuple()

		return render_template('upload.html', msg='Upload is done', video=file_name, duration=video_duration)
	else:
		return render_template('upload.html')

@socketio.on('addfile')
def add_file(json, methods=['GET', 'POST']):
	""" grava um arquivo txt com as informações do video """
	txt_full_path = os.path.abspath(os.path.join("files", json.get('filename')))
	
	f = open(txt_full_path+'.txt', 'a+')
	
	cut_list = json.get('cuts')

	for cut in cut_list:
		f.write(cut.get('start_time')+';'+cut.get('end_time')+';'+cut.get('title')+'\n') 

	f.close()

	socketio.emit('added_to_file', json)

def start():
	
	print('Iniciado serviço de interface admin para edição de videos')

	socketio.run(app, host=endpoints_config['web_host'], port=endpoints_config['web_port'], debug=True)
	


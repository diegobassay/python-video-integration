import os
import subprocess

from flask import Flask, render_template, request
from flask_classy import FlaskView, route
from inspect import getmembers
from pprint import pprint

app = Flask(__name__)

class ApiView(FlaskView):
	route_base = '/'
	@route('/')
	def index(self):
		return 'Api Globo.com'
	 
	@route('/cutvideo', methods=['POST'])
	def exec_cut_video(self):
		#subprocess.call('ls -la', shell=True)
		
		print('Recebendo request pelo consumidor do RabittMQ')
		pprint(request.form)
		
		cut_data = request.form
		filename = cut_data.get('filename')
		title = cut_data.get('title')
		start_time = cut_data.get('start_time')
		end_time = cut_data.get('end_time')

		dir_videos = os.getcwd() + '/videos'
		file_target = dir_videos + '/' + filename
		dir_cut_name = filename.replace('.mp4', '')
		path_dir_cut_name = dir_videos + '/' + dir_cut_name

		if not os.path.exists(path_dir_cut_name):
			os.makedirs(path_dir_cut_name)

		file_cutted_with_title = path_dir_cut_name + '/' + title + '.mp4' 

		result = subprocess.check_output(['ffmpeg', '-i', file_target, '-ss', start_time, '-to', end_time, '-c', 'copy', file_cutted_with_title])

		return result

ApiView.register(app)

def start():
	
	print('Iniciado serviço da api Globo que cortará os videos.')

	app.run(host='0.0.0.0', port=5000, debug=True)
import os
import pika
import json
import requests
from .config import endpoints_config

def processing_video_cut(ch, method, properties, body):
	"""Invocado pelo consumidor assim que é detectado um objeto na fila do RabbitMQ"""
	data = json.loads(body)

	end_point_cut = 'cutvideo'

	url_to_cut = 'http://{}:{}/{}'.format(endpoints_config['api_host'],endpoints_config['api_port'],end_point_cut)
	
	r = requests.post(url_to_cut, data)

	print(r.text)

class Consumer:
	
	def __init__(self):
		"""inicia conexão com RabbitMQ para consumir mensagens publicadas pelo watcher"""
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=endpoints_config['rabbit_host']))
		
		self.channel = self.connection.channel()
		
		self.channel.queue_declare(queue=endpoints_config['rabbit_topic'])
		
		self.channel.basic_consume(processing_video_cut, queue=endpoints_config['rabbit_topic'],no_ack=True)

	def run(self):
		
		self.channel.start_consuming()

def start():
	
	print('Iniciado consumer que receberá as informações para corte.')

	consumer = Consumer()
	
	consumer.run()
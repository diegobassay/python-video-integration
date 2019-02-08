import os
import pika
import json
import time
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from inspect import getmembers
from pprint import pprint
from werkzeug.utils import secure_filename
from .lib.video import Video
from .config import endpoints_config

class Watcher:
    """essa classe possui os comportamentos necessários aos eventos de um determinado diretório"""
    dir_files_videos_to_cut = os.getcwd() + endpoints_config['dir_txt']

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.dir_files_videos_to_cut, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Ocorreu um erro")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        """se qualquer arquivo for adicionado ou modificado no diretorio escolhido o listenner inicia essa funcao"""
        
        #print(dir(event))
        #pprint(getmembers(event))

        file_name = os.path.basename(event.src_path)

        file_name_video = file_name.replace('.txt', '')

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=endpoints_config['rabbit_host']))
        
        channel = connection.channel()

        channel.queue_declare(queue=endpoints_config['rabbit_topic'])

        file_received = open(event.src_path, "r")

        for cut_line in file_received:

            cut_information = cut_line.split(';')

            cut_data = {
                'filename': file_name_video,
                'start_time': cut_information[0],
                'end_time': cut_information[1],
                'title': secure_filename(cut_information[2])
            }

            message_cut_data = json.dumps(cut_data)
            
            print("Publicando mensagem de corte de video no RabbitMQ")

            channel.basic_publish(exchange='', routing_key=endpoints_config['rabbit_topic'], body=message_cut_data)
        
        connection.close()

        file_received.close()

def start():

    print('Iniciado serviço para enviar os arquivos para fila de corte.')
    
    w = Watcher()
    
    w.run()
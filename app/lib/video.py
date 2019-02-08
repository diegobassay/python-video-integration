import os
from pymediainfo import MediaInfo
from inspect import getmembers
from pprint import pprint

class Video:
    """Usada para obter informações de video através do PyMedia"""
    def __init__(self, path):
        if os.path.isfile(path):
            self.path = path
            self.info = MediaInfo.parse(self.path)
        else:
            raise FileNotFoundError

    def get_video_track(self):
        """Retorna o primeiro track encontrado no video"""
        for track in self.info.tracks:
            if track.track_type == 'Video':
                return track
        return None

    def get_audio_tracks(self):
        """Retorna todos os audio tracks do video"""
        array_tracks = []
        for track in self.info.tracks:
            if track.track_type == 'Audio':
                array_tracks.append(track)
        return array_tracks

    def get_audio_mapping(self):
        """Retorna os canais de audo"""
        array_audio = []
        for track in self.get_audio_tracks():
            array_audio.append(track.channel_s)
        return array_audio
    
    def get_video_duration_miliseconds(self):
        """Retona a duração do video em milisegundos"""
        track = self.get_video_track()
        return track.duration

    def show_info(self):
        """Imprime informações sobre primeiro indice"""
        pprint(getmembers(self.info.tracks.index(0)))

    def get_video_duration_tuple(self):
            """Retorna as informações de duração do video em uma tupla"""
            duration = self.get_video_duration_miliseconds()

            millis = int(duration)
            seconds=(millis/1000)%60
            seconds = int(seconds)
            minutes=(millis/(1000*60))%60
            minutes = int(minutes)
            hours=(millis/(1000*60*60))%24

            hours = "%d" % hours if hours > 9 else "0%d" % hours
            minutes = "%d" % minutes if minutes > 9 else "0%d" % minutes
            seconds = "%d" % seconds if seconds > 9 else "0%d" % seconds
            #print ("%s:%s:%s" % (hours, minutes, seconds))
            return (hours, minutes, seconds)


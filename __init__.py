from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.audioservice import AudioService

import requests


URLS = {
    "rro" : "http://streaming.swisstxt.ch/m/rro/aac_32"

}

def getURL(message):
    default = URLS["rro"] #default value
    for url in URLS:
        if url in message: 
            return URLS[url]
    return default

def find_mime(url):
    mime = 'audio/mpeg'
    response = requests.Session().head(url, allow_redirects=True)
    if 200 <= response.status_code < 300:
        mime = response.headers['content-type']
    return mime
class RadioPlayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):
        self.audio_service = AudioService(self.bus)

    @intent_file_handler('player.radio.intent')
    def handle_player_radio(self, message):
        self.speak_dialog('player.radio')

        url = getURL(message)
        mime = find_mime(url)
        backends = self.audio_service.available_backends()
        self.log.debug(backends)
        self.audio_service.play( (url, mime) )



def create_skill():
    return RadioPlayer()


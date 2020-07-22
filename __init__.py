from mycroft import MycroftSkill, intent_file_handler
from mycroft.audio.services.vlc import VlcService

import json

#SRF data from: https://www.broadcast.ch/fileadmin/kundendaten/Dokumente/Internet_Streaming/2020_06_links_for_streaming_internet_radio_de_fr_it_V006.pdf.pdf 
URLS = {}

def getURL(message=None):
    #radio_urls.json in format: "name of radio, all matching descriptions" : "actual_url"
    with open(file="radio_urls.json", mode='r') as file:
        URLS = json.load(file)
    default = URLS["default"] #default value

    radio = message.data.get("radio").lower()
    #TODO better recognition of radio, tty with from mycroft.util.parse import fuzzy_match
    if message: 
        for url in URLS:
            for word in message.data["utterance"].lower().split(): 
                if word in url.lower():
                    return URLS[url]
    return default

class RadioPlayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.mediaplayer = VlcService(config={'low_volume': 10, 'duck': True})
        self.recent_radiochannel = ''

    def play(self, message):
        tracklist = []
        url = getURL(message)
        self.recent_radiochannel = url
        self.log.info('URL: {}'.format(url))
        tracklist.append(url)
        self.mediaplayer.add_list(tracklist)
        self.mediaplayer.play()

    def stop(self):
        self.mediaplayer.stop()
        self.mediaplayer.clear_list()




    @intent_file_handler('radio.start.intent')
    def start_radio(self, message):
        self.speak_dialog('radio.start')
        self.play(self, message)

    @intent_file_handler('radio.stop.intent')
    def stop_radio(self, message):
        self.stop(self)
        self.speak_dialog('radio.stop')

    @intent_file_handler('radio.switch.intent')
    def switch_radio(self, message):
        if (self.mediaplayer.is_playing):
            self.stop(self)
        self.speak_dialog('radio.switch')
        self.play(self, message)

    @intent_file_handler('radio.pause.intent')
    def pause_radio(self, message):
        if (self.mediaplayer.is_playing):
            self.mediaplayer.pause() # only stop not clear playlist
            self.speak_dialog('radio.pause')

    @intent_file_handler('radio.resume.intent')
    def resume_radio(self, message):
        self.speak_dialog('radio.resume')
        try:
            self.mediaplayer.resume()
            self.log.info('Resume radio failed, try with recent_radiochannel!')
        except:
            self.mediaplayer.play(self.recent_radiochannel)




def create_skill():
    return RadioPlayer()


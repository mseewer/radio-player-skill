from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.audioservice import AudioService
from mycroft.audio.services.vlc import VlcService



#SRF data from: https://www.broadcast.ch/fileadmin/kundendaten/Dokumente/Internet_Streaming/2020_06_links_for_streaming_internet_radio_de_fr_it_V006.pdf.pdf 
URLS = {
    "rro" : "http://streaming.swisstxt.ch/m/rro/aac_32", 
    "srf3": "http://stream.srg-ssr.ch/drs3/aacp_96.m3u"

}

def getURL(message=None):
    default = URLS["rro"] #default value
    if message: 
        for url in URLS:
            if url.lower() in message.data["utterance"].lower():
                return URLS[url]
    return default

class RadioPlayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.mediaplayer = VlcService(config={'low_volume': 10, 'duck': True})


    @intent_file_handler('player.radio.intent')
    def handle_player_radio(self, message):
        self.speak_dialog('player.radio')
        tracklist = []
        url = getURL(message)
        self.log.info('URL: {}'.format(url))
        tracklist.append(url)
        self.mediaplayer.add_list(tracklist)
        self.mediaplayer.play()

    @intent_file_handler('radio.stop.intent')
    def stop(self):
        self.mediaplayer.stop()
        self.mediaplayer.clear_list()




def create_skill():
    return RadioPlayer()


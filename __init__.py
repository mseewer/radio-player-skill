from mycroft import MycroftSkill, intent_file_handler

import vlc


class RadioPlayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('player.radio.intent')
    def handle_player_radio(self, message):
        self.speak_dialog('player.radio')
        url = 'http://streaming.swisstxt.ch/m/rro/aac_32'

        #define VLC instance
        instance = vlc.Instance()

        #Define VLC player
        player=instance.media_player_new()

        #Define VLC media
        media=instance.media_new(url)

        #Set player media
        player.set_media(media)

        #Play the media
        player.play()
        input()


def create_skill():
    return RadioPlayer()


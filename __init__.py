from mycroft import MycroftSkill, intent_file_handler


class RadioPlayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('player.radio.intent')
    def handle_player_radio(self, message):
        self.speak_dialog('player.radio')


def create_skill():
    return RadioPlayer()


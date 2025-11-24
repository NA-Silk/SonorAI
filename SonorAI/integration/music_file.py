class MusicFile:
    def __init__(self, title, instrument_type, music_xml_path, user):
        self.title = title
        self.instrument_type = instrument_type
        self.music_xml_path = music_xml_path
        self.user = user

    def __str__(self):
        return self.title

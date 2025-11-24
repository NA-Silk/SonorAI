from .music_file import MusicFile

class MyFilesPage:
    MAX_FILES = 10

    def __init__(self, user):
        self.user = user
        self.music_files = {}

    def listMusicFiles(self):
        return list(self.music_files.values())

    def createMusicFile(self, music_file):
        if len(self.music_files) >= self.MAX_FILES:
            raise ValueError("File limit reached (10 files).")
        self.music_files[music_file.title] = music_file

    def readMusicFile(self, title):
        return self.music_files.get(title)

    def updateMusicFile(self, old_title, new_title):
        mf = self.music_files.pop(old_title)
        mf.title = new_title
        self.music_files[new_title] = mf

    def deleteMusicFile(self, title):
        self.music_files.pop(title, None)

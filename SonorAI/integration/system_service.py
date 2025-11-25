from ..aiapp import AudioAnalysis
from .user_classes import User, Admin
from .music_file import MusicFile
from .myfiles_page import MyFilesPage


class SonorAISystem:
    """
    Main class that connects the users, files, and AI.
    """
    def __init__(self):
        self.users = {}          # username -> User/Admin
        self.myfiles_pages = {}  # username -> MyFilesPage

    # USER FUNCTIONS

    def register_user(self, username, first_name, last_name, email, password):
        user = User(username, first_name, last_name, email, password)
        self.users[username] = user
        self.myfiles_pages[username] = MyFilesPage(user)
        return user

    def register_admin(self, username, first_name, last_name, email, password):
        admin = Admin(username, first_name, last_name, email, password)
        self.users[username] = admin
        self.myfiles_pages[username] = MyFilesPage(admin)
        return admin

    def get_user(self, username):
        return self.users.get(username)

    def delete_user(self, username):
        # removes user + their files
        self.users.pop(username, None)
        self.myfiles_pages.pop(username, None)

    # FILE / AI FUNCTIONS

    def generate_and_save_music_file(self, username, instrument_type, audio_file_path, title):
        """
        Runs AI, makes a MusicXML file, and returns the MusicXML text.

        If the username exists inside this system, it also creates a MusicFile
        object and stores it on that user's MyFilesPage. This part is optional
        and does not affect Django.
        """
        output_path = "out.musicxml"

        # Use the AI from aiapp.py
        AudioAnalysis.audio_analysis(
            audio_file=audio_file_path,
            output_path=output_path,
            title=title,
        )

        # Try to keep your in memory structure in sync (optional)
        user = self.get_user(username)
        if user:
            myfiles = self.myfiles_pages.get(username)
            if myfiles is None:
                myfiles = MyFilesPage(user)
                self.myfiles_pages[username] = myfiles

            music_file = MusicFile(title, instrument_type, output_path, user)
            myfiles.createMusicFile(music_file)

        # Always return the MusicXML contents so Django can use it
        with open(output_path, "r", encoding="utf-8") as f:
            musicxml = f.read()

        return musicxml

    def list_user_files(self, username):
        myfiles = self.myfiles_pages.get(username)
        if not myfiles:
            return []
        return myfiles.listMusicFiles()

    def rename_user_file(self, username, old_title, new_title):
        myfiles = self.myfiles_pages.get(username)
        if not myfiles:
            raise ValueError("User not found.")
        myfiles.updateMusicFile(old_title, new_title)

    def delete_user_file(self, username, title):
        myfiles = self.myfiles_pages.get(username)
        if not myfiles:
            raise ValueError("User not found.")
        myfiles.deleteMusicFile(title)

    def favorite_user_file(self, username, title, favorite=True):
        myfiles = self.myfiles_pages.get(username)
        if not myfiles:
            raise ValueError("User not found.")
        mf = myfiles.readMusicFile(title)
        if mf:
            mf.favorite = favorite

    # ADMIN OPTIONS  

    def admin_delete_user(self, admin_username, target_username):
        admin = self.get_user(admin_username)
        if not admin or not admin.is_superuser:
            raise PermissionError("Only admins can do this.")
        self.delete_user(target_username)

    def admin_list_users(self, admin_username):
        admin = self.get_user(admin_username)
        if not admin or not admin.is_superuser:
            raise PermissionError("Only admins can do this.")
        return list(self.users.values())


system = SonorAISystem()

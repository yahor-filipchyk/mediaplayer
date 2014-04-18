from apps.mediaplayer.OSMediaPlayer import OSMediaPlayer
import subprocess
import os


class MPlayer(OSMediaPlayer):

    def __init__(self, file_or_folder):
        if os.path.isdir(file_or_folder):
            self.play_folder(file_or_folder)
        else:
            self.play_file(file_or_folder)

    def play_file(self, file, file_type=OSMediaPlayer.TYPE_MUSIC):
        self.

    def play_folder(self, folder, files_type=OSMediaPlayer.TYPE_MUSIC):
        pass

    def play_pause(self):
        pass

    def next(self):
        pass

    def previous(self):
        pass

    def volume_up(self):
        pass

    def volume_down(self):
        pass

    def get_current_file(self):
        pass

    def get_current_folder(self):
        pass
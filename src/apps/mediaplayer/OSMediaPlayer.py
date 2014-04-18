

class OSMediaPlayer(object):

    TYPE_MUSIC = "music"
    TYPE_VIDEO = "video"

    def __init__(self, file_or_folder):
        pass

    def play_file(self, file, file_type=TYPE_MUSIC):
        pass

    def play_folder(self, folder, files_type=TYPE_MUSIC):
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
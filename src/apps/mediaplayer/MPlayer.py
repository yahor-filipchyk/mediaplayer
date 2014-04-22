from apps.mediaplayer.OSMediaPlayer import OSMediaPlayer
from subprocess import Popen, PIPE, SubprocessError, TimeoutExpired
import os
import re
import threading


class MPlayer(OSMediaPlayer):

    def __init__(self):
        self.player = None
        self.current_file = None
        self.current_folder = None
        self.lock = None
        self.updated = False

    def play(self, file, file_type=OSMediaPlayer.TYPE_MUSIC):
        self.stop()
        args = ["mplayer"]
        if file_type == OSMediaPlayer.TYPE_VIDEO:
            args.append("-fs")
        args.append("-loop")
        args.append("0")
        if os.path.isdir(file):
            files = os.listdir(file)
            for music_file in files:
                if re.match(".*\.(mp3|wma|flv|wmv|avi)", music_file):
                    args.append(os.path.join(file, music_file))
                    if self.current_file is None:
                        self.current_file = music_file
            self.current_folder = file
        else:
            args.append(file)
            self.current_file = file
        print(args)
        self.player = Popen(args, stdin=PIPE, stdout=PIPE, universal_newlines=True)
        t = threading.Thread(target=self.get_current_playing)
        t.setDaemon(True)
        t.start()
        self.lock = threading.Lock()
        # self.current_file = self.get_current_playing()

    def play_pause(self):
        self.player.stdin.write("p")

    def stop(self):
        if self.player is not None:
            try:
                # if not self.player.poll():
                self.player.communicate("q")
                # self.player.kill()
            except SubprocessError:
                print("Cannot stop playing the file")
            finally:
                self.player = None
                self.current_file = None
                self.current_folder = None

    def next(self):
        if self.current_folder is None:
            return
        self.player.stdin.write(">")
        self.wait_for_update()

    def previous(self):
        if self.current_folder is None:
            return
        self.player.stdin.write("<")
        self.wait_for_update()

    def volume_up(self):
        self.player.stdin.write("*")

    def volume_down(self):
        self.player.stdin.write("/")

    def get_current_file(self):
        return self.current_file

    def get_current_folder(self):
        return self.current_folder

    def wait_for_update(self):
        self.lock.acquire()
        self.updated = False
        self.lock.release()
        while not self.updated:
            pass

    def get_current_playing(self):
        while self.player is not None and not self.player.poll():
            try:
                line = self.player.stdout.readline()
            except UnicodeDecodeError:
                line = ""
            m = re.search("Playing .*/(.*\.(mp3|wma|avi|flv|wmv))", line)
            if m is not None:
                print("FOUND: " + m.group(1))
                self.lock.acquire()
                self.current_file = m.group(1)
                self.updated = True
                self.lock.release()
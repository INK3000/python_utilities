#!/usr/bin/python
# версия с классом
import os
import subprocess
import time

def init_generator(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g
    return inner


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        print('{:.2f} sec'.format(time.perf_counter()-start))
    return wrapper

def sec_to_hms(seconds):
    h = seconds//3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)

class VideoFile:
    total_duration = 0
    total_count = 0
    instance = ()
    def __init__(self, root, filename):
        self.filename = filename
        self.root = root
        self.duration = self.get_duration()
        VideoFile.instance += (self,)
        VideoFile.total_duration += self.duration
        VideoFile.total_count += 1


    def get_duration(self):
            full_path = os.path.join(self.root, self.filename)
            cmd = 'ffprobe -i \'{}\' -show_entries format=duration -v quiet -of csv="p=0"'.format(full_path)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, universal_newlines=True)
            # output = p.stdout.read().decode().split()
            stdout, stderr = p.communicate()
            duration = int(float(stdout))
            return duration



    def __repr__(self):
        return ('File "{}" - Duration: {}'.format(self.filename, sec_to_hms(self.duration)))

    def __str__(self):
        return ('File "{}" - Duration: {}'.format(self.filename, sec_to_hms(self.duration)))

    def __len__(self):
        return self.duration

@init_generator
def print_video_info():
    try:
        while True:
            videofile = yield
            print(videofile)
    except GeneratorExit:
        print ('Total files: {}. Total duration: {}'.format(VideoFile.total_count, sec_to_hms(VideoFile.total_duration)))



@timer
def find_videos():
    video_extensions = ('mp4', 'avi')
    # videos = []
    for root, subfolders, files in os.walk(os.getcwd()):
        for file in files:
            if  file.split('.')[-1] in video_extensions:
                full_path = os.path.join(root, file)
                videofile = VideoFile(root,file)
                printer.send(videofile)
    printer.close()
    return VideoFile.instance

if __name__ == '__main__':
    printer = print_video_info()
    find_videos()

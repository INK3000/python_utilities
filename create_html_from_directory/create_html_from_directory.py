#!/usr/bin/python
import os
from datetime import datetime
import pytz
from pymediainfo import MediaInfo
import time
import jinja2
import jj2_templates



def stopwatch(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Время выполнения {end - start:.2f} сек.')
        return result

    return wrapper


class VideoFile:
    path = root = directory_key = None
    _total_duration = None
    _total_count = None
    instance = ()
    error_instance = ()
    video_files_dict = dict()

    def __init__(self, filename):
        self.filename = filename
        self.root = VideoFile.root
        self.full_path = os.path.join(self.root, self.filename)
        self.relpath = os.path.relpath(self.full_path, VideoFile.path)
        self.duration = 0

        # MediaInfo ver.
        try:
            media_info = MediaInfo.parse(self.full_path)
            for track in media_info.tracks:
                if track.track_type == "Video":
                    self.duration = int(track.duration * 0.001)
        except Exception as e:
            print(e)

        if not VideoFile.video_files_dict.get(VideoFile.directory_key):
            VideoFile.video_files_dict[VideoFile.directory_key] = list()
        VideoFile.video_files_dict[VideoFile.directory_key].append(self)

        VideoFile.instance += (self,)
        VideoFile._total_duration = None
        VideoFile._total_count = None


    @classmethod
    @property
    def total_duration(cls):
        if not cls._total_duration:
            cls._total_duration = sum(cls.instance)
        return cls._total_duration

    @classmethod
    @property
    def total_count(cls):
        if not cls._total_count:
            cls._total_count = len(cls.instance)
        return cls._total_count



    def __repr__(self):
        return 'File "{}" - Duration: {}'.format(self.filename, sec_to_hms(self.duration))

    def __str__(self):
        return 'File "{}\n{}" - Duration: {} \n\n'.format(self.root, self.filename, sec_to_hms(self.duration))

    def __len__(self):
        return self.duration

    def __add__(self, object):
        if isinstance(object, VideoFile):
            result = self.duration + object.duration
        elif isinstance(object, (int,float)):
            result = self.duration + object
        else:
            result = self.duration
        return result

    def __radd__(self, object):
        if object == 0:
            return self
        else:
            return self.__add__(object)


def sec_to_hms(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)


def write_to_file(path, filename, text='', flag='w'):
    full_path = os.path.join(path, filename)
    with open(full_path, flag, encoding="utf-8") as file:
        file.write(text)


def create_video(files):
    video_format = list(('mp4', 'avi', 'mpg'))
    video_files = []
    video_files_dict = dict()

    for file in sorted(files):
        if file.split('.')[-1] in video_format:
            video = VideoFile(file)
            print(f'{video.filename} [{VideoFile.root}]')
    

def get_video_files_to_dict(path):
    root, directories, files = next(os.walk(path))  # for get root_lvl directories and root_lvl files

    if files:  # in root
        VideoFile.root = root
        VideoFile.directory_key = root
        VideoFile.path = path
        create_video(files)
    if directories:  # in root
        for directory in sorted(directories):
            for root, dirs, files in os.walk(directory):
                VideoFile.root = root
                VideoFile.directory_key = directory
                VideoFile.path = path
                create_video(files)


@stopwatch
def main():
    current_directory = os.getcwd()
    get_video_files_to_dict(path=current_directory)
    print(f'Total duration: {sec_to_hms(VideoFile.total_duration)}')

    env = jinja2.Environment(loader=jinja2.PackageLoader('jj2_templates'), autoescape=True)
    template = env.get_template('category.html')
    html = template.render(os=os,
                           video_files_dict=VideoFile.video_files_dict,
                           path=os.path.basename(current_directory),
                           total_duration=sec_to_hms(VideoFile.total_duration),
                           hms=sec_to_hms)

    write_to_file(current_directory, 'video_index.html', html, 'w')

    if VideoFile.error_instance:
        current_time = pytz.utc.localize(datetime.utcnow()).astimezone().isoformat()
        write_to_file(current_directory, 'error.txt', current_time + '\n', 'w')
        for file in VideoFile.error_instance:
            write_to_file(current_directory, 'error.txt', str(file) + '\n', 'a')


if __name__ == '__main__':
    main()

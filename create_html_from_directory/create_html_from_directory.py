#!/usr/bin/python
import os
import subprocess
from datetime import datetime
import pytz
from pymediainfo import MediaInfo
import time
from pprint import pprint
import jinja2
import jj2_templates
import pathlib
def stopwatch(func):
    def wrapper (*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print (f'Время выполнения {end-start:.2f} сек.')
        return result
    return wrapper


class VideoFile:
    total_duration = 0
    total_count = 0
    instance = ()
    error_instance =()
    def __init__(self, root, filename, path):
        self.filename = filename
        self.root = root
        self.full_path = os.path.join(self.root, self.filename)
        self.relpath = os.path.relpath(self.full_path, path)
        self.duration = self.get_duration()
        VideoFile.instance += (self,)
        VideoFile.total_duration += self.duration
        VideoFile.total_count += 1


    def get_duration(self):
        full_path = os.path.join(self.root, self.filename)
        result = 0
        media_info = MediaInfo.parse(full_path)
        for track in media_info.tracks:
            if track.track_type == "Video":
                result = int(track.duration*0.001)
        return result



    def __repr__(self):
        return ('File "{}" - Duration: {}'.format(self.filename, sec_to_hms(self.duration)))

    def __str__(self):
        return ('File "{}\n{}" - Duration: {} \n\n'.format(self.root, self.filename, sec_to_hms(self.duration)))

    def __len__(self):
        return self.duration


def sec_to_hms(seconds):
    h = seconds//3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)


def create_directory(path,name):
    directory_path = os.path.join(path,name)
    try:
        os.mkdir(directory_path)
    except FileExistsError:
        print(f'Директория {directory_path} уже существует.\nПродолжаю выполнять задачу...')
    return directory_path

def write_to_file(path,filename,text='', flag='w'):
    full_path = os.path.join(path, filename)
    with open(full_path, flag) as file:
        file.write(text)
        

def get_videofiles(path):
    video_files = []
    video_files_dict = dict()
    parent_root = None
    video_format = list(('mp4', 'avi', 'mpg'))
    
    for root, directory, files in os.walk(path):
        p = pathlib.PurePath(root)
        level = root.replace(path, '').count(os.sep)
        temp_video_files = []
        for file in sorted(files):
            if file.split('.')[-1] in video_format:
                video = VideoFile(root, file, path)
                temp_video_files.append(video)
                print (f'{video.relpath} [{sec_to_hms(video.duration)}]')


        if temp_video_files:
            if not parent_root :
                parent_root = root

            if not p.is_relative_to(parent_root) or parent_root == path:
                # video_files_dict.update({parent_root: video_files})
                # html_body += template.render(level=level, root=os.path.basename(parent_root), video_files=video_files)     
                video_files = temp_video_files
                parent_root = root
            else:
                video_files.extend(temp_video_files)
        if video_files:
            video_files_dict.update({parent_root: video_files})
            # html_body += template.render(level=level, root=os.path.basename(parent_root), video_files=video_files)     
    return video_files_dict



@stopwatch
def main():

    cwd = os.getcwd()
    # subdirs = [entry.path for entry in os.scandir(cwd)]
    # subdirs_basename = [os.path.basename(dir) for dir in subdirs]

    env = jinja2.Environment(loader=jinja2.PackageLoader('jj2_templates'), autoescape=True)
    template = env.get_template('category.html')

    # rendered = template.render(current_path=os.path.basename(cwd), subdirs=subdirs_basename)

    video_files_dict = get_videofiles(cwd)
    print(f'Total duration: {sec_to_hms(VideoFile.total_duration)}')
    html = template.render(os=os,
                                video_files_dict=video_files_dict,
                                path=os.path.basename(cwd),
                                total_duration=sec_to_hms(VideoFile.total_duration),
                                hms=sec_to_hms)     
  

    write_to_file(cwd, 'video_index.html', html, 'w')

    if VideoFile.error_instance:
        current_time = pytz.utc.localize(datetime.utcnow()).astimezone().isoformat()
        write_to_file(cwd, 'error.txt', current_time+'\n','w')
        for file in VideoFile.error_instance:
            write_to_file(cwd, 'error.txt', str(file)+'\n', 'a')

   


if __name__ == '__main__':
    main()
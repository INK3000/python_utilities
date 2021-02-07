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
    def __init__(self, root, filename):
        self.filename = filename
        self.root = root
        self.full_path = os.path.join(self.root, self.filename)
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


html_head = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
    <title>Видеофайлы из директории</title>
</head>
<body>
"""



html_foot = """
</body>
</html>
""" 

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
        

def fill_html_body(path_list):
    html_body = ''
    video_format = list(('mp4', 'avi', 'mpg'))
    for path in path_list:
        for root, directory, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            root_name = os.path.basename(root)

            for file in sorted(files):
                if file.split('.')[-1] in video_format:
                    video = VideoFile(root, file)
                    # print(video)
                    html_body += str(video.filename)
    #                 videos_html += f'''<div>
    #                             <a class="px-{level+2}" target="_blank" href="{video.full_path}">{video.filename} [{sec_to_hms(video.duration)}]</a>
    #                             </div>'''
    #         if not founded_files[root]:
    #             del founded_files[root]
    #         if videos_html:
    #             html_body += videos_html

    #     if html_body:    
    #         html_body = f'''<div class="container">
    #                         <div class="row py-3">
    #                         <div class="col-12 px-{level}">
    #                         <p>{root_name}</p>''' + html_body + '</div></div></div>'

    # #добавить общее время в конце страницы        
    # html_body = f"""<div class="container">
    #                 <div class="row py-3">
    #                    <div class="col">
    #                 <h3>{sec_to_hms(VideoFile.total_duration)}</h3>
    #                 </div></div></div>
    #             """ + html_body
    return html_body



@stopwatch
def main():

    cwd = os.getcwd()
    subdirs = [entry.path for entry in os.scandir(cwd)]
    subdirs_basename = [os.path.basename(dir) for dir in subdirs]

    env = jinja2.Environment(loader=jinja2.PackageLoader('jj2_templates'), autoescape=True)
    template = env.get_template('category.html')

    rendered = template.render(current_path=os.path.basename(cwd), subdirs=subdirs_basename)

    print(subdirs)

    write_to_file(cwd, 'video_index.html', rendered, 'w')

    if VideoFile.error_instance:
        current_time = pytz.utc.localize(datetime.utcnow()).astimezone().isoformat()
        write_to_file(cwd, 'error.txt', current_time+'\n','w')
        for file in VideoFile.error_instance:
            write_to_file(cwd, 'error.txt', str(file)+'\n', 'a')

   


if __name__ == '__main__':
    main()
#!/usr/bin/python
import os
import subprocess
import time 

def stopwatch(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args,**kwargs)
        end = time.perf_counter()
        print(f'Время выполнения {end-start:.2f} сек.')
        return result
    return wrapper


class VideoFile:
    total_duration = 0
    total_count = 0
    instance = ()
    def __init__(self, root, filename):
        self.filename = filename
        self.root = root
        self.duration = self.get_duration()
        self.full_path = os.path.join(self.root, self.filename)
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


html_head = """
<!DOCTYPE html>
<html>
<head>
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

def get_files(path):
	result = os.walk(os.getcwd())
	return result


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

def write_html(path,filename,html_body=''):
	full_path = os.path.join(path, filename)
	with open(full_path,'w') as html_file:
		html_file.write(html_head)
		html_file.write(html_body)
		html_file.write(html_foot)

def fill_html_body(files):
	html_body = ''
	video_format = list(('mp4', 'avi', 'mpg'))
	for root, directory, files in sorted(files):
		videos_html = ''
		for file in files:
			if file.split('.')[-1] in video_format:
				video = VideoFile(root, file)
				print(video)
				videos_html += f'''<a class="px-5" target="_blank" href="{video.full_path}">{video.filename} [{sec_to_hms(video.duration)}]</a>'''
		if videos_html:
			root_name = root.split('/')[-1]
			html_body += """<div class="container">"""
			html_body +="""<div class="row py-3">
					   <div class="col">"""
			html_body += f'''<p>{root_name}</p>'''
			html_body += videos_html
			html_body += '</div></div></div>'
	#добавить общее время в конце страницы		
	html_body = f"""<div class="container">
					<div class="row py-3">
			   		<div class="col">
					<h3>{sec_to_hms(VideoFile.total_duration)}</h3>
					</div></div></div>
				""" + html_body
	return html_body



@stopwatch
def main():
	cwd = os.getcwd()
	files = get_files(cwd)
	playlist_path = create_directory(cwd, '__playlist')
	html_body = fill_html_body(files)
	write_html(playlist_path, 'index.html', html_body)

	
	




if __name__ == '__main__':
	main()
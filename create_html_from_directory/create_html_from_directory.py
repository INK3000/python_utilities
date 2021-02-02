#!/usr/bin/python
import os


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
				videos_html += f'''<a class="px-5" target="_blank" href="{os.path.join(root, file)}">{file}</a>'''
		if videos_html:
			root_name = root.split('/')[-1]
			html_body += """<div class="container">"""
			html_body +="""<div class="row py-3">
					   <div class="col">"""
			html_body += f'''<p>{root_name}</p>'''
			html_body += videos_html
			html_body += '</div></div></div>'
	return html_body




def main():
	cwd = os.getcwd()
	files = get_files(cwd)
	playlist_path = create_directory(cwd, '__playlist')
	html_body = fill_html_body(files)
	write_html(playlist_path, 'index.html', html_body)

	
	




if __name__ == '__main__':
	main()
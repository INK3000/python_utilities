import cv2
import time
from pymediainfo import MediaInfo
from pprint import pprint

def stopwatch(func):
	
	def wrapper (*args, **kwargs):
		start = time.perf_counter()	
		result = func(*args, **kwargs)
		end = time.perf_counter()
		print(f'Время выполнения {end-start:.2f} сек. ({func.__name__})')
		return result
	return wrapper


@stopwatch
def with_opencv(filename):
    video = cv2.VideoCapture(filename)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    video.set(cv2.CAP_PROP_POS_FRAMES , frame_count)
    # video.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
    
    duration = video.get(cv2.CAP_PROP_POS_MSEC)
    return sec_to_hms(duration)

@stopwatch
def with_mediainfo(filename):
    result = None
    media_info = MediaInfo.parse(filename)
    for track in media_info.tracks:
        if track.track_type == "Video":
            result = sec_to_hms(track.duration*0.001)
    return result


def sec_to_hms(seconds):
    seconds = int(seconds)
    h = seconds//3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)


def main():
    filename = '1. ООП_ Объекты и классы.mp4'
    v = with_opencv(filename)
    print(v)
    v = with_mediainfo(filename)
    print(v)


if __name__ == '__main__':
	main()






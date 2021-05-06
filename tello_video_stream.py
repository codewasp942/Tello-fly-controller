import cv2 as cv
import treading

def show_video():
	# show video from drone
	print('start recv video stream')

	captures = []
	for i in ips:
		captures.append(cv.VideoCapture('udp://'+ips[0]+':11111'))

	while stream_on:
		for now_capture in captures:
			ret,now_frame = now_capture.read()
			try:
				cv.imshow('capture', now_frame)
			finally:
				pass
		if cv.waitKey(10)==ord('q'):
			break
	capture.release()
	cv.destroyAllWindows()

stream_on = False

def startup_video():
	global stream_on
	stream_on = False
	thread_video = threading.Thread(target=show_video)

def stop_video():
	global stream_on
	stream_on = False
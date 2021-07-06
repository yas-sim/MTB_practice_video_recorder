import copy
import time
import datetime
import numpy as np
import cv2

cam_width  = 800
cam_height = 600
cam_fps = 15

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, cam_fps)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,  cam_width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
fps = cam.get(cv2.CAP_PROP_FPS)
print(fps, 'fps')

stime = time.time()
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
record_length = 60 * 10   # buffer length [sec]
movie_length = 5          # movie rength [sec]

# Prepare ring buffer and fill with black frames
zero_img = np.zeros((cam_height, cam_width, 3), dtype=np.uint8)
_, zero_enc = cv2.imencode('.jpg', zero_img, encode_param)
ring_buf = [ zero_enc for dmy in range(int(cam_fps * record_length)) ]

ptr_w = 0
ptr_r = 0

ptr_inc = 1  # Read pointer increment value (0=pause, -1=reverse)

def add_ptr(ptrval:int, delta:int):
    global ring_buf
    ptrval += delta
    if ptrval < 0:
        ptrval += len(ring_buf)
    if ptrval >= len(ring_buf):
        ptrval -= len(ring_buf)
    return ptrval

while True:
    _, img = cam.read()
    _, encimg = cv2.imencode('.jpg', img, encode_param)
    ring_buf[ptr_w] = encimg
    ptr_w = add_ptr(ptr_w, 1)
    cv2.imshow('Real Time', img)

    playback_img = ring_buf[ptr_r]
    decimg = cv2.imdecode(playback_img, 3)
    ptr_r = add_ptr(ptr_r, ptr_inc)

    if ptr_w >= ptr_r:
        time_shift = ptr_w - ptr_r
    else:
        time_shift = (ptr_w + len(ring_buf) - ptr_r)
    msg = 'TIME SHIFT:{}sec'.format(int(time_shift/cam_fps))
    pos = (8, 24)
    cv2.putText(decimg, msg, pos, cv2.FONT_HERSHEY_PLAIN, 2, (  0,  0,  0), 2, cv2.LINE_AA)
    cv2.putText(decimg, msg, pos, cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA)
    if ptr_inc == -1:
        msg = 'Reverse'
        pos = (8, 48)
        cv2.putText(decimg, msg, pos, cv2.FONT_HERSHEY_PLAIN, 2, (  0,  0,  0), 2, cv2.LINE_AA)
        cv2.putText(decimg, msg, pos, cv2.FONT_HERSHEY_PLAIN, 2, (  0,255,255), 1, cv2.LINE_AA)
    cv2.imshow('Time Shift', decimg)

    key = cv2.waitKey(1)
    if key == ord('z'): ptr_r = add_ptr(ptr_r, -cam_fps)
    if key == ord('x'): ptr_r = add_ptr(ptr_r,  cam_fps)
    if key == ord('a'): ptr_r = add_ptr(ptr_r, -cam_fps*10)
    if key == ord('s'): ptr_r = add_ptr(ptr_r,  cam_fps*10)
    if key == ord('k'): ptr_r = add_ptr(ptr_r, -1)
    if key == ord('l'): ptr_r = add_ptr(ptr_r,  1)

    if key == ord('0'):
        ptr_r = ptr_w
    if key == ord(' ') or key == ord('p'):
        ptr_inc = 1 if ptr_inc != 1 else 0
    if key == ord('o'):
        ptr_inc = -1

    if key == ord('r'):
        dt = datetime.datetime.now()
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        filename = 'movie_{:04}{:02}{:02}-{:02}{:02}{:02}.mp4'.format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        writer = cv2.VideoWriter(filename, codec, 15.0, (cam_width, cam_height))
        for i in range(cam_fps * movie_length):
            tmp_img = cv2.imdecode(ring_buf[ptr_r + i], 3)
            writer.write(tmp_img)
        writer.release()

    if key == 27 or key == ord('q'):
        break

cv2.destroyAllWindows()

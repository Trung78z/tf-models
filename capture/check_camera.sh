v4l2-ctl --list-formats-ext -d /dev/video0


ffmpeg -f v4l2 -list_formats all -i /dev/video0
ffmpeg -f v4l2 -framerate 30 -video_size 640x480 -i /dev/video0 -f null -
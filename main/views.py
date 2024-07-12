import subprocess
from django.shortcuts import render
from django.http import HttpResponse

# Укажите ваш RTSP URL
source_url = "rtsp://admin:L2597A04@192.168.1.38/cam/realmonitor?channel=1&subtype=00&authbasic=YWRtaW46TDI1OTdBMDQ="
destination_url = "rtsp://84.54.12.206:8554/sadikonline/live"

ffmpeg_process = None

def start_stream(request):
    global ffmpeg_process
    if ffmpeg_process is None:
        command = [
            'ffmpeg',
            '-i', source_url,
            '-f', 'rtsp',
            '-rtsp_transport', 'tcp',
            destination_url
        ]
        ffmpeg_process = subprocess.Popen(command)
        return HttpResponse("Stream started")
    else:
        return HttpResponse("Stream already running")

def stop_stream(request):
    global ffmpeg_process
    if ffmpeg_process is not None:
        ffmpeg_process.terminate()
        ffmpeg_process = None
        return HttpResponse("Stream stopped")
    else:
        return HttpResponse("No stream running")
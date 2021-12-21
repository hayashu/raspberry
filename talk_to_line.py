import requests, os
from picamera import PiCamera
from time import sleep

cam = PiCamera()
cam.framerate = 15
cam.start_preview()
cam.resolution = (2592,1944)


def main():
    send_line_notify('\nてすとてすと\n彼女欲しい')

def send_line_notify(notification_message):
    """
    LINEに通知する
    """
    line_notify_token = 'Ai2BoygLdiZGghJdyUQaDJsucC3pkDsdDJIsxqZFwc6'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

def main_gazo():
    counter = 1
    for i in range(0,100,20):
        cam.annotate_text = "Brightness = %s" % i
        cam.brightness = i
        sleep(1)
        cam.capture('/home/pi/raspberry_pi/images/IMG%s.jpg' % counter)
        counter += 1
    cam.resolution = (1920,1080)
    cam.stop_preview()
    
    url = "https://notify-api.line.me/api/notify"
    token = "Ai2BoygLdiZGghJdyUQaDJsucC3pkDsdDJIsxqZFwc6"
    headers = {"Authorization" : "Bearer "+ token}


    message = 'Fortnite！'
    payload = {"message" :  message}
    #imagesフォルダの中のgazo.jpg
    files = {"imageFile":open('/home/pi/raspberry_pi/images/IMG3.jpg','rb')}
    #rbはバイナリファイルを読み込む
    post = requests.post(url ,headers = headers ,params=payload,files=files)
    
if __name__ == "__main__":
    main_gazo()
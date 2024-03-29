#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

import argparse
import os.path
import json
import sys


import google.auth.transport.requests
import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file



DEVICE_API_URL = 'https://embeddedassistant.googleapis.com/v1alpha2'


def process_device_actions(event, device_id):
    if 'inputs' in event.args:
        for i in event.args['inputs']:
            if i['intent'] == 'action.devices.EXECUTE':
                for c in i['payload']['commands']:
                    for device in c['devices']:
                        if device['id'] == device_id:
                            if 'execution' in c:
                                for e in c['execution']:
                                    if e['params']:
                                        yield e['command'], e['params']
                                    else:
                                        yield e['command'], None


def process_event(event, device_id, assistant):
    """Pretty prints events.

    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.

    Args:
        event(event.Event): The current event to process.
    """



    
    
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print()

    print(event)
    if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        s = event.args['text']
        print(s)
        if 'テレビ' in s and  ('つけて' in s or 'オン' in s):
            import subprocess
            try:
                DICT_PATH='/var/lib/mecab/dic/open-jtalk/naist-jdic/'
                VOICE_PATH='/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'
                with open('speech.txt', 'w') as f:
                    f.write("テレビつけるの無理")
                subprocess.run(['open_jtalk', '-x', DICT_PATH, '-m', VOICE_PATH, '-ow', 'speech.wav', 'speech.txt'])
                subprocess.run(['aplay', 'speech.wav'])
                print('tv on was failed')
            except OSError:
                print('error occured')
            assistant.stop_conversation()
            #################
        elif '温度' in s and ('教えて' in s):
            import time
            import board
            import adafruit_dht
            import sys
            import subprocess
            DICT_PATH='/var/lib/mecab/dic/open-jtalk/naist-jdic/'
            VOICE_PATH='/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'
            dhtDevice = adafruit_dht.DHT11(board.D16)
            assistant.stop_conversation()
            while True:
                try:
                    temp = dhtDevice.temperature
                    hum = dhtDevice.humidity
                    print('temperature:',temp,'C humidity:',hum)
                    with open('speech.txt', 'w') as f:
                        text = "只今の部屋の温度は",str(temp),'℃、湿度は',str(hum),'%です'
                        f.write(str(text))
                    subprocess.run(['open_jtalk', '-x', DICT_PATH, '-m', VOICE_PATH, '-ow', 'speech.wav', 'speech.txt'])
                    subprocess.run(['aplay', 'speech.wav'])
                except RuntimeError as error:
                    print(error.args[0])
                time.sleep(2.0)
        ##########################
        elif 'LED' in s and  ('つけて' in s or 'オン' in s):
            import RPi.GPIO as GPIO
            from time import sleep

            GPIO.setwarnings(False)

            pinLED = 26
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pinLED, GPIO.OUT)

            i = 0

            while i < 4:
                GPIO.output(pinLED, GPIO.HIGH)
                sleep(1)
                GPIO.output(pinLED,GPIO.LOW)
                sleep(1)
                i += 1
                print(i)
            sleep(1)
            GPIO.cleanup();
        elif 'カメラ' in s and  ('つけて' in s or 'オン' in s):
            from picamera import PiCamera
            from time import sleep

            cam = PiCamera()
            cam.framerate = 15
            cam.start_preview()
            cam.resolution = (2592,1944)

            counter = 1
            for i in range(0,100,20):
                cam.annotate_text = "Brightness = %s" % i
                cam.brightness = i
                sleep(1)
                cam.capture('/home/pi/Downloads/voice_recognition/IMG%s.jpg' % counter)
                counter += 1

            cam.resolution = (1920,1080)
            cam.start_recording('/home/pi/Downloads/video.h264')
            sleep(5)
            cam.stop_recording()
            cam.stop_preview()
        elif 'テレビ' in s and  ('消して' in s or 'オフ' in s):
            args = ['irsend', '-#', '1', 'SEND_ONCE', 'TV', 'power']
            try:
                subprocess.Popen(args)
            except OSError:
                print('command not found.')
            assistant.stop_conversation()
        elif 'NHK 教育' in s or 'Eテレ' in s:
            args = ['irsend', '-#', '1', 'SEND_ONCE', 'TV', 'ch2']
            try:
                subprocess.Popen(args)
            except OSError:
                print('command not found.')
            assistant.stop_conversation()
        elif 'NHK' in s:
            args = ['irsend', '-#', '1', 'SEND_ONCE', 'TV', 'ch1']
            try:
                subprocess.Popen(args)
            except OSError:
                print('command not found.')
            assistant.stop_conversation()
        elif 'TBS' in s:
            args = ['irsend', '-#', '1', 'SEND_ONCE', 'TV', 'ch6']
            try:
                subprocess.Popen(args)
            except OSError:
                print('command not found.')
            assistant.stop_conversation()
        elif 'フジテレビ' in s:
            args = ['irsend', '-#', '1', 'SEND_ONCE', 'TV', 'ch8']
            try:
                subprocess.Popen(args)
            except OSError:
                print('command not found.')
            assistant.stop_conversation()
        elif 'テレビ朝日' in s:
            args = ['irsend', '-#', '1', 'SEND_ONCE', 'TV', 'ch5']
            try:
                subprocess.Popen(args)
            except OSError:
                print('command not found.')
            assistant.stop_conversation()
        elif 'テレビ東京' in s:
            args = ['irsend', '-#', '1', 'SEND_ONCE', 'TV', 'ch7']
            try:
                subprocess.Popen(args)
            except OSError:
                print('command not found.')
            assistant.stop_conversation()
        elif 'MX' in s:
            args = ['irsend', '-#', '1', 'SEND_ONCE', 'TV', 'ch9']
            try:
                subprocess.Popen(args)
            except OSError:
                print('command not found.')
            assistant.stop_conversation()
        elif 'ボリューム' in s and ('上げて' in s or 'アップ' in s):
            args = ['irsend', '-#', '1', 'SEND_ONCE', 'TV', 'vup']
            try:
                subprocess.Popen(args)
            except OSError:
                print('command not found.')
            assistant.stop_conversation()
        elif 'ボリューム' in s and ('下げて' in s or 'ダウン' in s):
            args = ['irsend', '-#', '1', 'SEND_ONCE', 'TV', 'vdown']
            try:
                subprocess.Popen(args)
            except OSError:
                print('command not found.')
            assistant.stop_conversation()
        else:
            pass
 
    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        print()
    if event.type == EventType.ON_DEVICE_ACTION:
        for command, params in process_device_actions(event, device_id):
            print('Do command', command, 'with params', str(params))


def register_device(project_id, credentials, device_model_id, device_id):
    """Register the device if needed.

    Registers a new assistant device if an instance with the given id
    does not already exists for this model.

    Args:
       project_id(str): The project ID used to register device instance.
       credentials(google.oauth2.credentials.Credentials): The Google
                OAuth2 credentials of the user to associate the device
                instance with.
       device_model_id: The registered device model ID.
       device_id: The device ID of the new instance.
    """
    base_url = '/'.join([DEVICE_API_URL, 'projects', project_id, 'devices'])
    device_url = '/'.join([base_url, device_id])
    session = google.auth.transport.requests.AuthorizedSession(credentials)
    r = session.get(device_url)
    print(device_url, r.status_code)
    if r.status_code == 404:
        print('Registering....', end='', flush=True)
        r = session.post(base_url, data=json.dumps({
            'id': device_id,
            'model_id': device_model_id,
            'client_type': 'SDK_LIBRARY'
        }))
        if r.status_code != 200:
            raise Exception('failed to register device: ' + r.text)
        print('\rDevice registered.')


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
    parser.add_argument('--device_model_id', type=str,
                        metavar='DEVICE_MODEL_ID', required=True,
                        help='The device model ID registered with Google')
    parser.add_argument('--project_id', type=str,
                        metavar='PROJECT_ID', required=False,
                        help=('The project ID used to register'
                              'device instances'))

    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    with Assistant(credentials, args.device_model_id) as assistant:
        events = assistant.start()

        print('device_model_id:', args.device_model_id + '\n' +
              'device_id:', assistant.device_id + '\n')

        if args.project_id:
            register_device(args.project_id, credentials,
                            args.device_model_id, assistant.device_id)

        for event in events:
            process_event(event, assistant.device_id, assistant)


if __name__ == '__main__':
    main()

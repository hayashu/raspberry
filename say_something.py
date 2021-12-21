##open jtalk使用してみた

#!/usr/bin/env python3
import sys
import subprocess

DICT_PATH='/var/lib/mecab/dic/open-jtalk/naist-jdic/'
VOICE_PATH='/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'

while True:
    print('何か入力してエンターキーを押してね（CTRL+Cで終了）')
    text = input()
    with open('speech.txt', 'w') as f:
        f.write(text)
    subprocess.run(['open_jtalk', '-x', DICT_PATH, '-m', VOICE_PATH, '-ow', 'speech.wav', 'speech.txt'])
    subprocess.run(['aplay', 'speech.wav'])
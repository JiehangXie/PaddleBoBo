# -*- coding: utf-8 -*-  
from PaddleTools.TTS import TTSExecutor
from PaddleTools.GAN import wav2lip
import time
import os
import requests
import json
from config import Config
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, default='default.yaml', help='config file')

def get_news(timestamp):
    timestamp = timestamp - 600
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                "Cookie": "uid=wKhSYmG7/mV4wH0eAzi6Ag==; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1639710329; v=A5yfBb9vERPwqeXPo0txCKEbbbFLFUBwwrlUIHadqAdqwTLvniUQzxLJJJ7F"}
        news_url = "https://news.10jqka.com.cn/tapp/news/push/stock/?page=1&tag=&track=website&ctime={}".format(timestamp)
        news_requests = requests.get(news_url,headers=headers)
        news_content = news_requests.text
        news_json = json.loads(news_content)
        newest_news = news_json['data']['list'][0]
        newest_id = newest_news['id']
        newest_content = newest_news['digest']
        newest_content = newest_content.replace('/','一') #替换掉新闻中的/量词，如/桶，/盎司等
        return newest_id, newest_content
    except:
        return None, None

if __name__ == '__main__':
    args = parser.parse_args()
    _Config = Config(args.config)

    TTS = TTSExecutor()
    SAVEPATH = _Config.SavePath()
    before_news_id = None

    while True:
        timestamp = int(time.time())
        VIDEO_SAVE_PATH = os.path.join(SAVEPATH['VIDEO_SAVE_PATH'],f'{timestamp}.mp4')
        AUDIO_SAVE_PATH = os.path.join(SAVEPATH['AUDIO_SAVE_PATH'],f'{timestamp}.wav')

        news_id,news_content = get_news(timestamp)

        if news_id == None or news_id==before_news_id:
            #如果返回None或者与上一条相同
            pass
        else:
            wavfile = TTS.run(text=news_content,output=AUDIO_SAVE_PATH)
            video = wav2lip(_Config.GAN()['FOM_OUTPUT_VIDEO'],wavfile,VIDEO_SAVE_PATH)
            before_news_id = news_id

        time.sleep(15) #每15秒检查一次更新
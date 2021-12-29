# -*- coding: utf-8 -*-  
import os
import argparse

#引入飞桨生态的语音和GAN依赖
from PaddleTools.TTS import TTSExecutor
from PaddleTools.GAN import wav2lip

parser = argparse.ArgumentParser()
parser.add_argument('--human', type=str,default='', help='human video', required=True)
parser.add_argument('--output', type=str, default='output.mp4', help='output video')
parser.add_argument('--text', type=str,default='', help='human video', required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    TTS = TTSExecutor('default.yaml') #PaddleSpeech语音合成模块
    wavfile = TTS.run(text=args.text,output='output.wav') #合成音频
    video = wav2lip(args.human,wavfile,args.output) #将音频合成到唇形视频
    os.remove(wavfile) #删除临时的音频文件
    print('视频生成完毕，输出路径为：{}'.format(args.output))
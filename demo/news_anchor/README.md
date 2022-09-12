## 快速开始
### 1.安装依赖包
```
pip install ppgan paddlespeech
```
### 2.配置文件(default.yaml)
```
GANDRIVING:
  FOM_INPUT_IMAGE: './file/input/test.png' #带人脸的静态图
  FOM_DRIVING_VIDEO: './file/input/zimeng.mp4' #用作表情迁移的参考视频
  FOM_OUTPUT_VIDEO: './file/input/test.mp4' #表情迁移后的视频输出路径

TTS:
  SPEED: 1.0 #语速
  PITCH: 1.0 #音高
  ENERGY: 1.0 #发音能级

SAVEPATH:
  VIDEO_SAVE_PATH: './file/output/video/' #保存音频的路径
  AUDIO_SAVE_PATH: './file/output/audio/' #保存生成虚拟主播视频的路径
```
### 3.让静态人脸动起来
```
python create_virtual_human.py --config default.yaml
```
### 4.通用版本生成

```
python general_demo.py \
    --human ./file/input/test.mp4 \
    --output output.mp4 \
    --text 各位开发者大家好，欢迎使用飞桨。
```

| 参数 | 参数说明 |
| :---: | :---: |
| human | 第3步生成的人脸视频路径 |
| output | 生成虚拟主播视频的输出路径 |
| text | 虚拟主播语音文本 |
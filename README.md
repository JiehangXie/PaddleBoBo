# PaddleBoBo - 元宇宙时代，你也可以动手做一个虚拟主播。
![python version](https://img.shields.io/badge/python-3.7+-orange.svg)
![GitHub Repo stars](https://img.shields.io/github/stars/JiehangXie/PaddleBoBo)
![支持系统](https://img.shields.io/badge/支持系统-Win/Linux/MAC-9cf)  

PaddleBoBo是基于飞桨PaddlePaddle深度学习框架和PaddleSpeech、PaddleGAN等开发套件的虚拟主播快速生成项目。PaddleBoBo致力于简单高效、可复用性强，只需要一张带人像的图片和一段文字，就能快速生成一个虚拟主播的视频；并能通过简单的二次开发更改文字输入，实现视频实时生成和实时直播功能。

## 应用案例

![](https://ai-studio-static-online.cdn.bcebos.com/2562494f3e754bcf9e21ce0bc9cf7c6d997f34faf3604d0c84866ccdac36b3e0)

 - [PaddleBoBo虚拟主播实时直播演示 - Bilibili](https://www.bilibili.com/video/BV1xL4y1n7rH?share_source=copy_web)

 - [PaddleBoBo虚拟主播竖版生成演示 - Bilibili](https://www.bilibili.com/video/BV1aP4y1H7qi?share_source=copy_web)

 - [PaddleBoBo虚拟主播横版生成演示 - Bilibili](https://www.bilibili.com/video/BV1uu411S79J?share_source=copy_web)

## 运行环境
* [飞桨AIStudio在线运行](https://aistudio.baidu.com/aistudio/projectdetail/3280614?contributionType=1&shared=1) (强烈推荐，Tesla V100冲！！！)
* 自建本地环境
  * Windows 10
  * Python 3.7+
  * PaddlePaddle >= 2.2.1
  * Nvidia显卡 显存16G+（没测试过，希望有显卡的土豪大佬们反馈下）

## 更新日志
- 2021.12.29 加入PaddleSpeech TTS的特性，支持修改语速、音高和发音能级。

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
### 3.视频修剪 (用作driving video)
```
python video_crop.py --input ./file/input/need_crop.mp4 --output ./file/input/crop_driving.mp4
```
### 4.让静态人脸动起来
```
python create_virtual_human.py --config default.yaml
```
### 5.通用版本生成

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

## 案例库
### AI财经新闻主播
    * 运行news_app.py 持续采集同花顺新闻数据并生成视频
    * 运行play.py 实时和循环播放生成的视频
### 更多应用案例正在开发中，欢迎开发者投稿

## TODO LIST
 - ~~加入语速、音调控制~~
 - 修复黑框BUG  
如果大佬们有什么想法的话可以提Issue，同时也欢迎PR。
 - https://github.com/JiehangXie/PaddleBoBo/issues

## 参考资料
 - https://github.com/PaddlePaddle/PaddleSpeech
 - https://github.com/PaddlePaddle/PaddleGAN

import moviepy.editor as mpy
import ppgan.faceutils.face_detection.detection.sfd as sfd
import numpy
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str,default='./file/input/need_crop.mp4', help='need crop origin video')
parser.add_argument('--output', type=str, default='./file/input/crop_driving.mp4', help='output crop driving video')

if __name__ == '__main__':
    args = parser.parse_args()

    # 剪辑一分钟视频
    video = mpy.VideoFileClip(args.input).subclip("00:00:01","00:00:60")

    # 获取第一帧图像，必须包含人脸
    frame = video.get_frame(1)

    # s3fd 面部检测
    detector = sfd.FaceDetector()

    # 获取面部矩形框
    face_rect = detector.detect_from_batch([frame])[0][0]

    # 人脸修剪
    clip = video.crop(x1 = face_rect[0] - 50,y1 = face_rect[1] - 100,x2 = face_rect[2] + 100, y2 = face_rect[3] + 50)

    # 输出driving video
    clip.write_videofile(args.output)

    print('视频生成完毕，输出路径为：{}'.format(args.output))

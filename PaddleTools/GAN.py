import os
from ppgan.apps.wav2lip_predictor import Wav2LipPredictor
from ppgan.apps.first_order_predictor import FirstOrderPredictor

#热加载
wav2lip_predictor = Wav2LipPredictor(static = False,fps=30,pads = [0, 10, 0, 0],
                 face_det_batch_size = 4,
                 wav2lip_batch_size = 32,
                 resize_factor = 1,
                 crop = [0, -1, 0, -1],
                 box = [-1, -1, -1, -1],
                 rotate = False,
                 nosmooth = False,
                 face_detector = 'sfd',
                 face_enhancement = True)


def wav2lip(input_video,input_audio,output):
    wav2lip_predictor.run(input_video, input_audio, output)
    return output

def FOM(source_image,driving_video,output_path):
    output,filename = os.path.split(output_path)
    first_order_predictor = FirstOrderPredictor(output = output, 
                                                filename = filename, 
                                                face_enhancement = True, 
                                                ratio = 0.4,
                                                relative = True,
                                                image_size=512,
                                                adapt_scale = True)
    first_order_predictor.run(source_image, driving_video)
    return os.path.join(output,filename)

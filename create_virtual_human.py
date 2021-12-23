from PaddleTools.GAN import FOM
import argparse
from config import Config

parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, default='default.yaml', help='config file')

if __name__ == '__main__':
    args = parser.parse_args()
    _Config = Config(args.config)
    GAN_Config = _Config.GAN()

    cvh = FOM(GAN_Config['FOM_INPUT_IMAGE'],GAN_Config['FOM_DRIVING_VIDEO'],GAN_Config['FOM_OUTPUT_VIDEO'])

    print('已成功创建虚拟人，文件保存在{}'.format(cvh))

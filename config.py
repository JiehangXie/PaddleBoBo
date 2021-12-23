# -*- coding: utf-8 -*-  
import yaml

class Config(object):
    def __init__(self,filename):
        self.filename = filename
        self.config = self.load_config()

    def load_config(self):
        with open(self.filename,'r',encoding='utf-8') as f:
            config = yaml.load(f,Loader=yaml.FullLoader)
        return config

    def GAN(self):
        return self.config['GANDRIVING']
    
    def SavePath(self):
        return self.config['SAVEPATH']
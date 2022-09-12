# -*- coding: utf-8 -*-
# This module is based on PaddleSpeech, more infomation can be found in https://github.com/PaddlePaddle/PaddleSpeech.

from paddlespeech.cli.tts import TTSExecutor as PPTTS

CONFIG_OPTION = {
    "male_default": {
        "am": "fastspeech2_aishell3", 
        "voc": "pwgan_aishell3", 
        "spk_id": 167, 
        "lang": "zh"
    },
    
    "male_mix": {
        "am": "fastspeech2_mix", 
        "voc": "hifigan_csmsc", 
        "spk_id": 167, 
        "lang": "mix"
    },

    "female_default": {
        "am": "fastspeech2_csmsc", 
        "voc": "hifigan_csmsc", 
        "spk_id":0, 
        "lang":"zh"
    },

    "female_mix": {
        "am": "fastspeech2_mix", 
        "voc": "hifigan_csmsc", 
        "spk_id": 0, 
        "lang": "mix"
    }
}


class TTSExecutor(PPTTS):
    def __init__(self, config) -> None:
        super().__init__()
        self.config = CONFIG_OPTION[config]
        self.am = self.config["am"]
        self.voc = self.config["voc"]
        self.spk_id = self.config["spk_id"]
        self.lang = self.config["lang"]

    def __call__(self, text, output="output.wav"):
        self._init_from_path(
                am=self.am,
                voc=self.voc,
                lang=self.lang)
        self.infer(text=text, lang=self.lang, am=self.am, spk_id=self.spk_id)
        res = self.postprocess(output=output)
        print(res)
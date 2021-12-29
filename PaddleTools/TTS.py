# -*- coding: utf-8 -*-
import os

import numpy as np
import paddle
import soundfile as sf
import yaml
from yacs.config import CfgNode

from paddlespeech.cli.utils import download_and_decompress
from paddlespeech.cli.utils import MODEL_HOME

from paddlespeech.s2t.utils.dynamic_import import dynamic_import
from paddlespeech.t2s.frontend.zh_frontend import Frontend
from paddlespeech.t2s.modules.normalizer import ZScore

model_alias = {
    # acoustic model
    "fastspeech2": "paddlespeech.t2s.models.fastspeech2:FastSpeech2",
    "fastspeech2_inference": "paddlespeech.t2s.models.fastspeech2:StyleFastSpeech2Inference",
    # voc
    "pwgan":
    "paddlespeech.t2s.models.parallel_wavegan:PWGGenerator",
    "pwgan_inference":
    "paddlespeech.t2s.models.parallel_wavegan:PWGInference",
}

pretrained_models = {
    # fastspeech2
    "fastspeech2_csmsc-zh": {
        'url':
        'https://paddlespeech.bj.bcebos.com/Parakeet/released_models/fastspeech2/fastspeech2_nosil_baker_ckpt_0.4.zip',
        'md5':
        '637d28a5e53aa60275612ba4393d5f22',
        'config':
        'default.yaml',
        'ckpt':
        'snapshot_iter_76000.pdz',
        'speech_stats':
        'speech_stats.npy',
        'phones_dict':
        'phone_id_map.txt',
        'pitch_stats':
        'pitch_stats.npy',
        'energy_stats':
        'energy_stats.npy',
    },
    # pwgan
    "pwgan_csmsc-zh": {
        'url':
        'https://paddlespeech.bj.bcebos.com/Parakeet/released_models/pwgan/pwg_baker_ckpt_0.4.zip',
        'md5':
        '2e481633325b5bdf0a3823c714d2c117',
        'config':
        'pwg_default.yaml',
        'ckpt':
        'pwg_snapshot_iter_400000.pdz',
        'speech_stats':
        'pwg_stats.npy',
    },
}

class TTSExecutor():
    def __init__(self, config):
        
        #FastSpeech2
        model_tag = 'fastspeech2_csmsc-zh'
        am_res_path = self._get_pretrained_path(model_tag)
        am_config = os.path.join(am_res_path,pretrained_models[model_tag]['config'])
        am_ckpt = os.path.join(am_res_path,pretrained_models[model_tag]['ckpt'])
        am_stat = os.path.join(am_res_path, pretrained_models[model_tag]['speech_stats'])
        # must have phones_dict in acoustic
        phones_dict = os.path.join(am_res_path, pretrained_models[model_tag]['phones_dict'])
        # StyleFastSpeech
        pitch_stats = os.path.join(am_res_path, pretrained_models[model_tag]['pitch_stats'])
        energy_stats = os.path.join(am_res_path, pretrained_models[model_tag]['energy_stats'])

        #VOC
        voc_tag = "pwgan_csmsc-zh"
        voc_res_path = self._get_pretrained_path(voc_tag)
        voc_config = os.path.join(voc_res_path,pretrained_models[voc_tag]['config'])
        voc_ckpt = os.path.join(voc_res_path,pretrained_models[voc_tag]['ckpt'])
        voc_stat = os.path.join(voc_res_path, pretrained_models[voc_tag]['speech_stats'])

        # Init body.
        with open(am_config) as f:
            self.am_config = CfgNode(yaml.safe_load(f))
        with open(voc_config) as f:
            voc_config = CfgNode(yaml.safe_load(f))
        with open(config) as f:
            self.style_config = CfgNode(yaml.safe_load(f))

        with open(phones_dict, "r") as f:
            phn_id = [line.strip().split() for line in f.readlines()]
        vocab_size = len(phn_id)
        #print("vocab_size:", vocab_size)

        # acoustic model
        odim = self.am_config.n_mels

        am_class = dynamic_import('fastspeech2', model_alias)
        am_inference_class = dynamic_import('fastspeech2_inference', model_alias)

        am = am_class(idim=vocab_size, odim=odim, spk_num=1, **self.am_config["model"])

        am.set_state_dict(paddle.load(am_ckpt)["main_params"])
        am.eval()
        am_mu, am_std = np.load(am_stat)
        am_mu = paddle.to_tensor(am_mu)
        am_std = paddle.to_tensor(am_std)
        am_normalizer = ZScore(am_mu, am_std)
        self.am_inference = am_inference_class(am_normalizer, am, pitch_stats, energy_stats)
        self.am_inference.eval()

        # vocoder
        voc_class = dynamic_import('pwgan', model_alias)
        voc_inference_class = dynamic_import('pwgan_inference', model_alias)
        voc = voc_class(**voc_config["generator_params"])
        voc.set_state_dict(paddle.load(voc_ckpt)["generator_params"])
        voc.remove_weight_norm()
        voc.eval()
        voc_mu, voc_std = np.load(voc_stat)
        voc_mu = paddle.to_tensor(voc_mu)
        voc_std = paddle.to_tensor(voc_std)
        voc_normalizer = ZScore(voc_mu, voc_std)
        self.voc_inference = voc_inference_class(voc_normalizer, voc)
        self.voc_inference.eval()

        self.frontend = Frontend(phone_vocab_path=phones_dict, tone_vocab_path=None)

    def _get_pretrained_path(self, tag):
        """
        Download and returns pretrained resources path of current task.
        """
        assert tag in pretrained_models, 'Can not find pretrained resources of {}.'.format(tag)
        res_path = os.path.join(MODEL_HOME, tag)
        decompressed_path = download_and_decompress(pretrained_models[tag],
                                                    res_path)
        decompressed_path = os.path.abspath(decompressed_path)
        return decompressed_path

    def run(self, text, output):
        #文本输入
        sentences = [str(text)]

        # 长句处理
        for sentence in sentences:
            input_ids = self.frontend.get_input_ids(sentence, merge_sentences=False, get_tone_ids=False)
            phone_ids = input_ids["phone_ids"]
            flags = 0
            for part_phone_ids in phone_ids:
                with paddle.no_grad():
                    mel = self.am_inference(
                                        part_phone_ids,
                                        durations=None,
                                        durations_scale = 1 / float(self.style_config['TTS']['SPEED']),
                                        durations_bias = None,
                                        pitch = None,
                                        pitch_scale = float(self.style_config['TTS']['PITCH']),
                                        pitch_bias = None,
                                        energy = float(self.style_config['TTS']['ENERGY']),
                                        energy_scale = None,
                                        energy_bias = None,
                                        )
                    wav = self.voc_inference(mel)
                if flags == 0:
                    wav_all = wav
                    flags = 1
                else:
                    wav_all = paddle.concat([wav_all, wav])
            sf.write(
                output,
                wav_all.numpy(),
                samplerate=self.am_config.fs)
        return output
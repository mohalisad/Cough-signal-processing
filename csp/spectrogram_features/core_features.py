#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import librosa
import matplotlib.pyplot as plt


# get the spectrogram features
class SpectrogramFeatures(object):
    
    def __init__(self, audio_path):
    
        self.audio_path = audio_path
        self.EPS = 1e-8
        self.start = int(np.random.uniform(-4800, 4800))

    @staticmethod
    def wav_to_signal(audio_path):
        
        signal, source = librosa.load(audio_path, sr=None)
        return {'signal': signal, 'source': source}

    @staticmethod
    def get_spectrogram(signal, window='hamming'):
        
        fourier_transform = librosa.stft(
            signal,
            n_fft=480,
            hop_length=160,
            win_length=480,
            window=window)
        
        magnitude, phase = librosa.magphase(fourier_transform)
        
        return {'magnitude': magnitude, 'phase': phase}
    
    @staticmethod
    def get_mel_spectrogram(signal, sr):
        mel_mag = librosa.feature.melspectrogram(y=signal, sr=sr, n_fft=1024, hop_length=512, n_mels=128)
        mel_mag_db = librosa.power_to_db(mel_mag)
        return mel_mag, mel_mag_db

    def spectrogram_data(self, show_plot=False):
        """Separate a complex-valued spectrogram 
            D into its magnitude (S) 
            and phase (P) components, 
            so that D = S * P."""
        
        self.data = SpectrogramFeatures.wav_to_signal(self.audio_path)
        self.signal = self.data['signal']
        self.sr = self.data['source']
        
        mel_mag, mel_mag_db = SpectrogramFeatures.get_mel_spectrogram(self.signal, self.sr)
        
        self.spec = SpectrogramFeatures.get_spectrogram(self.signal, window='hamming')
        magnitude = self.spec['magnitude']
        
        log_spectrogram = np.log(magnitude)
        
        if show_plot:
            plt.imshow(log_spectrogram, aspect='auto', origin='lower',)
            plt.title('Raw audio spectrogram')

        return {'magnitude': magnitude,
                'signal': self.signal,
                'shape': self.signal.shape,
                'max': self.signal.max(),
                'min': self.signal.min(),
                'log_spectrogram': log_spectrogram,
                'sr': self.sr,
                'mel_spectrogram': mel_mag,
                'mel_spectrogram_db': mel_mag_db
                }

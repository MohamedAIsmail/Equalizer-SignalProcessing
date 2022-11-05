import plotly.graph_objects as go
import streamlit as st 
import numpy as np
import plotly as pt
import wave
from scipy.io.wavfile import read, write
from scipy.io import wavfile


def readAudioFile(fileName):
    audio_file = wave.open(fileName, 'rb')
    audio_player = open(fileName, 'rb')
    return audio_file, audio_player


def plotTimeDomain(time, data ):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=data,
                            mode='lines', name='Signal Plot'))
    fig.update_layout(title='Time Domain')
    fig.update_xaxes(title='Time')
    fig.update_yaxes(title='Signal Value')
    st.plotly_chart(fig)


def plotFrequencyDomain(frequency,frequency_magnitude):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=frequency, y=frequency_magnitude,
                            mode='lines', name='Signal Plot'))
    fig.update_layout(title='Frequency Domain')
    fig.update_xaxes(title='Frequency (Hz)')
    fig.update_yaxes(title='Magnitude')
    st.plotly_chart(fig)


def frequencyDomain(signal, sample_rate):
    freq = np.fft.rfft(signal)
    freq_magnitude= np.abs(freq)
    freq_phase=np.angle(freq,deg=False)
    fft_spectrum = np.fft.rfftfreq(signal.size, 1/sample_rate)
    return  freq_magnitude,freq_phase,fft_spectrum


## list = [{frequency_1: 5, frequency_2: 10, gain_db:2}]
def edit_frequency(freq_spectrum,freq_magnitude,sample_rate, edit_list):
    frequency_points= len(freq_spectrum)/(sample_rate/2)
    for edit in edit_list:
        freq_magnitude[int(frequency_points*edit["frequency_1"]):int((frequency_points*edit["frequency_2"]))]= np.sqrt((10**(edit['gain_db']/10)*(freq_magnitude[int(frequency_points*edit["frequency_1"]):int((frequency_points*edit["frequency_2"]))]**2)))
    return freq_magnitude


def inverse_fourier(mag, phase):
    complex_rect = mag * np.cos((phase))+ 1j*mag * np.sin((phase))
    inverse_forurier= np.fft.irfft(complex_rect)
    return inverse_forurier



def signal_to_wav(signal,sample_rate):
    signal=np.int16(signal)
    wavfile.write("file.wav",2*sample_rate,signal)
    return 
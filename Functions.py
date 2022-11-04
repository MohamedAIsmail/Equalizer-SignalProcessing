import plotly.graph_objects as go
import streamlit as st 
import numpy as np
import plotly as pt
import wave
from scipy.io.wavfile import read, write


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
    freq_magnitude = np.fft.rfft(signal)
    freq_magnitude_abs = np.abs(freq_magnitude)
    fft_spectrum = np.fft.rfftfreq(signal.size, 1/sample_rate)
    return  freq_magnitude_abs,fft_spectrum



## list = [{frequency_1: 5, frequency_2: 10 new_amplitude}]

def edit_frequency(freq_spectrum,frequency_magnitude, frequency_1, frequency_2,new_amplitude):
    for i,f in enumerate(frequency_magnitude):
        if f > frequency_1 and f < frequency_2 :
            freq_spectrum[i]= new_amplitude
    return freq_spectrum

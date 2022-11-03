import plotly.graph_objects as go
import streamlit as st  # 🎈 data web app development
import pandas as pd  # read csv, df manipulation
import numpy as np
import plotly as pt
import wave
from scipy.io.wavfile import read, write


def readAudioFile(fileName):
    audio_file = wave.open(fileName, 'rb')
    audio_player = open(fileName, 'rb')
    return audio_file, audio_player


def plotTimeDomain(data, time):

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=data,
                             mode='lines', name='Signal Plot'))

    fig.update_layout(title='Time Domain')
    fig.update_xaxes(title='Time')
    fig.update_yaxes(title='Signal Value')
    st.plotly_chart(fig)


def plotFrequencyDomain(data, time):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=data,
                             mode='lines', name='Signal Plot'))

    fig.update_layout(title='Frequency Domain')
    fig.update_xaxes(title='Frequency (Hz)')
    fig.update_yaxes(title='Magnitude')
    st.plotly_chart(fig)


def frequencyDomain(signal, sample_rate):
    fft_specturm = np.abs(np.fft.rfft(signal))
    freq = np.fft.rfftfreq(signal.size, 1/sample_rate)

    return fft_specturm, freq

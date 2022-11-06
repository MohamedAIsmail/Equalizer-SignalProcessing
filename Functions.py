import plotly.graph_objects as go
import streamlit as st  # 🎈 data web app development
import pandas as pd  # read csv, df manipulation
import numpy as np
import plotly as pt

import streamlit_vertical_slider as svs

from scipy.io.wavfile import read, write
from scipy.io import wavfile
from scipy import signal


def readAudioFile(fileName):
    sample_freq, audioData = read("Audios\\" + fileName)

    if 'audio_player' not in st.session_state:
        st.session_state['audio_player'] = open("Audios\\" + fileName, 'rb')

    return audioData, sample_freq, st.session_state.audio_player


def Sliders(sliderColumns):
    adjusted_data = []
    sliders = {}
    for idx in range(0, 11):
        with sliderColumns[idx]:
            if (idx == 0):
                st.header('')  # GUI USAGE
                st.header('')
                st.header('Power (dB)')
            else:
                key = f'member{str(idx)}'
                sliders[f'slider_group_{key}'] = svs.vertical_slider(
                    key=key, default_value=0, step=1, min_value=-12, max_value=12)
                if sliders[f'slider_group_{key}'] == None:
                    sliders[f'slider_group_{key}'] = 0
                adjusted_data.append((idx, sliders[f'slider_group_{key}']))

    return adjusted_data


def plot(x_points, y_points, graph_title, x_title, y_title, range):
    layout = go.Layout(margin=go.layout.Margin(l=0, r=0, b=0, t=30,))
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Scatter(x=x_points, y=y_points,
                             mode='lines'))
    fig.update_layout(height=300, title={
        'text': graph_title,
        'y': 1,
        'x': 0.49,
        'xanchor': 'center',
        'yanchor': 'top'},
        title_font=dict(
        family="Arial",
        size=17))
    fig.update_xaxes(title=x_title, range=[0, range])
    fig.update_yaxes(title=y_title)
    st.plotly_chart(fig, use_container_width=True)


def plotSpectrogram(audioData, fs, Title):
    N = 512
    w = signal.blackman(N)
    freqs, time, Pxx = signal.spectrogram(audioData, fs, window=w, nfft=N)

    layout = go.Layout(margin=go.layout.Margin(l=0, r=0, b=0, t=30,))
    fig = go.Figure(layout=layout)

    fig.add_trace(go.Heatmap(x=time, y=freqs, z=10*np.log10(Pxx),
                  colorscale='Jet', name='Spectrogram'))

    fig.update_layout(height=300, title={
        'text': Title,
        'y': 1,
        'x': 0.49,
        'xanchor': 'center',
        'yanchor': 'top'},
        title_font=dict(
        family="Arial",
        size=17))
    fig.update_xaxes(title='Time')
    fig.update_yaxes(title='Frequency')
    st.plotly_chart(fig, use_container_width=True)


def frequencyDomain(signalData, sampleFrequency):
    """
    fourier transform to frequency domain
    :param 
        signalData: list of time domain signal points 
        sampleFrequency: int of sample rate for signal (Hz)
    :return: average temperature
    """
    freq = np.fft.rfft(signalData)
    st.session_state['freq_magnitude'] = np.abs(freq)
    freq_phase = np.angle(freq, deg=False)
    fft_spectrum = np.fft.rfftfreq(signalData.size, 1/sampleFrequency)
    return st.session_state.freq_magnitude, freq_phase, fft_spectrum


def edit_frequency(freq_spectrum, freq_magnitude, sample_freq, edit_list):
    """
    edit frequecny range with ceratin gain
    :equation used
        Gain(dB)= 10log(new_frequency_power/new_frequency_power)
    :param 
        freq_spectrum : list of frequencies values in a certain signal
        freq_magnitude :  list of frequencies magnitudes in a certain signal
        sample_freq: int of sample rate for signal (Hz)
        edit_list: list of objects with a structrue:
                    [......{frequency_1: 5, frequency_2: 10, gain_db:2}]
                        frequency_1: start range of frequencies to be changed
                        frequency_2: end range of frequencies to be changed
                        gain_db: gain value ti change in decieble scale
    :return: list of edited frequency magnitudes 
    """
    frequency_points = len(freq_spectrum)/(sample_freq/2)
    for edit in edit_list:
        freq_magnitude[int(frequency_points*edit["frequency_1"]):int((frequency_points*edit["frequency_2"]))] = np.sqrt(
            (10**(edit['gain_db']/10)*(freq_magnitude[int(frequency_points*edit["frequency_1"]):int((frequency_points*edit["frequency_2"]))]**2)))
    return freq_magnitude


def inverse_fourier(mag, phase):
    """
    return frequency in polar form to rect form then take inverse fourier for it
    ** inverse with no data loss **
    :param 
        mag : list of frequencies magnitudes 
        phase :  list of frequencies phases
    :return: list of time domain signal after transformation 
    """
    complex_rect = mag * np.cos(phase) + 1j*mag * np.sin(phase)

    inverse_forurier = np.fft.irfft(complex_rect)

    return inverse_forurier


def signal_to_wav(signal, sample_rate):
    """
    convert signal array to a wav form saved in file.wav
    :param 
        signal : list of signal points in time domain
        sample_rate :  signal sample rate 
    : no return:
    """

    signal = np.int16(signal)
    wavfile.write("edited.wav", sample_rate, signal)

    st.session_state.audio_player = open("edited.wav", 'rb')

    return st.session_state.audio_player

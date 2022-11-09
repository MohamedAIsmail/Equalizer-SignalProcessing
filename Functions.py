import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st  # 🎈 data web app development
import pandas as pd  # read csv, df manipulation
import numpy as np
import plotly as pt
import streamlit_vertical_slider as svs
from scipy.io.wavfile import read, write
from scipy.io import wavfile
from scipy import signal
import scipy.io
import altair as alt



def readAudioFile(file_name):
    sample_freq, audio_data = read("Audios\\" + file_name)
    t_audio = len(audio_data) / sample_freq
    audio_palyer=open("Audios\\" + file_name, 'rb')
    time = np.linspace(0, t_audio, len(audio_data))
    return audio_data, time, t_audio, sample_freq, audio_palyer


def Sliders(sliderColumns, sliders_num):
    adjusted_data = []
    sliders = {}
    for idx in range(0, sliders_num):
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


def plot(time, amplitude, invAmplitude, x_title, y_title, range):

    fig = make_subplots(rows=1, cols=2, shared_yaxes=True,
                        horizontal_spacing=0.01)

    fig.add_trace(go.Scatter(x=time, y=amplitude,
                             mode='lines'), row=1, col=1)
    fig.add_trace(go.Scatter(x=time, y=invAmplitude,
                             mode='lines'), row=1, col=2)

    fig.update_xaxes(range=[0, range], title=x_title)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=200,
                      title_font=dict(
                          family="Arial",
                          size=17),
                      showlegend=False,
                      yaxis_title='Amplitude (mV)')
    st.plotly_chart(fig, use_container_width=True)


def plotSpectrogram(amplitude, invAmplitude, fs, range):
    N = 512
    w = signal.blackman(N)
    nFreqs, nTime, nPxx = signal.spectrogram(amplitude, fs, window=w, nfft=N)

    if (invAmplitude == []):
        invFreqs, invTime, invPXX = [], [], []
    else:
        invFreqs, invTime, invPXX = signal.spectrogram(
            invAmplitude, fs, window=w, nfft=N)

    layout = go.Layout(margin=go.layout.Margin(l=0, r=0, b=0, t=30,))
    fig = go.Figure(layout=layout).set_subplots(rows=1, cols=2, shared_yaxes=True,
                                                horizontal_spacing=0.01)

    fig.add_trace(go.Heatmap(x=nTime, y=nFreqs, z=10*np.log10(nPxx),
                  colorscale='Jet', name='Spectrogram'), row=1, col=1)
    fig.add_trace(go.Heatmap(x=invTime, y=invFreqs, z=10*np.log10(invPXX),
                  colorscale='Jet', name='Spectrogram'), row=1, col=2)

    fig.update_layout(height=300,
                      title_font=dict(
                          family="Arial",
                          size=17), yaxis_title='Frequency (Hz)')
    fig.update_xaxes(range=[0, range], title='Time (s)')
    st.plotly_chart(fig, use_container_width=True)


def frequencyDomain(signal_data, sampleFrequency):
    """
    fourier transform to frequency domain
    :param 
        signal_data: list of time domain signal points 
        sampleFrequency: int of sample rate for signal (Hz)
    :return: 3 lists (1- freq magnitude, 2-freq phase, frequency spectrum(x-axis))
    """
    freq = np.fft.rfft(signal_data)
    freq_magnitude = np.abs(freq)
    freq_phase = np.angle(freq, deg=False)
    fft_spectrum = np.fft.rfftfreq(signal_data.size, 1/sampleFrequency)
    return freq_magnitude, freq_phase, fft_spectrum


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
    time_domain_signal = np.fft.irfft(complex_rect)
    return time_domain_signal


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
    audio_player = open("edited.wav", 'rb')
    return audio_player


def open_mat(mat_file):
    """
        Open .Mat file for medical signal files
        :param 
        wav_file : uploaded mat file 
        :return:
            time-> list for x-axis(time) points 
            signal_array-> list for y-axis(amplitude)(V) points 
            sample_rate-> sample rate for the signal
    """
    file_data = scipy.io.loadmat(mat_file)
    signal_array = file_data["val"][0]/(200)
    signal_array = signal_array*10**-3  # in V

    # VIP: convert to volts to fourir inverse correctly
    time = np.linspace(0.0, 10, len(signal_array))
    sample_rate = 360
    return time, signal_array, sample_rate

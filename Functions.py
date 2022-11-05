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


def plot(x_points, y_points,graph_title, x_title,y_title ):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_points, y=y_points,
                            mode='lines', name='Signal Plot'))
    fig.update_layout(title=graph_title)
    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)
    st.plotly_chart(fig,use_container_width=True)



def frequencyDomain(signal, sample_rate):
    """
    fourier transform to frequency domain
    :param 
        signal: list of time domain signal points 
        sample_rate: int of sample rate for signal (Hz)
    :return: average temperature
    """
    freq = np.fft.rfft(signal)
    freq_magnitude= np.abs(freq)
    freq_phase=np.angle(freq,deg=False)
    fft_spectrum = np.fft.rfftfreq(signal.size, 1/sample_rate)
    return  freq_magnitude,freq_phase,fft_spectrum



def edit_frequency(freq_spectrum,freq_magnitude,sample_rate, edit_list):
    """
    edit frequecny range with ceratin gain
    :equation used
        Gain(dB)= 10log(new_frequency_power/new_frequency_power)
    :param 
        freq_spectrum : list of frequencies values in a certain signal
        freq_magnitude :  list of frequencies magnitudes in a certain signal
        sample_rate: int of sample rate for signal (Hz)
        edit_list: list of objects with a structrue:
                    [......{frequency_1: 5, frequency_2: 10, gain_db:2}]
                        frequency_1: start range of frequencies to be changed
                        frequency_2: end range of frequencies to be changed
                        gain_db: gain value ti change in decieble scale
    :return: list of edited frequency magnitudes 
    """
    frequency_points= len(freq_spectrum)/(sample_rate/2)
    for edit in edit_list:
        freq_magnitude[int(frequency_points*edit["frequency_1"]):int((frequency_points*edit["frequency_2"]))]= np.sqrt((10**(edit['gain_db']/10)*(freq_magnitude[int(frequency_points*edit["frequency_1"]):int((frequency_points*edit["frequency_2"]))]**2)))
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
    complex_rect = mag * np.cos(phase)+ 1j*mag * np.sin(phase)
    inverse_forurier= np.fft.irfft(complex_rect)
    return inverse_forurier



def signal_to_wav(signal,sample_rate):
    """
    convert signal array to a wav form saved in file.wav
    :param 
        signal : list of signal points in time domain
        sample_rate :  signal sample rate 
    : no return:
    """
    signal=np.int16(signal)
    wavfile.write("file.wav",2*sample_rate,signal)
    return 
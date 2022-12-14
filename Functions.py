import matplotlib.pyplot as plt
import streamlit as st  # 🎈 data web app development
import pandas as pd  # read csv, df manipulation
import numpy as np
from scipy.io.wavfile import read
from scipy.io import wavfile
from scipy import signal
import altair as alt
import os
import streamlit.components.v1 as components
import time as time_1

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "build")
_vertical_slider = components.declare_component(
    "vertical_slider", path=build_dir)


def vertical_slider(value, step, min=min, max=max, key=None):
    slider_value = _vertical_slider(
        value=value, step=step, min=min, max=max, key=key, default=value)
    return slider_value


def readAudioFile(file_name):
    """
    open wav file and extract signal from 
    :param
        file_name : name of file uploaded
    : return: 2 lists [signal list amplitude- signal time list ] , audio time, sampling frequency, file player 
    """
    sample_freq, audio_data = read("Audios\\" + file_name)
    t_audio = len(audio_data) / sample_freq
    audio_palyer = open("Audios\\" + file_name, 'rb')
    time = np.linspace(0, t_audio, len(audio_data))
    return audio_data, time, t_audio, sample_freq, audio_palyer


def Sliders(sliderColumns, sliders_num):
    adjusted_data = []
    sliders = {}
    for idx in range(0, sliders_num):
        with sliderColumns[idx]:
            key = f'member{str(idx)}'
            sliders[f'slider_group_{key}'] = vertical_slider(
                0, 1, -20, 20, key)
            adjusted_data.append((idx, sliders[f'slider_group_{key}']))

    return adjusted_data


def graph_sample(time, main_signal, edited_signal):
    sampled_time = time[::50]
    sampled_signal = main_signal[::50]
    sampled_edited_signal = edited_signal[::50]
    max_1 = max(sampled_edited_signal)
    max_2 = max(sampled_signal)
    min_1 = min(sampled_edited_signal)
    min_2 = min(sampled_signal)
    return sampled_time, sampled_signal, sampled_edited_signal, min(min_1, min_2), max(max_1, max_2)


def plot(time, main_signal, edited_signal):
    if "loop_flag" not in st.session_state:
        st.session_state["loop_flag"] = True
    sampled_time, sampled_signal, sampled_edited_signal, min, max = graph_sample(
        time, main_signal, edited_signal)
    graph_placeholder = st.empty()
    if "chart" not in st.session_state:
        update_chart(sampled_time, sampled_signal,
                     sampled_edited_signal, min, max)
    if "counter" not in st.session_state:
        st.session_state["counter"] = 0

    while(st.session_state.graph_mode == "play" and st.session_state.loop_flag == True):
        for i in range(st.session_state.counter, len(sampled_time), 5):
            time_1.sleep(0.01)
            update_chart(sampled_time[i:i+200], sampled_signal[i:i+200],
                         sampled_edited_signal[i:i+200], min, max)
            graph_placeholder.altair_chart(
                st.session_state.chart, use_container_width=True)
            st.session_state.counter = i
        st.session_state.loop_flag = False
    graph_placeholder.altair_chart(
        st.session_state.chart, use_container_width=True)


def update_chart(time, input_amp, output_amp, min_y=-20, max_y=20):
    signal_dataframe = pd.DataFrame({
        'Time(s)': time,
        'Input Amplitude': input_amp,
        "Output Amplitude": output_amp
    })
    st.session_state["chart"] = alt.Chart(signal_dataframe).mark_line().encode(
        x=alt.X(alt.repeat("row"), type='quantitative'),
        y=alt.Y(alt.repeat("column"), type='quantitative', scale=alt.Scale(
            domain=[min_y, max_y]))
    ).properties(
        width=650,
        height=180
    ).repeat(
        row=["Time(s)"],
        column=['Input Amplitude', 'Output Amplitude']
    ).interactive()


def view_full_chart(time, input_signal, outpit_signal):
    sampled_time, sampled_signal, sampled_edited_signal, min, max = graph_sample(
        time, input_signal, outpit_signal)
    update_chart(sampled_time, sampled_signal, sampled_edited_signal, min, max)


def plotSpectrogram(amplitude, invAmplitude, fs, range):
    # Set general font size
    plt.rcParams['font.size'] = '16'
    fig, spec = plt.subplots(1, 2, sharey=True, figsize=(40, 10))
    fig.tight_layout(w_pad=5, pad=10)

    if(not st.session_state.spectro_mode):
        spec[0].plot([], [])
        spec[1].plot([], [])
    else:
        N = 512
        w = signal.blackman(N)
        nFreqs, nTime, nPxx = signal.spectrogram(
            amplitude, fs, window=w, nfft=N)

        invFreqs, invTime, invPXX = signal.spectrogram(
            invAmplitude, fs, window=w, nfft=N)
        pcm1 = spec[0].pcolormesh(nTime, nFreqs, np.log(nPxx))
        fig.colorbar(pcm1, ax=spec[0])
        pcm2 = spec[1].pcolormesh(
            invTime, invFreqs, np.log(np.round(invPXX, 30)))
        fig.colorbar(pcm2, ax=spec[1])

    spec[0].set_xlabel(xlabel='Time [sec]', size=30)
    spec[0].set_ylabel(ylabel='Frequency (Hz)', size=30)

    spec[1].set_xlabel(xlabel='Time [sec]', size=30)

    st.pyplot(fig)


def frequencyDomain(signal_data, sampleFrequency):
    """
    fourier transform to frequency domain
    :param
        signal_data: list of time domain signal points
        sampleFrequency: int of sample rate for signal (Hz)
    :return: 2 lists (1- frequency value , 2- frequency spectrum(x-axis))
    """
    freq = np.fft.rfft(signal_data)
    fft_spectrum = np.fft.rfftfreq(signal_data.size, 1/sampleFrequency)
    return freq, fft_spectrum


def edit_frequency(freq_spectrum, freq_values, sample_freq, edit_list):
    """
    edit frequecny range with ceratin gain
    :equation used
        Gain(dB)= 10log(new_frequency/old_frequency)
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
        freq_values[int(frequency_points*edit["frequency_1"]):int((frequency_points*edit["frequency_2"]))] = (10**(
            edit['gain_db']/10)*(freq_values[int(frequency_points*edit["frequency_1"]):int((frequency_points*edit["frequency_2"]))]))
    return freq_values


def inverse_fourier(frequency_value):
    """
    return signal in time domain (Inverse Fourier)
    ** inverse with no data loss **
    :param
        frequency_value : list of frequencies values 
    :return: list of time domain signal after transformation
    """
    time_domain_signal = np.fft.irfft(frequency_value)
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


def refresh_graph():
    if "counter" in st.session_state:
        del st.session_state["counter"]
        del st.session_state["chart"]
        del st.session_state["loop_flag"]

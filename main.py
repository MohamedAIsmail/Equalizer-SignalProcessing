import streamlit as st
import streamlit_vertical_slider as svs
import Functions as fn
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title="Equalizer",page_icon=":bar_chart:", layout="wide")

col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

with col1:
    slider1 = svs.vertical_slider(key='Freq', step=1,
                                  min_value=1,
                                  max_value=100,
                                  slider_color='blue',  # optional
                                  track_color='lightgray',  # optional
                                  thumb_color='blue'  # optional
                                  )
uploadedAudio = st.file_uploader('Upload your audio here!')


if (uploadedAudio):
    audio_file, audio_player = fn.readAudioFile(uploadedAudio.name)
    sample_freq = audio_file.getframerate()
    n_samples = audio_file.getnframes()
    single_wave = audio_file.readframes(-1)
    t_audio = n_samples / sample_freq
    signal_array = fn.np.frombuffer(single_wave, dtype=fn.np.int16)
    time = fn.np.linspace(0, t_audio, n_samples)
    fn.plotTimeDomain(time,signal_array)
    freq_magnitude,frequency_spectrum_abs = fn.frequencyDomain(signal_array, sample_freq)
    fn.plotFrequencyDomain(frequency_spectrum_abs, freq_magnitude)
    st.audio(audio_player, format='audio/wav')
    # frequency_spectrum_abs= fn.edit_frequency(freq_magnitude,frequency_spectrum_abs,50,100,500)





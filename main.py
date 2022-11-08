import streamlit as st
import Functions as fn
import matplotlib.pyplot as plt
import json

st.set_page_config(page_title="Equalizer",
                   page_icon=":bar_chart:", layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

basic_data_file = open('data.json')
basic_data = json.load(basic_data_file)[0]

# Columns for GUI
left_col, right_col = st.columns((1, 4))
left_spectrogram_col, right_spectrogram_col, sub_right_spectrogram_col = st.columns(
    (1, 2, 2))
audio_left_col, audio_right_col = st.columns((1, 4))
sliders_cols = st.columns((1.01, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
labels_cols = st.columns(11)

with st.container():
    apply_btn = st.button('Apply Changes')

with left_col:
    chosen_mode_index = st.selectbox('Select mode', range(
        len(basic_data["Modes"])), format_func=lambda x: basic_data["Modes"][x])
    uploaded_audio = st.file_uploader(
        'Upload your audio here!', accept_multiple_files=False, type=basic_data["Extension"][chosen_mode_index])

# Saving the value of the sliders in a list [(1,0), (2,9)] ..
slider_data = fn.Sliders(sliders_cols, len(
    basic_data["Labels"][chosen_mode_index]))

alphabetList = [{'frequency_1': 100, 'frequency_2': 700, 'gain_db': slider_data[0][1]},
                {'frequency_1': 700, 'frequency_2': 800,
                    'gain_db': slider_data[1][1]},
                {'frequency_1': 800, 'frequency_2': 1200,
                    'gain_db': slider_data[2][1]},
                {'frequency_1': 2000, 'frequency_2': 4000,
                    'gain_db': slider_data[3][1]},
                # {'frequency_1': 1500, 'frequency_2': 4000, 'gain_db': slider_data[4][1]}
                ]
for idx, i in enumerate(basic_data["Labels"][chosen_mode_index]):
    with labels_cols[idx]:
        if (idx == 0):
            st.header(basic_data["Labels"][chosen_mode_index][idx])
        else:
            st.text(basic_data["Labels"][chosen_mode_index][idx])

# musical mode
musicalList = [{'frequency_1': 0, 'frequency_2': 128, 'gain_db': slider_data[0][1]},  # bass
               {'frequency_1': 128, 'frequency_2': 550,
                   'gain_db': slider_data[1][1]},  # trombone
               {'frequency_1': 550, 'frequency_2': 1000,
                'gain_db': slider_data[2][1]},  # E-flat clarinet
               {'frequency_1': 1000, 'frequency_2': 2000,
                'gain_db': slider_data[3][1]},  # piccolo
               {'frequency_1': 2000, 'frequency_2': 4000,
                'gain_db': slider_data[4][1]},
               # {'frequency_1': 2000, 'frequency_2': 20000, 'gain_db': slider_data[4][1]}, #viola
               ]


if (uploaded_audio):
    if (chosen_mode_index == 2):
        signalData, time, sample_freq = fn.open_mat(
            uploaded_audio)
    else:
        signalData, time, timeRange, sample_freq, st.session_state.audio_player = fn.readAudioFile(
            uploaded_audio.name)  # Read audio file uploaded

    st.session_state.freq_magnitude, freq_phase, fft_spectrum = fn.frequencyDomain(
        signalData, sample_freq)
    maxFFT_spectrum = max(fft_spectrum)

    with left_col:
        spectro_mode = st.checkbox('Show Spectrogram')
    # ----------------------------------------------------- PLOTTING -------------------------------------

# Applying slider values on the frequency magnitude
    if (apply_btn):
        st.session_state.freq_magnitude = fn.edit_frequency(
            fft_spectrum, st.session_state.freq_magnitude, sample_freq, musicalList)
        st.session_state.inverseFourier = fn.inverse_fourier(
            st.session_state.freq_magnitude, freq_phase)
        st.session_state.audio_player = fn.signal_to_wav(
            st.session_state.inverseFourier, sample_freq)

    with right_col:  # Plot the normal signal
        if 'inverseFourier' not in st.session_state:
            st.session_state['inverseFourier'] = []
        fn.plot(time, signalData, st.session_state.inverseFourier,
                'Time (s)', 'Amplitude (mV)', timeRange)
        if (spectro_mode):
            fn.plotSpectrogram(signalData, st.session_state.inverseFourier,
                               sample_freq, 'Time (s)', 'Frequency (Hz)', timeRange)

    with audio_right_col:  # Audio Play
        st.audio(st.session_state.audio_player, format='audio/wav')


else:
    if 'audio_player' in st.session_state:
        del st.session_state['audio_player']
    if 'freq_magnitude' in st.session_state:
        del st.session_state['freq_magnitude']
    if 'inverseFourier' in st.session_state:
        del st.session_state['inverseFourier']
    with right_col:
        fn.plot([], [], [], 'Time (s)', 'Amplitude (mV)', 7)
    with audio_right_col:  # Audio Play
        with open('Audios/Default.wav', 'rb') as fp:
            st.audio(fp, format='audio/wav')

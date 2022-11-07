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
left_col, right_col, sub_right_col = st.columns((1, 2, 2))
left_spectrogram_col, right_spectrogram_col, sub_right_spectrogram_col = st.columns(
    (1, 2, 2))
audio_left_col, audio_right_col = st.columns((1, 4))
sliders_cols = st.columns((1.01, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
labels_cols = st.columns(11)

with st.container():
    apply_btn = st.button('Apply Changes')

with left_col:
    uploaded_audio_placeholder=st.empty()
    uploaded_audio = uploaded_audio_placeholder.file_uploader('Upload your audio here!',accept_multiple_files=False,type=basic_data["Extension"][0],key="uploader")
    chosen_mode_index = st.selectbox('Select mode', range(len(basic_data["Modes"])), format_func=lambda x: basic_data["Modes"][x])
    uploaded_audio = uploaded_audio_placeholder.file_uploader('Upload your audio here!',accept_multiple_files=False,type=basic_data["Extension"][chosen_mode_index])


# Saving the value of the sliders in a list [(1,0), (2,9)] ..
slider_data = fn.Sliders(sliders_cols)

alphabetArr = [('Alphabet'), ('A'), ('B'), ('C'), ('D'), ('E'),
               ('F'), ('G'), ('H'), ('I'), ('J')]
alphabetList = [{'frequency_1': 100, 'frequency_2': 700, 'gain_db': slider_data[0][1]}, {
    'frequency_1': 700, 'frequency_2': 800, 'gain_db': slider_data[1][1]}, {'frequency_1': 800, 'frequency_2': 1200, 'gain_db': slider_data[2][1]},
    {'frequency_1': 1200, 'frequency_2': 1500, 'gain_db': slider_data[3][1]}, {'frequency_1': 1500, 'frequency_2': 4000, 'gain_db': slider_data[4][1]}]

for idx, i in enumerate(alphabetArr):
    with labels_cols[idx]:
        if (idx == 0):
            st.header(alphabetArr[idx])
        else:
            st.text(alphabetArr[idx])


if (uploaded_audio):
    audio_data, sample_freq, st.session_state.audio_player = fn.readAudioFile(
        uploaded_audio.name)  # Read audio file uploaded
    t_audio = len(audio_data) / sample_freq         
    if 'audio_data' not in st.session_state:
        st.session_state['audio_data'] = audio_data
    time = fn.np.linspace(0, t_audio, len(audio_data))
    st.session_state.freq_magnitude, freq_phase, fft_spectrum = fn.frequencyDomain(
        st.session_state.audio_data, sample_freq)
    maxFFT_spectrum = max(fft_spectrum)

    with left_col:
        spectro_mode = st.checkbox('Show Spectrogram')
    # ----------------------------------------------------- PLOTTING -------------------------------------

# Applying slider values on the frequency magnitude
    if (apply_btn):
        st.session_state.freq_magnitude = fn.edit_frequency(
            fft_spectrum, st.session_state.freq_magnitude, sample_freq, alphabetList)

        st.session_state.audio_data = fn.inverse_fourier(
            st.session_state.freq_magnitude, freq_phase)

        st.session_state.audio_player = fn.signal_to_wav(
            st.session_state.audio_data, sample_freq)

    with right_col:  # Plot the normal signal
        fn.plot(time, st.session_state.audio_data, 'Time Domain',
                'Time (s)', 'Amplitude (mV)', t_audio)

    with sub_right_col:  # Plot the frequency domain
        fn.plot(fft_spectrum, st.session_state.freq_magnitude, 'Frequency Domain',
                'Frequency (Hz)', 'Magnitude', 1400)

    with audio_right_col:  # Audio Play
        st.audio(st.session_state.audio_player, format='audio/wav')

    if (spectro_mode):
        with right_spectrogram_col:
            fn.plotSpectrogram(st.session_state.audio_data,
                               sample_freq, 'Input Spectrogram')
        with sub_right_spectrogram_col:
            fn.plotSpectrogram(
                st.session_state.freq_magnitude, sample_freq, 'Output Spectrogram')


else:
    if 'audio_player' in st.session_state:
        del st.session_state['audio_player']
    if 'freq_magnitude' in st.session_state:
        del st.session_state['freq_magnitude']
    if 'audio_data' in st.session_state:
        del st.session_state['audio_data']
    with right_col:
        fn.plot([], [6], 'Original Signal',
                'Time (s)', 'Amplitude (mV)', 7)
    with sub_right_col:
        fn.plot([], [], 'Frequency Domain',
                'Frequency (Hz)', 'Magnitude', 1000)
    with audio_right_col:  # Audio Play
        with open('Audios\Default.wav', 'rb') as fp:
            st.audio(fp, format='audio/wav')

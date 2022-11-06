import streamlit as st
import Functions as fn
import matplotlib.pyplot as plt

st.set_page_config(page_title="Equalizer",
                   page_icon=":bar_chart:", layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Columns for GUI
leftColumn, rightColumn, subRightColumn = st.columns((1, 2, 2))
leftSpectrogramColumn, rightSpectrogramColumn, subRightSpectrogramColumn = st.columns(
    (1, 2, 2))
audioLeftCol, audioRightCol = st.columns((1, 4))
sliderColumns = st.columns((1.01, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
textColumns = st.columns(11)

with st.container():
    Apply = st.button('Apply Changes')


with leftColumn:
    uploadedAudio = st.file_uploader('Upload your audio here!')
    selectMode = st.selectbox('Select mode', ('Musical Instruments', 'Vowels'))


# Saving the value of the sliders in a list [(1,0), (2,9)] ..
sliderData = fn.Sliders(sliderColumns)

alphabetArr = [('Alphabet'), ('A'), ('B'), ('C'), ('D'), ('E'),
               ('F'), ('G'), ('H'), ('I'), ('J')]
alphabetList = [{'frequency_1': 0, 'frequency_2': 50, 'gain_db': sliderData[0][1]}, {
    'frequency_1': 50, 'frequency_2': 100, 'gain_db': sliderData[1][1]}, {'frequency_1': 300, 'frequency_2': 500, 'gain_db': sliderData[2][1]},
    {'frequency_1': 500, 'frequency_2': 1000, 'gain_db': sliderData[3][1]}, {'frequency_1': 1000, 'frequency_2': 2000, 'gain_db': sliderData[4][1]}]

for idx, i in enumerate(alphabetArr):
    with textColumns[idx]:
        if (idx == 0):
            st.header(alphabetArr[idx])
        else:
            st.text(alphabetArr[idx])


if (uploadedAudio):

    # ---------------------------------------------- CALCULATIONS -----------------------------
    audio_file, st.session_state.audio_player = fn.readAudioFile(
        uploadedAudio.name)  # Read audio file uploaded

    # Calculate sample frequency from wav File
    sample_freq = audio_file.getframerate()
    n_samples = audio_file.getnframes()         # Get total number of samples
    # List containing magnitude values of signal
    single_wave = audio_file.readframes(-1)
    t_audio = n_samples / sample_freq           # Max time of the audio
    if 'audioData' not in st.session_state:
        st.session_state['audioData'] = fn.np.frombuffer(
            single_wave, dtype=fn.np.int16)
    time = fn.np.linspace(0, t_audio, n_samples)

    st.session_state.freq_magnitude, freq_phase, fft_spectrum = fn.frequencyDomain(
        st.session_state.audioData, sample_freq)
    maxFFT_spectrum = max(fft_spectrum)

    with leftColumn:
        spectroMode = st.checkbox('Show Spectrogram')

    # ----------------------------------------------------- PLOTTING -------------------------------------

# Applying slider values on the frequency magnitude
    if (Apply):
        st.session_state.freq_magnitude = fn.edit_frequency(
            fft_spectrum, st.session_state.freq_magnitude, sample_freq, alphabetList)

        st.session_state.audioData = fn.inverse_fourier(
            st.session_state.freq_magnitude, freq_phase)
        st.session_state.audio_player = fn.signal_to_wav(
            st.session_state.audioData, sample_freq)

    with rightColumn:  # Plot the normal signal
        fn.plot(time, st.session_state.audioData, 'Time Domain',
                'Time (s)', 'Amplitude (mV)', t_audio)
    with subRightColumn:  # Plot the frequency domain
        fn.plot(fft_spectrum, st.session_state.freq_magnitude, 'Frequency Domain',
                'Frequency (Hz)', 'Magnitude', 1400)

    with audioRightCol:  # Audio Play
        st.audio(st.session_state.audio_player, format='audio/wav')

    if (spectroMode):
        with rightSpectrogramColumn:
            fn.plotSpectrogram(st.session_state.audioData,
                               sample_freq, 'Input Spectrogram')
        with subRightSpectrogramColumn:
            fn.plotSpectrogram(
                st.session_state.freq_magnitude, sample_freq, 'Output Spectrogram')


else:
    with rightColumn:
        fn.plot([], [6], 'Original Signal',
                'Time (s)', 'Amplitude (mV)', 7)
    with subRightColumn:
        fn.plot([], [], 'Frequency Domain',
                'Frequency (Hz)', 'Magnitude', 1000)

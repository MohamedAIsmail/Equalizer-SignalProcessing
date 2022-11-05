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


alphabetArr = [('Alphabet'), ('A'), ('B'), ('C'), ('D'), ('E'),
               ('F'), ('G'), ('H'), ('I'), ('J')]


# Saving the value of the sliders in a list [(1,0), (2,9)] ..
sliderData = fn.Sliders(sliderColumns)


for idx, i in enumerate(alphabetArr):
    with textColumns[idx]:
        if (idx == 0):
            st.header(alphabetArr[idx])
        else:
            st.text(alphabetArr[idx])

if (uploadedAudio):
    # ---------------------------------------------- CALCULATIONS -----------------------------

    audio_file, audio_player = fn.readAudioFile(
        uploadedAudio.name)  # Read audio file uploaded

    # Calculate sample frequency from wav File
    sample_freq = audio_file.getframerate()
    n_samples = audio_file.getnframes()         # Get total number of samples
    # List containing magnitude values of signal
    single_wave = audio_file.readframes(-1)

    t_audio = n_samples / sample_freq           # Max time of the audio

    audioData = fn.np.frombuffer(single_wave, dtype=fn.np.int16)
    time = fn.np.linspace(0, t_audio, n_samples)
    maxTime = max(time)

    freq_magnitude, freq_phase, fft_spectrum = fn.frequencyDomain(
        audioData, sample_freq)
    maxFFT_spectrum = max(fft_spectrum)

    with leftColumn:
        spectroMode = st.checkbox('Show Spectrogram')
    if (Apply):
        freq_magnitude = fn.Equalizer(
            freq_magnitude, fft_spectrum, sample_freq)

    # ----------------------------------------------------- PLOTTING -------------------------------------
    with rightColumn:  # Plot the normal signal
        fn.plot(time, audioData, 'Original Signal',
                'Time (s)', 'Amplitude (mV)', maxTime)

    with subRightColumn:  # Plot the frequency domain
        fn.plot(fft_spectrum, freq_magnitude, 'Frequency Domain',
                'Frequency (Hz)', 'Magnitude', maxFFT_spectrum)

    with audioRightCol:  # Audio Play
        st.audio(audio_player, format='audio/wav')

    if (spectroMode):
        with rightSpectrogramColumn:
            fn.plotSpectrogram(audioData, sample_freq, 'Input Spectrogram')
        with subRightSpectrogramColumn:
            fn.plotSpectrogram(
                freq_magnitude, sample_freq, 'Output Spectrogram')
else:
    with rightColumn:
        fn.plot([], [6], 'Original Signal',
                'Time (s)', 'Amplitude (mV)', 7)
    with subRightColumn:
        fn.plot([], [], 'Frequency Domain',
                'Frequency (Hz)', 'Magnitude', 1000)

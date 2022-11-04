import streamlit as st
import streamlit_vertical_slider as svs
import Functions as fn
import matplotlib.pyplot as plt

st.set_page_config(page_title="Equalizer",
                   page_icon=":bar_chart:", layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


leftColumn, rightColumn, subRightColumn = st.columns((1, 2, 2))
with leftColumn:
    uploadedAudio = st.file_uploader('Upload your audio here!')
    selectMode = st.selectbox('Select mode', ())
    Apply = st.button('Apply Changes')


col1, slid1, slid2, slid3, slid4, slid5, slid6, slid7, slid8, slid9, slid10 = st.columns(
    11)
text, slid1text, slid2text, slid3text, slid4text, slid5text, slid6text, slid7text, slid8text, slid9text, slid10text = st.columns(
    11)

with text:
    st.header('Frequencies')

with slid1:
    slider1 = svs.vertical_slider(key='Freq1', step=1,
                                  min_value=1,
                                  max_value=100,
                                  slider_color='blue',  # optional
                                  track_color='lightgray',  # optional
                                  thumb_color='blue'  # optional
                                  )
with slid1text:
    st.text('100 - 200 Hz')


with slid2:
    slider2 = svs.vertical_slider(key='Freq2', step=1,
                                  min_value=1,
                                  max_value=100,
                                  slider_color='blue',  # optional
                                  track_color='lightgray',  # optional
                                  thumb_color='blue'  # optional
                                  )
with slid2text:
    st.text('200-1000 Hz')

with slid3:
    slider3 = svs.vertical_slider(key='Freq3', step=1,
                                  min_value=1,
                                  max_value=100,
                                  slider_color='blue',  # optional
                                  track_color='lightgray',  # optional
                                  thumb_color='blue'  # optional
                                  )
with slid3text:
    st.text('1000 - 2000 Hz')
with slid4:
    slider4 = svs.vertical_slider(key='Freq4', step=1,
                                  min_value=1,
                                  max_value=100,
                                  slider_color='blue',  # optional
                                  track_color='lightgray',  # optional
                                  thumb_color='blue'  # optional
                                  )
with slid5:
    slider5 = svs.vertical_slider(key='Freq5', step=1,
                                  min_value=1,
                                  max_value=100,
                                  slider_color='blue',  # optional
                                  track_color='lightgray',  # optional
                                  thumb_color='blue'  # optional
                                  )
with slid6:
    slider6 = svs.vertical_slider(key='Freq6', step=1,
                                  min_value=1,
                                  max_value=100,
                                  slider_color='blue',  # optional
                                  track_color='lightgray',  # optional
                                  thumb_color='blue'  # optional
                                  )
with slid7:
    slider7 = svs.vertical_slider(key='Freq7', step=1,
                                  min_value=1,
                                  max_value=100,
                                  slider_color='blue',  # optional
                                  track_color='lightgray',  # optional
                                  thumb_color='blue'  # optional
                                  )
with slid8:
    slider8 = svs.vertical_slider(key='Freq8', step=1,
                                  min_value=1,
                                  max_value=100,
                                  slider_color='blue',  # optional
                                  track_color='lightgray',  # optional
                                  thumb_color='blue'  # optional
                                  )
with slid9:
    slider9 = svs.vertical_slider(key='Freq9', step=1,
                                  min_value=1,
                                  max_value=100,
                                  slider_color='blue',  # optional
                                  track_color='lightgray',  # optional
                                  thumb_color='blue'  # optional
                                  )
with slid10:
    slider10 = svs.vertical_slider(key='Freq10', step=1,
                                   min_value=1,
                                   max_value=100,
                                   slider_color='blue',  # optional
                                   track_color='lightgray',  # optional
                                   thumb_color='blue'  # optional

                                   )

if (uploadedAudio):
    audio_file, audio_player = fn.readAudioFile(uploadedAudio.name)
    if (Apply):
        sample_freq = audio_file.getframerate()
        n_samples = audio_file.getnframes()
        single_wave = audio_file.readframes(-1)

        t_audio = n_samples / sample_freq

        signal_array = fn.np.frombuffer(single_wave, dtype=fn.np.int16)
        time = fn.np.linspace(0, t_audio, n_samples)

        with rightColumn:
            fn.plotTimeDomain(signal_array, time)

        signal_fd, time_fd = fn.frequencyDomain(
            signal_array, sample_freq)
        with subRightColumn:
            fn.plotFrequencyDomain(signal_fd, time_fd)

        st.audio(audio_player, format='audio/wav')
    else:

        with rightColumn:
            fn.plotTimeDomain([], [6])
        with subRightColumn:
            fn.plotFrequencyDomain([], [])
        st.audio(audio_player, format='audio/wav')
else:
    with rightColumn:
        fn.plotTimeDomain([], [6])
    with subRightColumn:
        fn.plotFrequencyDomain([], [])

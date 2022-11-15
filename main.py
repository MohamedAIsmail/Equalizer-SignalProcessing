import streamlit as st
import Functions as fn
import json

st.set_page_config(page_title="Equalizer",
                   page_icon=":bar_chart:", layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

basic_data_file = open('data.json')
basic_data = json.load(basic_data_file)[0]
if "graph_mode" not in st.session_state:
    st.session_state["graph_mode"] = "pause"

# Columns for GUI
margin_col2, play_col, replay_col, margin_col2 = st.columns((8.5, 1, 1, 5))
left_col, right_col = st.columns((1, 4))
margin_col, audio_left_col, audio_right_col = st.columns((1.01, 2, 2))


with left_col:
    chosen_mode_index = st.selectbox('Select mode', range(
        len(basic_data["Modes"])), format_func=lambda x: basic_data["Modes"][x])
    uploaded_audio = st.file_uploader(
        'Upload your audio here!', accept_multiple_files=False, type=basic_data["Extension"][chosen_mode_index])
    spectro_mode = st.checkbox('Show Spectrogram')
sliders_cols = st.columns(len(basic_data["Labels"][chosen_mode_index]))

# Saving the value of the sliders in a list [(1,0), (2,9)] ..
slider_data = fn.Sliders(sliders_cols, len(
    basic_data["Labels"][chosen_mode_index]))

for idx, i in enumerate(basic_data["Labels"][chosen_mode_index]):
    with sliders_cols[idx]:
        st.text(basic_data["Labels"][chosen_mode_index][idx])

edit_list = []
for counter in range(0, len(basic_data["Labels"][chosen_mode_index])):
    edit_list.append({'frequency_1': basic_data["freq_ranges"][chosen_mode_index][counter][0],
                     'frequency_2': basic_data["freq_ranges"][chosen_mode_index][counter][1], 'gain_db': slider_data[counter][1]})

if (uploaded_audio):
    signal_data, time, time_range, sample_freq, input_audio_player = fn.readAudioFile(
        uploaded_audio.name)
    if "edited_signal_player" not in st.session_state:
        st.session_state["edited_signal_player"] = input_audio_player
        st.session_state["edited_signal_time_domain"] = signal_data

    freq_magnitude, freq_phase, fft_spectrum = fn.frequencyDomain(
        signal_data, sample_freq)
    max_signal_freq = max(fft_spectrum)

    edited_freq_magnitude = fn.edit_frequency(
        fft_spectrum, freq_magnitude, sample_freq, edit_list)
    st.session_state.edited_signal_time_domain = fn.inverse_fourier(
        edited_freq_magnitude, freq_phase)
    st.session_state.edited_signal_player = fn.signal_to_wav(
        st.session_state.edited_signal_time_domain, sample_freq)

    with play_col:
        btn_placeholder = st.empty()
        if (st.session_state.graph_mode == "pause"):
            play_btn = btn_placeholder.button("▶")
        elif (st.session_state.graph_mode == "play"):
            play_btn = btn_placeholder.button("▐▐")
        if (play_btn):
            if (st.session_state.graph_mode == "pause"):
                st.session_state.graph_mode = "play"
                play_btn = btn_placeholder.button("▐▐ ")
                st.experimental_rerun()
            elif (st.session_state.graph_mode == "play"):
                st.session_state.graph_mode = "pause"
                play_btn = btn_placeholder.button("▶")
                st.experimental_rerun()
    with replay_col:
        replay_btn = st.button('↻')
        if(replay_btn):
            fn.refresh_graph()
            st.session_state.graph_mode = "play"
            st.experimental_rerun()
        with right_col:
            fn.plot(time, signal_data,
                    st.session_state.edited_signal_time_domain)
            if (spectro_mode):
                fn.plotSpectrogram(signal_data, st.session_state.edited_signal_time_domain,
                                   sample_freq, time_range)

    with audio_right_col:
        st.audio(st.session_state.edited_signal_player, format='audio/wav')
    with audio_left_col:
        st.audio(input_audio_player, format='audio/wav')


else:
    if "edited_signal_player" in st.session_state:
        del st.session_state["edited_signal_player"]
        fn.refresh_graph()
    with right_col:
        chart = fn.empty_plot()
        st.altair_chart(chart, use_container_width=True)
    with audio_right_col:
        with open('Audios/Default.wav', 'rb') as fp:
            st.audio(fp, format='audio/wav')
    with audio_left_col:
        with open('Audios/Default.wav', 'rb') as fp:
            st.audio(fp, format='audio/wav')

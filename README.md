# Equalizer - Signal Processing

---

## Table of contents

- [Introduction](#introduction)
- [Brief Explanation](#brief-explanation)
- [Features](#features)
- [Preview](#preview)
- [How to Run The Project](#run-the-project)
- [Team](#team)

### Introduction

- Website used for Equalizing audios (reducing and increasing specific audios according to the chosen mode of operation) through Signal Processing.

### Brief Explanation

- We process the signal by scaling a range of frequencies based on **Decibel scale** after applying **Fast Fourier Transfrom** on the audio uploaded, After the changes we invert the changed frequencies back to Time Domain then convert it back into audio format.

- Our application works in different modes such as:
   - Uniform Range Mode: The sampling frequency of the input audio (44.1k Hz) we divide it by 2 to get the maximum frequency then divide it uniformly into 8 equal ranges of frequencies, each is controlled by one slider in the UI.
   - Vowels Mode: Each slider can control the magnitude of specific vowel.
   - Musical Instruments Mode: Each slider can control the power of a specific musical instrument.
   - Animals Mode: Each slider can control the magnitude of a specific animal sound.
 



### Features

> Optimized software & fast processing speed
> Clean audio reconstruction
> Live dynamic plotting
![](Gifs/Live%20plotting%20preview.gif)
> Quick updates on spectrogram
![](Gifs/Live%20Spectrogram%20preview.gif)


### Run the Project 

1. Install Python3 on your computer
``` 
Download it from www.python.org/downloads/
```
2. Install the following modules
   - numpy
   - streamlit
   - matplotlib
   - pandas
   - numpy
   - scipy
   - altair
   - streamlit.components.v1
 - Open Project Terminal & Run the following command
```
pip install moudle-name
```
3. Start Server by Running 
```
streamlit run main.py
```

## Team

#### Equalizer

Digital Signal Processing (SBE3110) class project created by:

| Team Members' Names                                  | Section | B.N. |
|------------------------------------------------------|:-------:|:----:|
| [Mohamed Ahmed Ismail](https://github.com/1brahimmohamed) |    2    |  16   |
| [Romaisaa Sherif](https://github.com/Romaisaa)    |    1    |  36  |
| [Mariam Wael](https://github.com/MariamWaell)   |    2    |  36   |
| [Mariam Megahed](https://github.com/MaryamMegahed)    |    2    |  32  |


### Submitted to:

- Dr. Tamer Basha & Eng. Mohamed Mostafa

All rights reserved © 2022 to our Team - Systems & Biomedical Engineering, Cairo University (Class 2024)

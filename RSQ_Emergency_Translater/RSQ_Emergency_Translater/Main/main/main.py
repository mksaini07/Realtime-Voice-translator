from gtts import gTTS
import streamlit as st
import os
import speech_recognition as sr
import pygame
from googletrans import LANGUAGES, Translator

# varuabls
is_Trans_On = False
translator = Translator()
pygame.mixer.init()


lg_map = {name: code for code, name in LANGUAGES.items()}


def take_language_code(language_name):
    return lg_map.get(language_name, language_name)


def translator_fn(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src=from_language, dest=to_language)


def text_to_voice(text_data, to_language, speed="Normal"):
    slow_mode = True if speed == "Slow" else False
    obj = gTTS(text=text_data, lang=to_language, slow=slow_mode)
    obj.save("cache.mp3")
    
   
    if speed == "Fast":
        pygame.mixer.quit()
        pygame.mixer.init(frequency=44100) 
    elif speed == "Slow":
        pygame.mixer.quit()
        pygame.mixer.init(frequency=22050)  
    else:
        pygame.mixer.quit()
        pygame.mixer.init(frequency=44100)  
    
    audio = pygame.mixer.Sound("cache.mp3")
    audio.play()
    os.remove("cache.mp3")


def main_process(out_holder, from_language, to_language, mic_sensitivity, voice_speed):
    global is_Trans_On
    while is_Trans_On:
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            
            rec.energy_threshold = mic_sensitivity
            out_holder.markdown('<p class="status-text">Listening... 🎤</p>', unsafe_allow_html=True)
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)
        
        try:
            out_holder.markdown('<p class="status-text">Translating... 🔄</p>', unsafe_allow_html=True)
            spoken_text = rec.recognize_google(audio, language=from_language)
            
            out_holder.markdown('<p class="status-text">Speaking... 🔊</p>', unsafe_allow_html=True)
            translated_text = translator_fn(spoken_text, from_language, to_language)

            
            text_to_voice(translated_text.text, to_language, speed=voice_speed)
    
        except Exception as e:
            print(e)


def add_custom_css():
    st.markdown("""
    <style>
        /* Background gradient */
        .stApp {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            min-height: 100vh;
            color: white;
            font-family: 'Arial', sans-serif;
        }

        /* Header styling */
        .header {
            text-align: center;
            font-size: 1.8rem;
            padding: 15px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            margin-bottom: 20px;
            transition: transform 0.3s ease-in-out;
        }

        /* Hover effect for header */
        .header:hover {
            transform: scale(1.05);
        }

        /* Footer styling */
        .footer {
            text-align: center;
            font-size: 1rem;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            margin-top: 20px;
            position: fixed;
            bottom: 0;
            width: 100%;
            z-index: 999;
            transition: transform 0.3s ease-in-out;
        }

        /* Hover effect for footer */
        .footer:hover {
            transform: translateY(-5px);
        }

        /* Title styling */
        h1 {
            text-align: center;
            font-size: 3rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            animation: pulse 3s infinite;
        }

        /* Pulse animation for title */
        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
            100% {
                transform: scale(1);
            }
        }

        /* Button styling */
        .stButton>button {
            background-color: #ff6f61;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 1rem;
            border-radius: 10px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s, box-shadow 0.2s, background-color 0.3s;
        }

        /* Hover effect for buttons */
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.5);
            background-color: #e65c50; /* Slightly darker red */
        }

        /* Click effect for buttons */
        .stButton>button:active {
            transform: scale(0.95);
            box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
            background-color: #ff4d3b; /* Even darker red */
        }

        /* Status text styling */
        .status-text {
            text-align: center;
            font-size: 1.2rem;
            margin-top: 20px;
            animation: fadeInOut 2s infinite alternate;
        }

        /* Fade-in-out animation */
        @keyframes fadeInOut {
            0% {
                opacity: 0.8;
            }
            100% {
                opacity: 1;
            }
        }

        /* Dropdown drawer */
        .drawer {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-in-out, padding 0.3s ease-in-out;
            background-color: rgba(255, 255, 255, 0.1);
            padding: 0 10px;
            border-radius: 10px;
            margin-top: 10px;
        }

        /* Open drawer */
        .drawer.open {
            max-height: 300px; /* Adjust height as needed */
            padding: 10px;
        }

        /* Drawer content */
        .drawer-content {
            color: white;
            font-size: 1rem;
            line-height: 1.5;
        }

        /* Centered buttons */
        .center-buttons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)


add_custom_css()


st.markdown('<div class="header">RSQ Emergency Voice Translator</div>', unsafe_allow_html=True)

# Language selection 
col1, col2 = st.columns(2)
with col1:
    from_language_name = st.selectbox("Input Language:", list(LANGUAGES.values()))
with col2:
    to_language_name = st.selectbox("Output Language:", list(LANGUAGES.values()))

# Get language
from_language = take_language_code(from_language_name)
to_language = take_language_code(to_language_name)

st.markdown('<div class="center-buttons">', unsafe_allow_html=True)
start_button = st.button("Start 🎤")
stop_button = st.button("Stop ⏹️")
st.markdown('</div>', unsafe_allow_html=True)


out_holder = st.empty()


if 'mic_sensitivity' not in st.session_state:
    st.session_state.mic_sensitivity = 300  
if 'voice_speed' not in st.session_state:
    st.session_state.voice_speed = "Normal"  
if 'drawer_open' not in st.session_state:
    st.session_state.drawer_open = False


if st.button("⚙️ Settings"):
    st.session_state.drawer_open = not st.session_state.drawer_open


if st.session_state.drawer_open:
    st.markdown('<div class="drawer open"><div class="drawer-content">', unsafe_allow_html=True)
    st.markdown("<h3>Settings</h3>", unsafe_allow_html=True)
    
   
    mic_sensitivity = st.slider("Adjust Microphone Sensitivity", 100, 500, st.session_state.mic_sensitivity)
    st.session_state.mic_sensitivity = mic_sensitivity

   
    voice_speed = st.selectbox(
        "Select Voice Speed",
        ["Fast", "Normal", "Slow"],
        index=["Fast", "Normal", "Slow"].index(st.session_state.voice_speed)
    )
    st.session_state.voice_speed = voice_speed

    
    st.markdown("<p><strong>Customize Languages:</strong></p>", unsafe_allow_html=True)
    st.button("Add Custom Language (Coming Soon!)")

    st.markdown("</div></div>", unsafe_allow_html=True)
else:
    st.markdown('<div class="drawer"></div>', unsafe_allow_html=True)


if start_button:
    if not is_Trans_On:
        is_Trans_On = True
        out_holder.markdown('<p class="status-text">Translation Started... 🎤</p>', unsafe_allow_html=True)
        main_process(out_holder, from_language, to_language, st.session_state.mic_sensitivity, st.session_state.voice_speed)

if stop_button:
    is_Trans_On = False
    out_holder.markdown('<p class="status-text">Translation Stopped. ⏹️</p>', unsafe_allow_html=True)

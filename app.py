import streamlit as st
import moviepy.editor as mp
import whisper
from googletrans import Translator
from gtts import gTTS
import os

def extract_audio(video_file, audio_path="temp.wav"):
    video = mp.VideoFileClip(video_file)
    video.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]

def translate_text(text, target_lang="ar"):
    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    return translated.text

def text_to_speech(text, lang="ar", output_path="translated_audio.mp3"):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)
    return output_path

def generate_srt(text, output_file="translation.srt"):
    lines = text.split('. ')
    with open(output_file, "w", encoding="utf-8") as f:
        for i, line in enumerate(lines):
            start = f"00:00:{i*5:02},000"
            end = f"00:00:{(i+1)*5:02},000"
            f.write(f"{i+1}\n{start} --> {end}\n{line.strip()}\n\n")
    return output_file

st.set_page_config(page_title="AI Video Translator", layout="centered")
st.title("مترجم الفيديو بالذكاء الاصطناعي")

uploaded_file = st.file_uploader("ارفع فيديو بصيغة MP4", type=["mp4"])
target_lang = st.selectbox("اختر اللغة المستهدفة", ["ar", "en", "fr", "es", "de"])

if uploaded_file:
    with open("uploaded_video.mp4", "wb") as f:
        f.write(uploaded_file.read())

    st.info("جارٍ استخراج الصوت من الفيديو...")
    audio_path = extract_audio("uploaded_video.mp4")

    st.info("جارٍ تحويل الصوت إلى نص...")
    original_text = transcribe_audio(audio_path)

    st.success("النص الأصلي:")
    st.write(original_text)

    st.info("جارٍ ترجمة النص...")
    translated_text = translate_text(original_text, target_lang)

    st.success("النص المترجم:")
    st.write(translated_text)

    if st.button("تحميل الترجمة الصوتية"):
        audio_output = text_to_speech(translated_text, target_lang)
        st.audio(audio_output, format="audio/mp3")
        with open(audio_output, "rb") as f:
            st.download_button("تحميل ملف MP3", f, file_name="translated_audio.mp3")

    with open("translated_text.txt", "w", encoding="utf-8") as f:
        f.write(translated_text)
    with open("translated_text.txt", "rb") as f:
        st.download_button("تحميل الترجمة كنص", f, file_name="translated_text.txt")

    if st.button("تحميل الترجمة كملف SRT"):
        srt_path = generate_srt(translated_text)
        with open(srt_path, "rb") as f:
            st.download_button("تحميل ملف الترجمة SRT", f, file_name="translated_subtitles.srt")
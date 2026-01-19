import streamlit as st
from googletrans import Translator
from gtts import gTTS
import tempfile
import time

st.set_page_config(page_title="AI Language Translator", page_icon="🌍")

st.title("🌍 AI Language Translation Tool")
st.write("Smart NLP-based translator with auto detection and speech output")

translator = Translator()

languages = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Russian": "ru"
}

text = st.text_area("✍️ Enter text to translate:", height=150)

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Source Language:", ["Auto Detect"] + list(languages.keys()))

with col2:
    target_lang = st.selectbox("Target Language:", list(languages.keys()))

if st.button("🔄 Translate"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        success = False

        # Try translation twice (fix first-time failure)
        for attempt in range(2):
            try:
                if source_lang == "Auto Detect":
                    result = translator.translate(text, dest=languages[target_lang])
                    detected = result.src
                else:
                    result = translator.translate(
                        text,
                        src=languages[source_lang],
                        dest=languages[target_lang]
                    )
                    detected = languages[source_lang]

                st.success("✅ Translation Successful")
                st.write(f"**Detected Source Language:** `{detected}`")
                st.text_area("🌐 Translated Text:", result.text, height=150)
                st.code(result.text)

                # Generate audio
                tts = gTTS(result.text, lang=languages[target_lang])
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                    tts.save(tmpfile.name)
                    st.audio(tmpfile.name, format="audio/mp3")

                success = True
                break

            except Exception as e:
                st.error(f"Error: {e}")
                time.sleep(1)

        if not success:
            st.error("❌ Translation failed. Please check internet and try again.")

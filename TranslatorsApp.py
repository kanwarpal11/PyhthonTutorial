import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
class TranslatorsApp(object):
    # 🌐 Language options
    language_options = {
        'English': 'en',
        'Hindi': 'hi',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de'
    }
    @staticmethod
    def get_language_choice(prompt, options):
        print(prompt)
        for i, lang in enumerate(options.keys(), 1):
            print(f"{i}. {lang}")
        choice = int(input("Enter choice (1-5): "))
        return list(options.items())[choice - 1]

    def capture_speech(lang_code):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Speak now...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio, language=lang_code)
                print(f"📝 You said: {text}")
                return text
            except sr.UnknownValueError:
                print("❌ Could not understand audio.")
            except sr.RequestError as e:
                print(f"❌ API error: {e}")
            return None

    def translate_text(text, src_lang, dest_lang):
        translator = Translator()
        translated = translator.translate(text, src=src_lang, dest=dest_lang)
        print(f"🌍 Translated: {translated.text}")
        return translated.text

    def speak_text(text, lang_code):
        tts = gTTS(text=text, lang=lang_code)
        tts.save("translated.mp3")
        sound = AudioSegment.from_mp3("translated.mp3")
        play(sound)
        print("Using ffmpeg at:", AudioSegment.converter)
        os.remove("translated.mp3")

    def main():
        print("🔄 Voice Translator App")

        input_lang_name, input_lang_code = TranslatorsApp.get_language_choice("Select input language:", TranslatorsApp.language_options)
        output_lang_name, output_lang_code = TranslatorsApp.get_language_choice("Select output language:", TranslatorsApp.language_options)
        # output_lang_name, output_lang_code = get_language_choice("Select output language:", language_options)

        # Capture speech
        spoken_text = TranslatorsApp.capture_speech(input_lang_code)
        if not spoken_text:
            return

        # Translate and speak
        translated_text = TranslatorsApp.translate_text(spoken_text, input_lang_code, output_lang_code)
        TranslatorsApp.speak_text(translated_text, output_lang_code)

  
if __name__ == "__main__":
 TranslatorsApp.main()

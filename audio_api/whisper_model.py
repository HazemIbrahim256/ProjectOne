import whisper

def transcribe_audio(self, audio_path, lang='ssss', model_path='medium'):
        model = whisper.load_model(model_path)
        if lang == 'ssss':
            result = model.transcribe(audio_path)
            text = result["text"]
        elif lang in ['en', 'es', 'ar', 'it']:
            result = model.transcribe(audio_path, language=lang)
            text = result["text"]
        else:
            return None
        return text
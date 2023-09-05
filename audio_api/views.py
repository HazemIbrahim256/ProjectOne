from .models import Audio
from .serializers import AudioSerializer
from django.http import JsonResponse
from googletrans import Translator
from .ner_model import perform_ner
import logging
import whisper
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

logger = logging.getLogger(__name__)


class AudioUploadView(APIView):
    parser_classes = (MultiPartParser, )
    
    def post(self, request, source_language, target_language):
        file_serializer = AudioSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()

            # Perform transcription
            audio_instance = file_serializer.instance
            transcribed_text = self.transcribe_audio(audio_instance.file.path, source_language)
            audio_instance.transcription = transcribed_text
            audio_instance.save()

            entities, entity_types, numbers = perform_ner(transcribed_text)

            # Translate transcribed text
            translated_text = self.translate_text(transcribed_text, target_language)

            return JsonResponse({
                'source_language': source_language,
                'target_language': target_language,
                'transcription': transcribed_text,
                'translation': translated_text,
                'entities': entities,
                'entity_types': entity_types,
                'numbers': numbers
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
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
    
    
    def translate_text(self, text, target_lang):
        translator = Translator()
        translated_text = translator.translate(text, dest=target_lang).text
        return translated_text


class AudioListView(APIView):
    def get(self, request):
        audios = Audio.objects.all()
        serializer = AudioSerializer(audios, many=True)
        return Response(serializer.data)



class AudioTranscriptionView(APIView):
    # Define the translate_text function within the class
    def translate_text(self, text, target_lang):
        translator = Translator()
        translated_text = translator.translate(text, dest=target_lang).text
        return translated_text

    def post(self, request, target_language,*args, **kwargs):
        data = request.data
        text = data.get("text")

        if not text:
            return JsonResponse({"error": "Empty text provided"}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     # Use the translate_text method
        #     target_lang = 'ar'  # Set your target language here
        #     translated_text = self.translate_text(text, target_lang)
        #     entity2, entity2_type, numbers = perform_ner(text)

        #     return JsonResponse({
        #         'translation': translated_text,
        #         'entities': entity2,
        #         'entity_types': entity2_type,
        #         'numbers': numbers
        #     }, status=status.HTTP_201_CREATED)
        try:
            entity2, entity2_type, numbers = perform_ner(text)
            translation = self.translate_text(text, target_language)  # Replace 'ar' with your target language

            response_data = {
                "translation": translation,
                "ner_output": entity2,  # Assuming entity2 is the list of NER entities
                "target_language": target_language,
                # Add other fields if needed
            }

            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
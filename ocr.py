import io
import os
from google.cloud import vision
from google.cloud import translate_v2 as translate

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()


def ocr_image(path_imagem):
    try:
        with io.open(path_imagem, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations
        if texts:
            return texts[0].description.replace("\n", " ")
        return None
    except Exception as e:
        print(f"Erro OCR: {e}")
        return None


def traduzir_texto(texto):
    try:
        if not texto:
            return None
        result = translate_client.translate(texto, target_language="pt")
        return result['translatedText']
    except:
        return "Erro tradução"

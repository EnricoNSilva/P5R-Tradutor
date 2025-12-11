import mss
import mss.tools
from ocr import ocr_image, traduzir_texto

def realizar_traducao_area(coords):
    """
    Captura a tela na área fornecida e realiza OCR + tradução.
    area_captura deve ser um dict com x1, y1, x2, y2
    """
    nome_arquivo = "captura_crop.png"

    try:
        monitor = {
            "top": int(coords["y1"]),
            "left": int(coords["x1"]),
            "width": int(coords["x2"] - coords["x1"]),
            "height": int(coords["y2"] - coords["y1"])
        }
        # Captura a tela
        with mss.mss() as sct:
            output = sct.grab(monitor)
            mss.tools.to_png(output.rgb, output.size, output=nome_arquivo)

        # 2. OCR
        print(">> Lendo imagem...")
        texto_ingles = ocr_image(nome_arquivo)
        
        if texto_ingles:
            print(f"🇺🇸 EN: {texto_ingles}")
            # 3. Tradução
            texto_pt = traduzir_texto(texto_ingles)
            print(f"🇧🇷 PT: {texto_pt}")
            return texto_pt
        else:
            print("❌ Nada detectado.")
            return "Texto não encontrado."

    except Exception as e:
        print(f"Erro no processamento: {e}")
        return f"Erro: {e}"
import time
import mss
import mss.tools
from ocr import ocr_image, traduzir_texto

def processar_captura(fila_texto, area_captura):
    """
    Captura a tela na área fornecida e realiza OCR + tradução.
    area_captura deve ser um dict com x1, y1, x2, y2
    """
    nome_arquivo = "captura_crop.png"
    fila_texto.put("CMD_HIDE")
    time.sleep(0.15)

    try:
        monitor = {
            "top": area_captura["y1"],
            "left": area_captura["x1"],
            "width": area_captura["x2"] - area_captura["x1"],
            "height": area_captura["y2"] - area_captura["y1"]
        }

        with mss.mss() as sct:
            output = sct.grab(monitor)
            mss.tools.to_png(output.rgb, output.size, output=nome_arquivo)

        fila_texto.put("CMD_LOADING")
        print(">> Lendo imagem...")

        texto_ingles = ocr_image(nome_arquivo)

        if texto_ingles:
            print(f"🇺🇸 EN: {texto_ingles}")
            texto_pt = traduzir_texto(texto_ingles)
            print(f"🇧🇷 PT: {texto_pt}")
            fila_texto.put(f"TXT:{texto_pt}")
        else:
            print("❌ Nada detectado.")
            fila_texto.put("TXT:Texto não encontrado.")

    except Exception as e:
        print(f"Erro: {e}")
        fila_texto.put("TXT:Erro interno.")

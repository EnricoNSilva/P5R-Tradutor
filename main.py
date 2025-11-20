import time
import mss
import mss.tools
from pynput import keyboard, mouse
import os
import io
import threading
import queue
import tkinter as tk
from google.cloud import vision
from google.cloud import translate_v2 as translate

# --- CONFIGURAÇÃO ---
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# --- SUAS COORDENADAS (Ajustadas conforme seu envio) ---
x1 = 870
y1 = 1400
x2 = 1904
y2 = 1607

# Largura e altura
LARGURA = x2 - x1
ALTURA = y2 - y1

area_captura = {"top": y1, "left": x1, "width": LARGURA, "height": ALTURA}

# --- FILA DE COMUNICAÇÃO ---
fila_texto = queue.Queue()

# Clientes Google
vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()

print("--- P5R Tradutor v3 (Correção Inception) ---")
print("F10: Traduzir | F9: Esconder | ESC: FECHAR FORÇADO")

# --- BACKEND ---
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
        if not texto: return None
        result = translate_client.translate(texto, target_language="pt")
        return result['translatedText']
    except: return "Erro tradução"

def processar_captura():
    nome_arquivo = "captura_crop.png"
    
    # 1. Manda esconder a janela para ela não sair na foto
    fila_texto.put("CMD_HIDE")
    
    # 2. Espera um tiquinho para o Windows processar o sumiço
    time.sleep(0.15) 
    
    try:
        # 3. Captura
        with mss.mss() as sct:
            output = sct.grab(area_captura)
            mss.tools.to_png(output.rgb, output.size, output=nome_arquivo)
        
        # 4. Manda aparecer de volta avisando que está lendo
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

def on_key_release(key):
    try:
        if key == keyboard.Key.delete:
            # MATADOR DE PROCESSO (Kill Switch)
            print("🛑 Encerrando forçado...")
            os._exit(0)
            return False

        if key == keyboard.Key.f10:
            t = threading.Thread(target=processar_captura)
            t.start()
        
        if key == keyboard.Key.f9:
            fila_texto.put("TOGGLE")

    except Exception as e:
        print(f"Erro teclado: {e}")

def on_click(x, y, button, pressed):
    if not pressed and button == mouse.Button.left:
        dentro_x = x1 <= x <= x2
        dentro_y = y1 <= y <= y2

        if not (dentro_x and dentro_y):
            fila_texto.put("CMD_HIDE_CLICK")

# --- FRONTEND (Overlay) ---
def iniciar_overlay():
    root = tk.Tk()
    root.title("Legenda P5R")
    
    root.overrideredirect(True)
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-alpha", 0.9) # Ajuste a transparência se quiser
    root.configure(bg='black')
    root.geometry(f"{LARGURA}x{ALTURA}+{x1}+{y1}")

    # Label Principal
    label = tk.Label(
        root, 
        text="--- AGUARDANDO F10 ---", 
        font=("Optima Nova Black", 32, "bold"), 
        fg="#FFFFFF", # Branco
        bg="black", 
        wraplength=LARGURA-20,
        justify="center"
    )
    label.pack(expand=True, fill='both', padx=10, pady=10)

    # VARIÁVEL DE ESTADO MANUAL
    # O Python não vai perguntar pro Windows, ele vai confiar nessa variável.
    estado = {"visivel": True} 

    def verificar_fila():
        try:
            while not fila_texto.empty():
                msg = str(fila_texto.get_nowait()).strip()
                
                # --- LÓGICA DE COMANDOS ---
                if msg.startswith("CMD_"):
                    
                    if msg == "CMD_HIDE":
                        root.withdraw()
                        root.update()
                        estado["visivel"] = False
                    
                    elif msg == "CMD_HIDE_CLICK":
                        # Só esconde se a gente sabe que está visível
                        if estado["visivel"]:
                            root.withdraw()
                            estado["visivel"] = False
                    
                    elif msg == "CMD_LOADING":
                        root.deiconify()
                        label.config(text="Traduzindo...", fg="#00FF00")
                        root.update()
                        estado["visivel"] = True

                # --- LÓGICA DE TEXTO ---
                elif msg.startswith("TXT:"):
                    texto_limpo = msg[4:] # Remove o prefixo "TXT:"
                    
                    if not estado["visivel"]:
                        root.deiconify()
                        estado["visivel"] = True
                    
                    label.config(text=texto_limpo, fg="#FFFFFF")

        except queue.Empty:
            pass
        
        root.after(50, verificar_fila)

    verificar_fila()

    key_listener = keyboard.Listener(on_release=on_key_release)
    key_listener.start()
    
    # Listener do mouse (agora monitorando o release para ser mais suave)
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    root.mainloop()

if __name__ == "__main__":
    iniciar_overlay()
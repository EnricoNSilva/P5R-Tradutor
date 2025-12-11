# overlay.py
import tkinter as tk
from input_handlers import create_input_listeners

def iniciar_overlay(area):
    """
    Inicia o overlay de tradução na tela.
    Recebe a área selecionada como dicionário:
    {
        "x1": ...,
        "y1": ...,
        "x2": ...,
        "y2": ...
    }
    """

    # Cria fila de comunicação com listeners do teclado e mouse
    fila_texto = create_input_listeners(area)

    # Calcula dimensões da janela
    x1 = area["x1"]
    y1 = area["y1"]
    largura = area["x2"] - area["x1"]
    altura = area["y2"] - area["y1"]

    # Configuração da janela Tkinter
    root = tk.Tk()
    root.title("Legenda P5R")
    root.overrideredirect(True)
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-alpha", 0.9)
    root.configure(bg='black')
    root.geometry(f"{largura}x{altura}+{x1}+{y1}")

    # Label para exibir o texto traduzido
    label = tk.Label(
        root,
        text="--- AGUARDANDO F10 ---",
        font=("Optima Nova Black", 32, "bold"),
        fg="#FFFFFF",
        bg="black",
        wraplength=largura - 20,
        justify="center"
    )
    label.pack(expand=True, fill='both', padx=10, pady=10)

    # Estado do overlay (visível ou oculto)
    estado = {"visivel": True}

    # Função para verificar a fila e atualizar a interface
    def verificar_fila():
        try:
            while not fila_texto.empty():
                msg = str(fila_texto.get_nowait()).strip()

                # ------------------------------
                # COMANDOS DE CONTROLE
                # ------------------------------
                if msg.startswith("CMD_"):
                    if msg == "CMD_HIDE":
                        root.withdraw()
                        estado["visivel"] = False

                    elif msg == "CMD_HIDE_CLICK":
                        if estado["visivel"]:
                            root.withdraw()
                            estado["visivel"] = False

                    elif msg == "CMD_LOADING":
                        root.deiconify()
                        label.config(text="Traduzindo...", fg="#00FF00")
                        estado["visivel"] = True

                # ------------------------------
                # TEXTO PARA MOSTRAR
                # ------------------------------
                elif msg.startswith("TXT:"):
                    texto_limpo = msg[4:]
                    if not estado["visivel"]:
                        root.deiconify()
                        estado["visivel"] = True

                    label.config(text=texto_limpo, fg="#FFFFFF")

        except:
            pass

        # Verifica a fila a cada 50ms
        root.after(50, verificar_fila)

    # Inicia verificação da fila
    verificar_fila()
    root.mainloop()

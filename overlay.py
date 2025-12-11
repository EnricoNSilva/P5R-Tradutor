import tkinter as tk
import tkinter.font as tkfont
import threading
import queue
from input_handlers import iniciar_listeners
from captura import realizar_traducao_area

class P5RTranslatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("P5R Tradutor")
        
        # Configurações iniciais da janela (começa escondida)
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.configure(bg='black')

        # --- VARIÁVEIS DE ESTADO ---
        self.estado = "IDLE" 
        self.coords_selecao = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}
        self.fila = queue.Queue()

        # --- ELEMENTOS DE UI ---
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey15")
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # 2. Label para resultado (Texto)
        self.label = tk.Label(
            self.root, 
            text="Carregando...", 
            font=("Optima Nova Black", 16, "bold"), # Ajuste sua fonte aqui
            fg="#FFFFFF", 
            bg="black", 
            justify="center"
        )

        iniciar_listeners(self.fila)
        # Loop de verificação
        self.verificar_fila()

    def run(self):
        self.root.mainloop()

    def verificar_fila(self):
        try:
            while not self.fila.empty():
                tipo, dados = self.fila.get_nowait()
                
                if tipo == "EVENT_F10":
                    self.iniciar_selecao()
                
                elif tipo == "EVENT_CLICK":
                    # Se clicar fora enquanto mostra o resultado, esconde
                    if self.estado == "SHOWING":
                        x_click, y_click = dados
                        if not self.clique_foi_dentro(x_click, y_click):
                            self.esconder_tudo()

                elif tipo == "RESULTADO_PRONTO":
                    self.mostrar_resultado(dados)

        except queue.Empty:
            pass
        
        self.root.after(50, self.verificar_fila)

    # --- LÓGICA DE ESTADOS ---

    def iniciar_selecao(self):
        """Entra no modo de seleção (Tela cheia transparente)"""
        print(">> Modo Seleção Iniciado")
        self.estado = "SELECTING"
        self.root.deiconify()
        
        # Configura para tela cheia transparente
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        self.root.geometry(f"{largura_tela}x{altura_tela}+0+0")
        self.root.attributes("-alpha", 0.3)
        
        # Mostra Canvas, Esconde Label
        self.label.pack_forget()
        self.canvas.pack(fill="both", expand=True)
        self.canvas.delete("all")

    def esconder_tudo(self):
        """Volta para o modo background"""
        self.root.withdraw()
        self.estado = "IDLE"

    def mostrar_resultado(self, texto):
        """Configura a janela para mostrar apenas o texto na posição certa"""
        self.estado = "SHOWING"
        
        # Dimensões da caixa desenhada
        x = self.coords_selecao["x1"]
        y = self.coords_selecao["y1"]
        w = max(self.coords_selecao["x2"] - x, 50) 
        h = max(self.coords_selecao["y2"] - y, 50)

        # Calcula qual fonte cabe dentro de w (largura) e h (altura)
        tamanho_ideal = self.calcular_melhor_fonte(texto, w, h)

        # Configura visual
        self.canvas.pack_forget()
        self.label.config(text=texto, font=("Optima Nova Black", tamanho_ideal, "bold"), wraplength=w-10)
        self.label.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.attributes("-alpha", 0.9)
        self.root.deiconify()

    def calcular_melhor_fonte(self, texto, largura_box, altura_box):
        """
        Tenta tamanhos de fonte do maior (32) para o menor (10)
        até encontrar um que caiba na caixa desenhada.
        """
        tamanho = 32 
        minimo = 8 
        
        pad_x = 20
        pad_y = 20
        largura_util = largura_box - pad_x

        while tamanho > minimo:
            
            fonte_teste = tkfont.Font(family="Optima Nova Black", size=tamanho, weight="bold")
            
            largura_texto_total = fonte_teste.measure(texto)
            
            # (Largura Total / Largura da Caixa) + 1 linha extra por garantia
            linhas_estimadas = int(largura_texto_total / largura_util) + 1
            
            # Se o texto tiver quebras de linha manuais (\n), ajustamos
            linhas_quebras_manuais = texto.count('\n') + 1
            linhas_estimadas = max(linhas_estimadas, linhas_quebras_manuais)

            # Calcular altura total necessária (Linhas * Altura de cada linha)
            altura_linha = fonte_teste.metrics("linespace")
            altura_necessaria = linhas_estimadas * altura_linha
            
            # Verificar se cabe na altura da caixa
            if altura_necessaria <= (altura_box - pad_y):
                return tamanho 
            
            tamanho -= 2 # Não coube, diminui a fonte e tenta de novo
        
        return minimo # Se nada der certo, retorna o mínimo
    
    # --- LÓGICA DE MOUSE (SELEÇÃO) ---

    def on_mouse_down(self, event):
        self.coords_selecao["x1"] = event.x
        self.coords_selecao["y1"] = event.y

    def on_mouse_drag(self, event):
        self.canvas.delete("rect")
        self.canvas.create_rectangle(
            self.coords_selecao["x1"], self.coords_selecao["y1"],
            event.x, event.y,
            outline="red", width=2, tag="rect"
        )

    def on_mouse_up(self, event):
        # 1. Salva coordenadas finais
        self.coords_selecao["x2"] = event.x
        self.coords_selecao["y2"] = event.y
        
        # Garante ordem correta (x1 < x2)
        x1, x2 = sorted([self.coords_selecao["x1"], self.coords_selecao["x2"]])
        y1, y2 = sorted([self.coords_selecao["y1"], self.coords_selecao["y2"]])
        self.coords_selecao = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}

        # 2. Esconde UI temporariamente e inicia processamento
        self.root.withdraw() # Esconde pra não sair no print
        
        # Inicia thread de processamento
        t = threading.Thread(target=self.thread_processamento)
        t.start()

    def thread_processamento(self):
        import time
        time.sleep(0.1)
        
        # Realiza a tradução
        texto = realizar_traducao_area(self.coords_selecao)
        
        # Devolve pra UI
        self.fila.put(("RESULTADO_PRONTO", texto))

    def clique_foi_dentro(self, x, y):
        c = self.coords_selecao
        return (c["x1"] <= x <= c["x2"]) and (c["y1"] <= y <= c["y2"])
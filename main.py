from utils import configurar_dpi # ajustar a escala de DPI no Windows
from overlay import P5RTranslatorApp

def main():

    configurar_dpi() # Precisa ser chamado antes de qualquer coisa no Windows

    print("O programa está rodando em segundo plano.")
    print("-> Pressione F10 para Selecionar e Traduzir.")
    print("-> Clique fora da tradução para fechar.")
    print("-> Pressione DELETE para encerrar.")

    app = P5RTranslatorApp()
    app.run()

if __name__ == "__main__":
    main()
from utils import configurar_dpi # ajustar a escala de DPI no Windows
from pegar_area import selecionar_area
from overlay import iniciar_overlay

def main():

    configurar_dpi() # Precisa ser chamado antes de qualquer coisa no Windows

    print("--- P5R Tradutor v3 (Correção Inception) ---")
    print("F10: Traduzir | F9: Esconder | ESC: FECHAR FORÇADO")

    area = selecionar_area()
    print("\n=== ÁREA DEFINIDA ===")
    print(f"x1 = {area['x1']}")
    print(f"y1 = {area['y1']}")
    print(f"x2 = {area['x2']}")
    print(f"y2 = {area['y2']}")
    print("=====================\n")

    iniciar_overlay(area)

if __name__ == "__main__":
    main()
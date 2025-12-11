import threading
from pynput import keyboard, mouse
from queue import Queue

fila_texto = Queue()


def on_key_release(key, area):
    """
    Trata os eventos de teclado.
    """
    try:
        if key == keyboard.Key.delete:
            print("🛑 Encerrando forçado...")
            import os
            os._exit(0)
            return False

        if key == keyboard.Key.f10:
            if not area:
                print("⚠ Nenhuma área selecionada!")
                return
            # Lazy import para evitar circular import
            from captura import processar_captura
            t = threading.Thread(target=processar_captura, args=(fila_texto, area))
            t.start()

        if key == keyboard.Key.f9:
            fila_texto.put("TOGGLE")

    except Exception as e:
        print(f"Erro teclado: {e}")


def create_input_listeners(area_capturada):
    """
    Cria listeners de teclado e mouse e retorna a fila de mensagens.
    """

    key_listener = keyboard.Listener(
        on_release=lambda key: on_key_release(key, area_capturada)
    )
    key_listener.start()

    def on_click(x, y, button, pressed):
        if not pressed and button == mouse.Button.left:
            dentro_x = area_capturada["x1"] <= x <= area_capturada["x2"]
            dentro_y = area_capturada["y1"] <= y <= area_capturada["y2"]
            if not (dentro_x and dentro_y):
                fila_texto.put("CMD_HIDE_CLICK")

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    return fila_texto

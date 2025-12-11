from pynput import keyboard, mouse

def iniciar_listeners(fila_eventos):
    """
    Inicia os listeners globais e envia eventos para a fila.
    """
    
    # --- TECLADO ---
    def on_release(key):
        try:
            if key == keyboard.Key.f10:
                fila_eventos.put(("EVENT_F10", None))
            elif key == keyboard.Key.delete:
                import os
                print("🛑 Encerrando (DELETE)...")
                os._exit(0)
        except Exception:
            pass

    # --- MOUSE ---
    def on_click(x, y, button, pressed):
        # Detecta quando solta o clique (Release) para evitar conflitos
        if not pressed and button == mouse.Button.left:
            fila_eventos.put(("EVENT_CLICK", (x, y)))

    # Inicia as threads dos listeners
    kb_listener = keyboard.Listener(on_release=on_release)
    kb_listener.start()

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
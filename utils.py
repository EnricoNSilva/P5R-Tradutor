import ctypes

def configurar_dpi():
    """
    Ajusta a escala de DPI para que o Windows não distorça
    a resolução da captura e do overlay.
    """
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass
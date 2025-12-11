import tkinter as tk

def selecionar_area():
    """
    Abre uma tela fullscreen para o usuário selecionar uma área.
    Retorna um dicionário com as coordenadas:
    {
        "x1": int,
        "y1": int,
        "x2": int,
        "y2": int
    }
    """
    coords = {}

    def on_mouse_down(event):
        coords["x1"] = event.x_root
        coords["y1"] = event.y_root
        canvas.delete("rect")

    def on_mouse_drag(event):
        canvas.delete("rect")
        canvas.create_rectangle(
            coords["x1"], coords["y1"],
            event.x_root, event.y_root,
            outline="red",
            width=2,
            tag="rect"
        )

    def on_mouse_up(event):
        coords["x2"] = event.x_root
        coords["y2"] = event.y_root

        print("\n=== ÁREA CAPTURADA ===")
        print(f"x1 = {coords['x1']}")
        print(f"y1 = {coords['y1']}")
        print(f"x2 = {coords['x2']}")
        print(f"y2 = {coords['y2']}")
        print("======================\n")

        root.destroy()

    root = tk.Tk()
    root.title("Selecione a Área de Tradução")
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.25)
    root.attributes("-topmost", True)
    root.configure(bg="black")

    canvas = tk.Canvas(root, bg="black")
    canvas.pack(fill="both", expand=True)

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()

    return coords

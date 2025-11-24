import tkinter as tk
from tkinter import messagebox
import json

# ============================================================
#   FENÊTRE POP-UP : OUVERTURE D'UNE AFFAIRE
# ============================================================
def ouvrir_affaire(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            affaire = json.load(f)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir l'affaire :\n{e}")
        return

    popup = tk.Toplevel()
    popup.title(affaire.get("titre", "Affaire"))
    popup.geometry("750x650")

    top_bar = tk.Frame(popup, bg="#f8f8f8")
    top_bar.pack(fill="x")

    tk.Label(
        top_bar,
        text=affaire["titre"],
        font=("Arial", 20, "bold"),
        bg="#f8f8f8"
    ).pack(side="left", padx=15, pady=10)

    tk.Button(
        top_bar,
        text="Modifier ✎",
        font=("Arial", 12, "bold"),
        bg="#ececec",
        command=lambda: print("TODO: ouvrir interface modification")
    ).pack(side="right", padx=15, pady=10)

    canvas = tk.Canvas(popup, bg="white")
    scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas, bg="white")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    window_id = canvas.create_window((0, 0), window=frame, anchor="nw")

    def update_scroll(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    frame.bind("<Configure>", update_scroll)

    def resize_canvas(event):
        canvas.itemconfig(window_id, width=event.width)
    canvas.bind("<Configure>", resize_canvas)

    def _on_mousewheel(event):
        if event.delta:
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        else:
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

    popup.bind("<MouseWheel>", _on_mousewheel)
    popup.bind("<Button-4>", _on_mousewheel)
    popup.bind("<Button-5>", _on_mousewheel)

    def add_title(text):
        tk.Label(frame, text=text, font=("Arial", 16, "bold"),
                 bg="white").pack(anchor="w", pady=(15, 5))

    def add_label(text):
        tk.Label(frame, text=text, font=("Arial", 12),
                 bg="white", wraplength=700, justify="left").pack(anchor="w", pady=3)

    add_title("Informations générales")
    add_label(f"📅 Date : {affaire.get('date', '—')}")
    add_label(f"📍 Lieu : {affaire.get('lieu', '—')}")
    add_label(f"🧩 Type : {affaire.get('type_affaire', '—')}")
    add_label(f"👮 Responsable : {affaire.get('responsables', '—')}")
    add_label(f"📌 État : {affaire.get('etat', '—')}")
    add_label(f"📊 Niveau d’urgence : {affaire.get('urgence', '—')}")

    add_title("Description")
    add_label(affaire.get("description", "Aucune description disponible."))

    add_title("Personnes impliquées")
    for p in affaire.get("personnes", []):
        tk.Label(frame,
                 text=f"{p.get('role','')} – {p.get('nom','')}",
                 font=("Arial", 13, "bold"),
                 bg="white").pack(anchor="w", pady=(8, 0))

        add_label(f"Identité : {p.get('identité','—')}")
        add_label(f"Adresse : {p.get('adresse','—')}")
        add_label(f"Contact : {p.get('contact','—')}")
        add_label(f"Liens : {p.get('liens','—')}")
        add_label(f"Notes : {p.get('historique','—')}")

    popup.mainloop()

import tkinter as tk
from gui.nouvelle_affaire import nouvelle_affaire_interface


def accueil(fenetre):
    for widget in fenetre.winfo_children():
        widget.destroy()

    fenetre.title("AffairTrack")

    bouton = tk.Button(
        fenetre,
        text="Nouvelle Affaire",
        command=lambda: nouvelle_affaire_interface(fenetre)
    )
    bouton.pack(fill="x", padx=20, pady=20)

    tk.Label(fenetre, text="Affaires en cours", anchor="w").pack(fill="x", padx=20, pady=20)
    tk.Label(fenetre, text="Affaires à surveiller", anchor="w").pack(fill="x", padx=20, pady=20)
    tk.Label(fenetre, text="Affaires gelées pour manque d'informations", anchor="w").pack(fill="x", padx=20, pady=20)
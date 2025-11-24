import tkinter as tk
from tkinter import ttk, messagebox

from gui.nouvelle_affaire import nouvelle_affaire_interface
from gui.ouvrir_affaire import ouvrir_affaire  # ← ajouté
from utils.loader import charger_affaires, trier_par_etat


# ============================================================
#   INTERFACE D'ACCUEIL
# ============================================================
def accueil(fenetre):

    # Nettoyage
    for widget in fenetre.winfo_children():
        widget.destroy()

    fenetre.title("AffairTrack")

    # ======================================
    #   BOUTON : NOUVELLE AFFAIRE
    # ======================================
    bouton = tk.Button(
        fenetre,
        text="Nouvelle Affaire",
        font=("Arial", 16, "bold"),
        padx=20,
        pady=15,
        height=2,
        command=lambda: nouvelle_affaire_interface(fenetre)
    )
    bouton.pack(fill="x", padx=40, pady=20)

    # ======================================
    #   SCROLLBAR PRINCIPALE
    # ======================================
    conteneur_scroll = tk.Frame(fenetre)
    conteneur_scroll.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(conteneur_scroll, orient="vertical")
    scrollbar.pack(side="left", fill="y")

    canvas = tk.Canvas(conteneur_scroll, highlightthickness=0, bg="#f0f0f0")
    canvas.pack(side="right", fill="both", expand=True)

    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=canvas.yview)

    frame_global = tk.Frame(canvas, bg="#f0f0f0")
    window_id = canvas.create_window((0, 0), window=frame_global, anchor="nw")

    def update_scrollregion(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    frame_global.bind("<Configure>", update_scrollregion)

    def resize_frame(event):
        canvas.itemconfig(window_id, width=event.width)
        update_scrollregion()
    canvas.bind("<Configure>", resize_frame)

    # Molette souris
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int(e.delta / 120), "units"))
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    # ======================================
    #   CHARGEMENT DES AFFAIRES
    # ======================================
    affaires = charger_affaires()
    en_cours, surveiller, gelee = trier_par_etat(affaires)

    # ======================================
    #   AFFICHAGE DES CARTES
    # ======================================
    # (inchangé, je le laisse dans accueil.py pour éviter modification)

    def afficher_cartes(frame_parent, liste_affaires):

        cards = []

        for affaire in liste_affaires:

            card = tk.Frame(
                frame_parent,
                bd=1,
                relief="solid",
                bg="white",
                width=320,
                height=210
            )

            card.pack_propagate(False)
            card.grid_propagate(False)

            card_inner = tk.Frame(card, bg="white")
            card_inner.pack(fill="both", expand=True, padx=10, pady=10)

            cards.append(card)

            tk.Label(card_inner, text=affaire["titre"], font=("Arial", 12, "bold"),
                     bg="white", wraplength=290, justify="left").pack(anchor="w")

            tk.Label(card_inner, text=f"📍 {affaire['lieu']}", bg="white").pack(anchor="w")
            tk.Label(card_inner, text=f"📅 Dernier mouvement : {affaire['date_dernier_mouvement']}", bg="white").pack(anchor="w")
            tk.Label(card_inner, text=f"🧩 {affaire['type_affaire']}", bg="white").pack(anchor="w")
            tk.Label(card_inner, text=f"👮 {affaire['responsable']}", bg="white").pack(anchor="w")

            tk.Label(
                card_inner,
                text=f"Victimes: {affaire['victimes']}   Suspects: {affaire['suspects']}   Témoins: {affaire['temoins']}",
                bg="white"
            ).pack(anchor="w")

            tk.Button(
                card_inner,
                text="Ouvrir",
                command=lambda p=affaire["path"]: ouvrir_affaire(p)
            ).pack(anchor="e", pady=5)

        def repositionner(event=None):
            largeur = frame_parent.winfo_width()
            carte_largeur = 340
            max_par_ligne = max(1, largeur // carte_largeur)

            row = col = 0
            for card in cards:
                card.grid_forget()
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nw")
                col += 1
                if col >= max_par_ligne:
                    col = 0
                    row += 1

        frame_parent.bind("<Configure>", repositionner)
        repositionner()

    # ======================================
    #   SECTIONS
    # ======================================
    tk.Label(frame_global, text="🟢 Affaires en cours", font=("Arial", 16, "bold"),
             bg="#f0f0f0").pack(anchor="w", pady=(10, 5))
    frame_en_cours = tk.Frame(frame_global, bg="#f0f0f0")
    frame_en_cours.pack(fill="x")
    afficher_cartes(frame_en_cours, en_cours)

    tk.Label(frame_global, text="🟡 Affaires à surveiller", font=("Arial", 16, "bold"),
             bg="#f0f0f0").pack(anchor="w", pady=(20, 5))
    frame_surveiller = tk.Frame(frame_global, bg="#f0f0f0")
    frame_surveiller.pack(fill="x")
    afficher_cartes(frame_surveiller, surveiller)

    tk.Label(frame_global, text="🔵 Affaires gelées", font=("Arial", 16, "bold"),
             bg="#f0f0f0").pack(anchor="w", pady=(20, 5))
    frame_gelee = tk.Frame(frame_global, bg="#f0f0f0")
    frame_gelee.pack(fill="x")
    afficher_cartes(frame_gelee, gelee)

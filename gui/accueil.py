import tkinter as tk
from gui.nouvelle_affaire import nouvelle_affaire_interface
from utils.loader import charger_affaires, trier_par_etat


def ouvrir_affaire(path):
    print("Ouverture de l'affaire :", path)
    # Met ici ton code pour ouvrir l'affaire


def accueil(fenetre):

    # Nettoyage
    for widget in fenetre.winfo_children():
        widget.destroy()

    fenetre.title("AffairTrack")

    # ================================
    #   BOUTON NOUVELLE AFFAIRE
    # ================================
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

    # ============================================
    #         ZONE SCROLLABLE + MOLETTE
    # ============================================
    canvas = tk.Canvas(fenetre, highlightthickness=0, bg="#f0f0f0")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(fenetre, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame_global = tk.Frame(canvas, bg="#f0f0f0")
    window_id = canvas.create_window((0, 0), window=frame_global, anchor="nw")

    def update_scrollregion(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_global.bind("<Configure>", update_scrollregion)

    def resize_frame(event):
        canvas_width = event.width
        canvas.itemconfig(window_id, width=canvas_width)
        update_scrollregion()

    canvas.bind("<Configure>", resize_frame)

    # ----- SCROLL SOURIS -----
    def _on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    # ================================
    #     CHARGEMENT DES AFFAIRES
    # ================================
    affaires = charger_affaires()
    en_cours, surveiller, gelee = trier_par_etat(affaires)

    # ============================================
    #     FLOW LAYOUT POUR LES CARTES
    # ============================================

    def afficher_cartes(frame_parent, liste_affaires):

        cards = []

        for affaire in liste_affaires:
            # ---------------------------
            #      CARTE UNIFORME
            # ---------------------------
            card = tk.Frame(
                frame_parent,
                bd=1,
                relief="solid",
                padx=10,
                pady=10,
                bg="white",
                width=320,     # ⭐ largeur uniforme
                height=210     # ⭐ hauteur uniforme
            )
            card.grid_propagate(False)
            cards.append(card)

            # TITRE
            tk.Label(
                card,
                text=affaire["titre"],
                font=("Arial", 12, "bold"),
                bg="white",
                wraplength=290,
                justify="left"
            ).pack(anchor="w")

            # INFORMATIONS PRINCIPALES
            tk.Label(card, text=f"📍 {affaire['lieu']}", bg="white", wraplength=290).pack(anchor="w")
            tk.Label(card, text=f"📅 {affaire['date_dernier_mouvement']}", bg="white").pack(anchor="w")
            tk.Label(card, text=f"🧩 {affaire['type_affaire']}", bg="white", wraplength=290).pack(anchor="w")
            tk.Label(card, text=f"👮 {affaire['responsable']}", bg="white", wraplength=290).pack(anchor="w")

            # Abréviations Vic / Sus / Tem
            tk.Label(
                card,
                text=f"Victimes: {affaire['victimes']}   Suspects: {affaire['suspects']}   Temoins: {affaire['temoins']}",
                bg="white"
            ).pack(anchor="w")

            # Bouton
            tk.Button(
                card,
                text="Ouvrir",
                command=lambda p=affaire["path"]: ouvrir_affaire(p)
            ).pack(anchor="e", pady=5)

        # --------- FLOW LAYOUT INTELLIGENT ---------
        def repositionner(event=None):
            largeur = frame_parent.winfo_width()
            if largeur < 50:
                return

            carte_largeur = 340  # largeur + marge
            max_par_ligne = max(1, largeur // carte_largeur)

            row = 0
            col = 0

            for card in cards:
                card.grid_forget()
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nw")
                col += 1

                if col >= max_par_ligne:
                    col = 0
                    row += 1

        frame_parent.bind("<Configure>", repositionner)
        repositionner()

    # ============================
    #   SECTIONS AFFAIRES
    # ============================

    tk.Label(frame_global, text="🟢 Affaires en cours", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(10, 5))
    frame_en_cours = tk.Frame(frame_global, bg="#f0f0f0")
    frame_en_cours.pack(fill="x")
    afficher_cartes(frame_en_cours, en_cours)

    tk.Label(frame_global, text="🟡 Affaires à surveiller", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(20, 5))
    frame_surveiller = tk.Frame(frame_global, bg="#f0f0f0")
    frame_surveiller.pack(fill="x")
    afficher_cartes(frame_surveiller, surveiller)

    tk.Label(frame_global, text="🔵 Affaires gelées", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(20, 5))
    frame_gelee = tk.Frame(frame_global, bg="#f0f0f0")
    frame_gelee.pack(fill="x")
    afficher_cartes(frame_gelee, gelee)

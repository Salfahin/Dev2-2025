import os
import tkinter as tk
from tkinter import messagebox

from gui.nouvelle_affaire import nouvelle_affaire_interface
from gui.ouvrir_affaire import ouvrir_affaire
from utils.loader import charger_affaires, trier_par_etat

# Stocke le bind global actuel (pour pouvoir le supprimer)
global_mousewheel_bind = False


# ============================================================
#   INTERFACE D'ACCUEIL
# ============================================================
def accueil(fenetre):
    global global_mousewheel_bind

    # Nettoyage de la fenêtre
    for widget in fenetre.winfo_children():
        widget.destroy()

    # Désactive d'éventuels anciens scrolls globaux
    if global_mousewheel_bind:
        fenetre.unbind_all("<MouseWheel>")
        fenetre.unbind_all("<Button-4>")
        fenetre.unbind_all("<Button-5>")
        global_mousewheel_bind = False

    fenetre.title("AffairTrack")

    # ======================================
    #   BOUTONS : NOUVELLE AFFAIRE + AFFAIRES CLASSEES
    # ======================================
    frame_top_buttons = tk.Frame(fenetre)
    frame_top_buttons.pack(fill="x", padx=40, pady=20)

    bouton_nouvelle = tk.Button(
        frame_top_buttons,
        text="Nouvelle Affaire",
        font=("Arial", 16, "bold"),
        padx=20,
        pady=15,
        height=2,
        command=lambda: nouvelle_affaire_interface(fenetre)
    )
    bouton_nouvelle.pack(side="left", expand=True, fill="x", padx=(0, 10))

    bouton_classees = tk.Button(
        frame_top_buttons,
        text="Affaires classées",
        font=("Arial", 16, "bold"),
        padx=20,
        pady=15,
        height=2,
        command=lambda: affaires_classees_interface(fenetre)
    )
    bouton_classees.pack(side="left", expand=True, fill="x", padx=(10, 0))

    # ======================================
    #   SCROLLBAR + CANVAS
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

    # Mise à jour automatique de la taille
    def update_scrollregion(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_global.bind("<Configure>", update_scrollregion)

    def resize_canvas(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    # ======================================
    #   SCROLL GLOBAL — ACTIF UNIQUEMENT DANS L’ACCUEIL
    # ======================================
    def _global_mousewheel(event):
        if event.delta:
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        else:
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

    fenetre.bind("<MouseWheel>", _global_mousewheel)
    fenetre.bind("<Button-4>", _global_mousewheel)
    fenetre.bind("<Button-5>", _global_mousewheel)
    global_mousewheel_bind = True

    # ======================================
    #   CHARGEMENT DES AFFAIRES
    # ======================================
    affaires = charger_affaires()
    en_cours, surveiller, gelee = trier_par_etat(affaires)

    # ======================================
    #   AFFICHAGE DES CARTES
    # ======================================
    def afficher_cartes(frame_parent, liste_affaires):
        cards = []

        # --- Fonction interne pour supprimer une affaire ---
        def supprimer_affaire(path, card_widget):
            if not messagebox.askyesno(
                "Supprimer",
                "Voulez-vous vraiment supprimer cette affaire ?"
            ):
                return

            try:
                os.remove(path)
            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible de supprimer l'affaire :\n{e}"
                )
                return

            # Supprime la carte visuellement
            card_widget.destroy()
            messagebox.showinfo("Supprimé", "Affaire supprimée avec succès.")

            # Recharge entièrement l'accueil pour mettre à jour les listes
            accueil(fenetre)

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

            # ------- CONTENU DE LA CARTE -------
            tk.Label(
                card_inner,
                text=affaire["titre"],
                font=("Arial", 12, "bold"),
                bg="white", wraplength=290, justify="left"
            ).pack(anchor="w")

            tk.Label(
                card_inner,
                text=f"📍 {affaire['lieu']}",
                bg="white"
            ).pack(anchor="w")

            tk.Label(
                card_inner,
                text=f"📅 Dernier mouvement : {affaire['date_dernier_mouvement']}",
                bg="white"
            ).pack(anchor="w")

            tk.Label(
                card_inner,
                text=f"🧩 {affaire['type_affaire']}",
                bg="white"
            ).pack(anchor="w")

            tk.Label(
                card_inner,
                text=f"👮 {affaire['responsable']}",
                bg="white"
            ).pack(anchor="w")

            tk.Label(
                card_inner,
                text=f"Victimes: {affaire['victimes']}   Suspects: {affaire['suspects']}   Témoins: {affaire['temoins']}",
                bg="white"
            ).pack(anchor="w")

            tk.Button(
                card_inner,
                text="Ouvrir",
                command=lambda p=affaire["path"]: ouvrir_affaire(p, lambda: accueil(fenetre))
            ).pack(anchor="e", pady=5)


            # ------- BOUTON SUPPRESSION EN OVERLAY -------
            btn_delete = tk.Button(
                card,
                text="✖",
                fg="red",   # croix rouge
                bg="white",  # bouton blanc
                width=2,
                height=1,
                bd=0,
                relief="solid",
                font=("Arial", 10, "bold"),
                command=lambda p=affaire["path"], c=card: supprimer_affaire(p, c)
            )
            # Positionnement du bouton
            btn_delete.place(relx=1.0, x=-5, y=5, anchor="ne")
            btn_delete.lift()  # s'assure qu'il est au-dessus du contenu

        # Positionnement responsive
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
    tk.Label(
        frame_global,
        text="🟢 Affaires en cours",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    ).pack(anchor="w", pady=(10, 5))

    frame_en_cours = tk.Frame(frame_global, bg="#f0f0f0")
    frame_en_cours.pack(fill="x")
    afficher_cartes(frame_en_cours, en_cours)

    tk.Label(
        frame_global,
        text="🟡 Affaires à surveiller",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    ).pack(anchor="w", pady=(20, 5))

    frame_surveiller = tk.Frame(frame_global, bg="#f0f0f0")
    frame_surveiller.pack(fill="x")
    afficher_cartes(frame_surveiller, surveiller)

    tk.Label(
        frame_global,
        text="🔵 Affaires gelées",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    ).pack(anchor="w", pady=(20, 5))

    frame_gelee = tk.Frame(frame_global, bg="#f0f0f0")
    frame_gelee.pack(fill="x")
    afficher_cartes(frame_gelee, gelee)


# ============================================================
#   INTERFACE : AFFAIRES CLASSÉES
# ============================================================
def affaires_classees_interface(fenetre):
    """
    Interface dédiée qui affiche uniquement les affaires dont l'état contient 'class'
    (ex: '🟣 Affaire classée', 'Affaire classée non élucidée', etc.).
    """
    global global_mousewheel_bind

    # Nettoyage
    for widget in fenetre.winfo_children():
        widget.destroy()

    # Désactive d'éventuels anciens scrolls globaux
    if global_mousewheel_bind:
        fenetre.unbind_all("<MouseWheel>")
        fenetre.unbind_all("<Button-4>")
        fenetre.unbind_all("<Button-5>")
        global_mousewheel_bind = False

    fenetre.title("Affaires classées")

    # ======================================
    #   BOUTON RETOUR
    # ======================================
    top_bar = tk.Frame(fenetre)
    top_bar.pack(fill="x", padx=40, pady=10)

    tk.Button(
        top_bar,
        text="⬅ Retour à l'accueil",
        font=("Arial", 12, "bold"),
        command=lambda: accueil(fenetre)
    ).pack(side="left")

    tk.Label(
        top_bar,
        text="Affaires classées",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=40)

    # ======================================
    #   SCROLLBAR + CANVAS
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

    def resize_canvas(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    # Scroll souris spécifique à cette vue
    def _mousewheel(event):
        if event.delta:
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        else:
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

    fenetre.bind("<MouseWheel>", _mousewheel)
    fenetre.bind("<Button-4>", _mousewheel)
    fenetre.bind("<Button-5>", _mousewheel)
    global_mousewheel_bind = True

    # ======================================
    #   CHARGEMENT + FILTRE
    # ======================================
    affaires = charger_affaires()
    affaires_classees = [
        a for a in affaires
        if "class" in a["etat"].lower()  # "classée", "classées", etc.
    ]

    # ======================================
    #   AFFICHAGE DES CARTES
    # ======================================
    tk.Label(
        frame_global,
        text="🟣 Affaires classées",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    ).pack(anchor="w", pady=(10, 5))

    frame_liste = tk.Frame(frame_global, bg="#f0f0f0")
    frame_liste.pack(fill="x")

    cards = []

    def supprimer_affaire(path, card_widget):
        if not messagebox.askyesno(
            "Supprimer",
            "Voulez-vous vraiment supprimer cette affaire classée ?"
        ):
            return

        try:
            os.remove(path)
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de supprimer l'affaire :\n{e}"
            )
            return

        card_widget.destroy()
        messagebox.showinfo("Supprimé", "Affaire supprimée avec succès.")
        # Recharge cette interface pour mettre la liste à jour
        affaires_classees_interface(fenetre)

    for affaire in affaires_classees:
        card = tk.Frame(
            frame_liste,
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

        tk.Label(
            card_inner,
            text=affaire["titre"],
            font=("Arial", 12, "bold"),
            bg="white", wraplength=290, justify="left"
        ).pack(anchor="w")

        tk.Label(
            card_inner,
            text=f"📍 {affaire['lieu']}",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            card_inner,
            text=f"📅 Dernier mouvement : {affaire['date_dernier_mouvement']}",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            card_inner,
            text=f"🧩 {affaire['type_affaire']}",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            card_inner,
            text=f"👮 {affaire['responsable']}",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            card_inner,
            text=f"Victimes: {affaire['victimes']}   Suspects: {affaire['suspects']}   Témoins: {affaire['temoins']}",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            card_inner,
            text=f"État : {affaire['etat']}",
            bg="white"
        ).pack(anchor="w")

        tk.Button(
            card_inner,
            text="Ouvrir",
            command=lambda p=affaire["path"]: ouvrir_affaire(p, lambda: affaires_classees_interface(fenetre))
        ).pack(anchor="e", pady=5)


        btn_delete = tk.Button(
            card,
            text="✖",
            fg="red",
            bg="white",
            width=2,
            height=1,
            bd=0,
            relief="solid",
            font=("Arial", 10, "bold"),
            command=lambda p=affaire["path"], c=card: supprimer_affaire(p, c)
        )
        btn_delete.place(relx=1.0, x=-5, y=5, anchor="ne")
        btn_delete.lift()

    def repositionner(event=None):
        largeur = frame_liste.winfo_width()
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

    frame_liste.bind("<Configure>", repositionner)
    repositionner()

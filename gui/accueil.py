import tkinter as tk
from tkinter import ttk, messagebox
import json

from gui.nouvelle_affaire import nouvelle_affaire_interface
from utils.loader import charger_affaires, trier_par_etat


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

    # ================================
    #   BARRE Titre + BOUTON Modifier
    # ================================
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

    # ================================
    #   ZONE SCROLLABLE
    # ================================
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

    # ================================
    #   SCROLL MULTI-FENÊTRES PRO
    # ================================
    def _on_mousewheel(event):
        # Windows / Mac
        if event.delta:
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        else:
            # Linux
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

    # Bind uniquement pour CETTE fenêtre
    popup.bind("<MouseWheel>", _on_mousewheel)      # Windows / macOS
    popup.bind("<Button-4>", _on_mousewheel)        # Linux scroll up
    popup.bind("<Button-5>", _on_mousewheel)        # Linux scroll down

    # ================================
    #   AFFICHAGE DU CONTENU
    # ================================
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
    def afficher_cartes(frame_parent, liste_affaires):

        cards = []

        for affaire in liste_affaires:

            # --- CADRE FIXE EXACTEMENT COMME AVANT ---
            card = tk.Frame(
                frame_parent,
                bd=1,
                relief="solid",
                bg="white",
                width=320,
                height=210
            )

            # Empêche tout changement de taille
            card.pack_propagate(False)
            card.grid_propagate(False)

            # Ajout d’un cadre interne pour les paddings
            card_inner = tk.Frame(card, bg="white")
            card_inner.pack(fill="both", expand=True, padx=10, pady=10)

            cards.append(card)

            # TITRE
            tk.Label(card_inner, text=affaire["titre"], font=("Arial", 12, "bold"),
                     bg="white", wraplength=290, justify="left").pack(anchor="w")

            # INFOS
            tk.Label(card_inner, text=f"📍 {affaire['lieu']}", bg="white").pack(anchor="w")
            tk.Label(card_inner, text=f"📅 Dernier mouvement : {affaire['date_dernier_mouvement']}", bg="white").pack(anchor="w")
            tk.Label(card_inner, text=f"🧩 {affaire['type_affaire']}", bg="white").pack(anchor="w")
            tk.Label(card_inner, text=f"👮 {affaire['responsable']}", bg="white").pack(anchor="w")

            tk.Label(
                card_inner,
                text=f"Victimes: {affaire['victimes']}   Suspects: {affaire['suspects']}   Témoins: {affaire['temoins']}",
                bg="white"
            ).pack(anchor="w")

            # Bouton ouvrir
            tk.Button(
                card_inner,
                text="Ouvrir",
                command=lambda p=affaire["path"]: ouvrir_affaire(p)
            ).pack(anchor="e", pady=5)

        # --- DISPOSITION AUTOMATIQUE COMME AVANT ---
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
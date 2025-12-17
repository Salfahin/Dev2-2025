from __future__ import annotations
from gui.theme import *

import tkinter as tk
from tkinter import messagebox

from core.services.affaire_service import AffaireService
from gui.nouvelle_affaire_view import NouvelleAffaireView
from gui.ouvrir_affaire_view import OuvrirAffaireView
from gui.filtrage import FiltreFenetre


class AccueilView:
    """
    Vue principale affichant la liste des affaires.
    """

    def __init__(self, root: tk.Tk, service: AffaireService):
        self.root = root
        self.service = service
        self.root.configure(bg=BG_MAIN)
        self.root.title("AffairTrack")

        # Pour gérer les bindings de scroll global
        self._mousewheel_active = False

        self.build()

    # -------------------------------------------------------
    #   RECONSTRUIRE LA FENÊTRE
    # -------------------------------------------------------
    def build(self):
        """Construit toute la fenêtre d’accueil."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=BG_MAIN)
        self.root.geometry("700x750")

        # Désactive anciens scrolls
        if self._mousewheel_active:
            self.root.unbind_all("<MouseWheel>")
            self.root.unbind_all("<Button-4>")
            self.root.unbind_all("<Button-5>")
            self._mousewheel_active = False

        self.build_top_buttons()
        self.build_affaires_section()

    # -------------------------------------------------------
    #   BOUTONS DU HAUT
    # -------------------------------------------------------
    def build_top_buttons(self):
        top_bar = tk.Frame(self.root, bg=BG_MAIN)
        top_bar.pack(fill="x", padx=40, pady=20)
        frame = tk.Frame(self.root, bg=BG_MAIN)
        frame.pack(fill="x", padx=40, pady=20)

        # Nouveau
        btn_new = tk.Button(
            frame,
            text="Nouvelle Affaire",
            font=("Arial", 16, "bold"),
            padx=20, pady=15, bg=PRIMARY, fg="white",
            command=lambda: NouvelleAffaireView(self.root, self.service, on_done=self.refresh)
        )
        btn_new.pack(side="left", expand=True, fill="x", padx=(0, 10))

        # Affaires classées
        btn_closed = tk.Button(
            frame,
            text="Affaires classées",
            font=("Arial", 16, "bold"),
            padx=20, pady=15, bg=PRIMARY, fg="white",
            command=self.show_affaires_classees
        )
        btn_closed.pack(side="left", expand=True, fill="x", padx=(10, 0))

        #button de filtrage
        btn_filter = tk.Button(
            frame,
            text="🔍 Filtrer",
            font=("Arial", 16, "bold"),
            padx=20, pady=15, bg=PRIMARY, fg="white",
            command=self.open_filter_popup
        )
        btn_filter.pack(side="left", expand=True, fill="x", padx=(10, 0))

    #methode de filtrage
    def open_filter_popup(self):
        FiltreFenetre(
            parent=self.root,
            service=self.service,
            on_apply=self.apply_filtered_affaires,
            on_reset=self.reset_filter
        )   

    def apply_filtered_affaires(self, affaires):
        self.render_affaires(affaires)

    def reset_filter(self):
        self.refresh()


    # -------------------------------------------------------
    #   AFFICHAGE DES AFFAIRES AVEC SCROLL
    # -------------------------------------------------------
    def build_affaires_section(self):
        # Scroll global
        container = tk.Frame(self.root, bg=BG_MAIN)
        container.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical")
        scrollbar.pack(side="left", fill="y")

        self.canvas = tk.Canvas(container, highlightthickness=0, bg=BG_MAIN)
        self.canvas.pack(side="right", fill="both", expand=True)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.canvas.yview)

        self.frame_global = tk.Frame(self.canvas, bg=BG_MAIN)
        self.window_id = self.canvas.create_window((0, 0), window=self.frame_global, anchor="nw")

        # Auto resize
        self.frame_global.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.window_id, width=e.width))

        # Scroll souris
        self.enable_global_mousewheel()

        # Charger affaires
        self.display_affaires()

    # -------------------------------------------------------
    #   SCROLL SOURIS GLOBAL
    # -------------------------------------------------------
    def enable_global_mousewheel(self):
        def _mouse(event):
            if not hasattr(self, "canvas"):
                return
            if not self.canvas.winfo_exists():
                return

            if event.delta:
                self.canvas.yview_scroll(-int(event.delta / 120), "units")
            else:
                if event.num == 4:
                    self.canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.canvas.yview_scroll(1, "units")

        self.root.bind_all("<MouseWheel>", _mouse)
        self.root.bind_all("<Button-4>", _mouse)
        self.root.bind_all("<Button-5>", _mouse)
        self._mousewheel_active = True

    # -------------------------------------------------------
    #   AFFICHAGE DES AFFAIRES
    # -------------------------------------------------------
    def display_affaires(self):
        affaires = self.service.get_all()
        self.render_affaires(affaires)

    # -----------------------------------------------
    # interface principal des affaires après filtrage
    #------------------------------------------------

    def render_affaires(self, affaires: list):
        # Nettoyer la zone scroll
        for w in self.frame_global.winfo_children():
            w.destroy()

        en_cours, surveiller, gelee = self.service.trier_par_etat(affaires)

        # Section : En cours
        tk.Label(self.frame_global, text="🟢 Affaires en cours",
            font=SECTION_FONT, bg=BG_MAIN, fg=SUCCESS).pack(anchor="w", pady=(10, 5))
        frame_cours = tk.Frame(self.frame_global, bg=BG_MAIN)
        frame_cours.pack(fill="x")
        self._afficher_cartes(frame_cours, en_cours)

        # Section : Surveiller
        tk.Label(self.frame_global, text="🟡 Affaires à surveiller",
            font=SECTION_FONT, bg=BG_MAIN, fg=WARNING).pack(anchor="w", pady=(20, 5))
        frame_surv = tk.Frame(self.frame_global, bg=BG_MAIN)
        frame_surv.pack(fill="x")
        self._afficher_cartes(frame_surv, surveiller)

        # Section : Gelée
        tk.Label(self.frame_global, text="🔵 Affaires gelées",
            font=SECTION_FONT, bg=BG_MAIN, fg=INFO).pack(anchor="w", pady=(20, 5))
        frame_gel = tk.Frame(self.frame_global, bg=BG_MAIN)
        frame_gel.pack(fill="x")
        self._afficher_cartes(frame_gel, gelee)


    # -------------------------------------------------------
    #   AFFICHAGE D'UN ENSEMBLE DE CARTES
    # -------------------------------------------------------
    def _afficher_cartes(self, parent: tk.Frame, affaires: list):
        cards = []

        for affaire in affaires:
            card = tk.Frame(parent, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, width=320, height=210)
            card.pack_propagate(False)

            content = tk.Frame(card, bg=BG_CARD)
            content.pack(fill="both", expand=True, padx=10, pady=10)

            # Texte
            tk.Label(content, text=affaire.titre, font=CARD_TITLE_FONT, bg=BG_CARD, fg=TEXT_MAIN).pack(anchor="w")

            tk.Label(content, text=f"📍 {affaire.lieu}", bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
            tk.Label(content, text=f"🧩 {affaire.type_affaire}", bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
            tk.Label(content, text=f"👮 {affaire.responsables}", bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")

            tk.Label(content, text=f"Victimes: {affaire.nombre_victimes()}   "
                                   f"Suspects: {affaire.nombre_suspects()}   "
                                   f"Témoins: {affaire.nombre_temoins()}",
                     bg="white").pack(anchor="w")

            # Ouvrir affaire
            tk.Button(content,
                text="Ouvrir",
                font=("Segoe UI", 10, "bold"),
                bg=PRIMARY,
                fg="white",
                bd=0,
                padx=14,
                pady=7,
                cursor="hand2",
                activebackground=PRIMARY_DARK,
                activeforeground="white",
                      command=lambda a=affaire: OuvrirAffaireView(self.root, self.service, a, on_done=self.refresh)
                      ).pack(anchor="e", pady=5)

            # Supprimer
            btn_delete = tk.Button(
                card,
                text="✖",
                fg=DANGER,
                bg=BG_CARD,
                bd=0, cursor="hand2",
                font=("Segoe UI", 11, "bold"),
                activeforeground="#991b1b",
                command=lambda a=affaire, c=card: self._supprimer_affaire(a, c)
            )
            btn_delete.place(relx=1.0, x=-5, y=5, anchor="ne")

            cards.append(card)

        # Positionnement dynamique
        def reposition(event=None):
            width = parent.winfo_width()
            card_width = 340
            max_cols = max(1, width // card_width)

            row = col = 0
            for card in cards:
                card.grid_forget()
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nw")
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

        parent.bind("<Configure>", reposition)
        reposition()

    # -------------------------------------------------------
    #   SUPPRESSION D'UNE AFFAIRE
    # -------------------------------------------------------
    def _supprimer_affaire(self, affaire, widget):
        if not messagebox.askyesno("Supprimer", "Voulez-vous supprimer cette affaire ?"):
            return

        self.service.delete(affaire)
        widget.destroy()
        self.refresh()

    # -------------------------------------------------------
    #   AFFICHAGE DES AFFAIRES CLASSÉES
    # -------------------------------------------------------
    def show_affaires_classees(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=BG_MAIN)

        # Titre + retour
        top = tk.Frame(self.root, bg=BG_MAIN)
        top.pack(fill="x", padx=40, pady=10)

        tk.Button(top, text="⬅ Retour", font=("Arial", 12, "bold"),
                  command=self.refresh).pack(side="left")

        tk.Label(top, text="Affaires classées", font=("Arial", 18, "bold"), bg=BG_MAIN).pack(side="left", padx=40)

        # Setup scroll area
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical")
        scrollbar.pack(side="left", fill="y")

        canvas = tk.Canvas(container, bg="#f0f0f0")
        canvas.pack(side="right", fill="both", expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=canvas.yview)

        frame = tk.Frame(canvas, bg="#f0f0f0")
        window_id = canvas.create_window((0, 0), window=frame, anchor="nw")

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))

        # Charger les affaires classées
        affaires = self.service.get_all()
        classees = self.service.affaires_classees(affaires)

        self._afficher_cartes(frame, classees)

    # -------------------------------------------------------
    #   RAFRAICHIR L'ACCUEIL
    # -------------------------------------------------------
    def refresh(self):
        """Recharge complètement l’interface d’accueil."""
        self.build()
